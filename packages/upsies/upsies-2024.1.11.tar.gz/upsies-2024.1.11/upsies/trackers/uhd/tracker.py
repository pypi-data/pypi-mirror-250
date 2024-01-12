"""
Concrete :class:`~.base.TrackerBase` subclass for UHD
"""

import re
import urllib
from datetime import datetime

from ... import __project_name__, errors, utils
from ..base import TrackerBase
from .config import UhdTrackerConfig
from .jobs import UhdTrackerJobs

import logging  # isort:skip
_log = logging.getLogger(__name__)


class UhdTracker(TrackerBase):
    name = 'uhd'
    label = 'UHD'

    setup_howto_template = (
        ...
    )

    TrackerConfig = UhdTrackerConfig
    TrackerJobs = UhdTrackerJobs

    @property
    def _base_url(self):
        return self.options['base_url']

    @property
    def _login_url(self):
        return urllib.parse.urljoin(self._base_url, '/login.php')

    @property
    def _logout_url(self):
        return urllib.parse.urljoin(self._base_url, '/logout.php')

    @property
    def _ajax_url(self):
        return urllib.parse.urljoin(self._base_url, '/ajax.php')

    @property
    def _upload_url(self):
        return urllib.parse.urljoin(self._base_url, '/upload.php')

    @property
    def _torrents_url(self):
        return urllib.parse.urljoin(self._base_url, '/torrents.php')

    async def _request(self, method, *args, error_prefix='', **kwargs):

        # raise RuntimeError('nope')

        try:
            # `method` is "GET" or "POST"
            return await getattr(utils.http, method.lower())(
                *args,
                user_agent=True,
                cache=False,
                **kwargs,
            )
        except errors.RequestError as e:
            if error_prefix:
                raise errors.RequestError(f'{error_prefix}: {e}')
            else:
                raise e

    def _failed_to_find_error(self, doc, msg_prefix):
        filepath = f'{msg_prefix}.{self.name}.html'
        utils.html.dump(doc, filepath)
        raise RuntimeError(f'{msg_prefix}: No error message found (dumped HTML response to {filepath})')

    async def _login(self):
        if not self.options.get('username'):
            raise errors.RequestError('Login failed: No username configured')
        elif not self.options.get('password'):
            raise errors.RequestError('Login failed: No password configured')

        _log.debug('%s: Logging in as %r', self.name, self.options['username'])
        post_data = {
            'username': self.options['username'],
            'password': self.options['password'],
            'two_step': '',  # 2FA
            'login': 'Log in',
        }

        response = await self._request(
            method='POST',
            url=f'{self._login_url}',
            data=post_data,
            error_prefix='Login failed',
            debug_file='login.uhd',
        )

        self._confirm_login(response)
        _log.debug('%s: Logged in as %r', self.name, self.options['username'])

    def _confirm_login(self, response):
        doc = utils.html.parse(response)
        auth_regex = re.compile(r'logout\.php\?.*\bauth=([0-9a-zA-Z]+)')
        logout_link_tag = doc.find('a', href=auth_regex)
        if logout_link_tag:
            logout_link_href = logout_link_tag['href']
            match = auth_regex.search(logout_link_href)
            self._auth = match.group(1)
        else:
            msg_prefix = 'Login failed'
            form_tag = doc.find('form', action='login.php')
            if form_tag:
                form_tag.table.extract()
                msg = utils.html.as_text(form_tag)
                raise errors.RequestError(f'{msg_prefix}: {msg}')
            else:
                self._failed_to_find_error(doc, msg_prefix)

    async def _logout(self):
        try:
            _log.debug('%s: Logging out', self.name)
            await self._request(
                method='GET',
                url=self._logout_url,
                params={'auth': self._auth},
                error_prefix='Logout failed',
                debug_file='logout.uhd',
            )
        finally:
            delattr(self, '_auth')
            _log.debug('%s: Logged out', self.name)

    async def get_announce_url(self):
        if self.options.get('announce_url'):
            return self.options['announce_url']
        else:
            if not self.is_logged_in:
                raise RuntimeError('Call login() first')

            response = await self._request(
                method='GET',
                url=self._upload_url,
                debug_file='get_announce.uhd',
            )
            doc = utils.html.parse(response)
            announce_url_tag = doc.find('input', value=re.compile(r'^https?://.*/announce\b'))
            if announce_url_tag:
                return announce_url_tag['value']
            else:
                cmd = f'{__project_name__} set trackers.{self.name}.announce_url YOUR_URL'
                raise errors.RequestError(f'Failed to find announce URL - set it manually: {cmd}')

    async def get_uhd_info(self, imdb_id):
        assert imdb_id, 'IMDb ID is not available yet'
        params = {
            'action': 'imdb_fetch',
            'imdbid': imdb_id,
            # Local unix time in milliseconds. We use UTC time at midnight so we
            # can cache the response for one day.
            '_': int(
                datetime.now()
                .replace(hour=0, minute=0, second=0, microsecond=0)
                .timestamp()
            ) * 1000,
        }
        response = await utils.http.get(
            url=self._ajax_url,
            params=params,
            user_agent=True,
            cache=True,
            debug_file='ajax.uhd',
        )
        _log.debug('UHD INFO: %r', response)
        return response.json()

    async def upload(self, tracker_jobs):
        assert self.is_logged_in

        post_data = tracker_jobs.post_data
        post_data['auth'] = self._auth

        _log.debug('POSTing data:')
        for k, v in post_data.items():
            _log.debug(' * %s = %s', k, v)

        post_files = tracker_jobs.post_files
        _log.debug('POSTing files: %r', post_files)

        response = await self._request(
            method='POST',
            url=self._upload_url,
            data=post_data,
            files=post_files,
            follow_redirects=True,
            debug_file='upload.uhd',
        )

        return self._handle_upload_response(response)

    # Error message CSS selector: '#scontent .thin p + p'

    def _handle_upload_response(self, response):
        # "Location" header should contain the uploaded torrent's URL
        _log.debug('Upload response headers: %r', response.headers)
        location = response.headers.get('Location')
        _log.debug('Upload response location: %r', location)

        if location:
            torrent_page_url = urllib.parse.urljoin(self.options['base_url'], location)
            # Redirect URL should start with "https://.../torrents.php"
            if torrent_page_url.startswith(self._torrents_url):
                return torrent_page_url

        # Find error message in HTML
        msg_prefix = 'Upload failed'
        doc = utils.html.parse(response)
        alert_tag = doc.find(class_='alert')
        if alert_tag:
            msg = utils.html.as_text(alert_tag)
            raise errors.RequestError(f'{msg_prefix}: {msg}')

        # Failed to find error message
        self._failed_to_find_error(doc, msg_prefix)
