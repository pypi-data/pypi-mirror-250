"""
Concrete :class:`~.base.TrackerJobsBase` subclass for UHD
"""

import functools
import re
from datetime import datetime

from ... import __homepage__, __project_name__, errors, jobs, utils
from ..base import TrackerJobsBase

import logging  # isort:skip
_log = logging.getLogger(__name__)


class UhdTrackerJobs(TrackerJobsBase):

    @functools.cached_property
    def jobs_before_upload(self):
        return (
            # Common interactive jobs
            self.imdb_job,
            self.type_job,
            self.year_job,
            self.quality_job,
            self.version_job,
            self.source_job,
            self.codec_job,
            self.hdr_format_job,
            self.tags_job,
            self.poster_job,
            self.trailer_job,
            self.season_job,
            self.scene_check_job,

            # Common background jobs
            self.create_torrent_job,
            self.mediainfo_job,
            self.screenshots_job,
            self.upload_screenshots_job,
            self.description_job,
        )

    @property
    def isolated_jobs(self):
        """
        Sequence of job attribute names (e.g. "title_job") that were singled
        out by the user, e.g. with --only-title
        """
        if self.options.get('only_description', False):
            return self.get_job_and_dependencies(
                self.description_job,
                # `screenshots_job` is needed by `upload_screenshots_job`, but
                # `upload_screenshots_job` is a `QueueJobBase`, which doesn't
                # know anything about the job it gets input from and therefore
                # can't tells us that it needs `screenshots_job`.
                self.screenshots_job,
            )
        else:
            # Activate all jobs in jobs_before/after_upload
            return ()

    def update_imdb_query(self, type_job_):
        """
        Set :attr:`~.webdbs.common.Query.type` on
        :attr:`~.TrackerJobsBase.imdb_job` to :attr:`~.ReleaseType.movie` or
        :attr:`~.ReleaseType.series` depending on the output of :attr:`type_job`
        """
        assert self.type_job.is_finished
        if self.type_job.output:
            new_type = self.type_job.output[0]
            if new_type == 'Movie':
                _log.debug('Updating IMDb query type: %r', utils.release.ReleaseType.movie)
                self.imdb_job.query.type = utils.release.ReleaseType.movie
            elif new_type == 'TV':
                _log.debug('Updating IMDb query type: %r', utils.release.ReleaseType.series)
                self.imdb_job.query.type = utils.release.ReleaseType.series

    @functools.cached_property
    def type_job(self):
        return jobs.dialog.ChoiceJob(
            name=self.get_job_name('type'),
            label='Type',
            precondition=self.make_precondition('type_job'),
            prejobs=(
                self.imdb_job,
            ),
            autodetect=self.autodetect_type,
            autofinish=True,
            options=(
                ('Movie', '0'),
                # ("Music", '1'),  # Not supported by upsies
                ('TV', '2'),
            ),
            **self.common_job_args(ignore_cache=True),
        )

    async def autodetect_type(self, _):
        assert self.imdb_job.is_finished, self.imdb_job
        if self.imdb_job.output:
            imdb_id = self.imdb_job.output[0]
            type = await self.imdb.type(imdb_id)
            if type is utils.release.ReleaseType.movie:
                return 'Movie'
            elif type in (
                    utils.release.ReleaseType.season,
                    utils.release.ReleaseType.episode,
            ):
                return 'TV'

    @functools.cached_property
    def year_job(self):
        return jobs.dialog.TextFieldJob(
            name=self.get_job_name('year'),
            label='Year',
            precondition=self.make_precondition('year_job'),
            prejobs=(
                self.imdb_job,
            ),
            text=self.autodetect_year,
            nonfatal_exceptions=(
                errors.RequestError,
            ),
            normalizer=self.normalize_year,
            validator=self.validate_year,
            finish_on_success=True,
            **self.common_job_args(),
        )

    async def autodetect_year(self):
        json = await self._tracker.get_uhd_info(self.imdb_id)
        year = json.get('year', None)
        _log.debug('Autodetected UHD year: %r', year)
        if year:
            return year

        year = await self.imdb.year(self.imdb_id)
        if year:
            _log.debug('Autodetected IMDb year: %r', year)
            return year

    def normalize_year(self, text):
        return text.strip()

    def validate_year(self, text):
        if not text:
            raise ValueError('Year must not be empty.')
        try:
            year = int(text)
        except ValueError:
            raise ValueError('Year must be a number.')
        else:
            if not 1800 < year < datetime.now().year + 10:
                raise ValueError('Year is not reasonable.')

    @functools.cached_property
    def season_job(self):
        if self.release_name.type in (
                utils.release.ReleaseType.season,
                utils.release.ReleaseType.episode,
        ):
            return jobs.dialog.TextFieldJob(
                name=self.get_job_name('season'),
                label='Season',
                precondition=self.make_precondition('season_job'),
                text=self.autodetect_season,
                normalizer=self.normalize_season,
                validator=self.validate_season,
                finish_on_success=True,
                **self.common_job_args(ignore_cache=True),
            )

    async def autodetect_season(self):
        if (
                self.release_name.only_season
                and 'UNKNOWN' not in self.release_name.only_season
        ):
            return self.release_name.only_season

    def normalize_season(self, text):
        return text.strip()

    def validate_season(self, text):
        if not text:
            raise ValueError('Season must not be empty.')
        try:
            season = int(text)
        except ValueError:
            raise ValueError('Season must be a number.')
        else:
            # NOTE: Season 0 is ok for pilots, specials, etc.
            if not 0 <= season <= 100:
                raise ValueError('Season is not reasonable.')

    @functools.cached_property
    def quality_job(self):
        return jobs.dialog.ChoiceJob(
            name=self.get_job_name('quality'),
            label='Quality',
            precondition=self.make_precondition('quality_job'),
            autodetect=self.autodetect_quality,
            autofinish=True,
            options=(
                ('mHD', 'mHD'),
                ('720p', '720p'),
                ('1080p', '1080p'),
                ('1080i', '1080i'),
                ('2160p', '2160p'),
                ('Other', 'Others'),
            ),
            **self.common_job_args(),
        )

    async def autodetect_quality(self, _):
        resolution_int = utils.video.resolution_int(self.content_path)
        _log.debug('Autodetecting quality: %s', resolution_int)
        if resolution_int > 2160:
            return 'Other'
        elif resolution_int == 2160:
            return '2160p'
        elif utils.video.resolution(self.content_path) == '1080i':
            return '1080i'
        elif resolution_int >= 1080:
            return '1080p'
        elif resolution_int >= 720:
            return '720p'
        else:
            return 'mHD'

    @functools.cached_property
    def version_job(self):
        return jobs.custom.CustomJob(
            name=self.get_job_name('version'),
            label='Version',
            precondition=self.make_precondition('version_job'),
            worker=self.autodetect_version,
            # Non-special releases produce no output, which is not an error.
            no_output_is_ok=True,
            **self.common_job_args(ignore_cache=True),
        )

    async def autodetect_version(self, _):
        versions = set()
        for version, is_version in self.version_map.items():
            if not is_version:
                _log.debug('Unsupported autodetection for %r', version)
            elif is_version(self.release_name):
                _log.debug('Autodetected version: %r', version)
                versions.add(version)
        return versions

    version_map = {
        "Director's Cut": lambda release: "Director's Cut" in release.edition,
        'Theatrical': lambda release: 'Theatrical Cut' in release.edition,
        'Extended': lambda release: 'Extended Cut' in release.edition,
        'IMAX': lambda release: 'IMAX' in release.edition,
        'Uncut': lambda release: 'Uncut' in release.edition,
        'TV Cut': lambda release: None,  # TODO
        'Unrated': lambda release: 'Unrated' in release.edition,
        'Remastered': lambda release: 'Remastered' in release.edition,
        '4K Remaster': lambda release: '4k Remastered' in release.edition,
        '4K Restoration': lambda release: '4k Restored' in release.edition,
        'B&W Version': None,  # TODO
        'Criterion': lambda release: 'Criterion Collection' in release.edition,
        '2in1': lambda release: '2in1' in release.edition,
        '3in1': lambda release: '3in1' in release.edition,
        'Hybrid': lambda release: 'Hybrid' in release.source,
        '10-bit': lambda release: utils.video.bit_depth(release.path) == 10,
        'Extras': None,
    }

    # On the website, this is called "Media".
    @functools.cached_property
    def source_job(self):
        return jobs.dialog.ChoiceJob(
            name=self.get_job_name('source'),
            label='Source',
            precondition=self.make_precondition('source_job'),
            autodetect=self.autodetect_source,
            autofinish=True,
            options=(
                ('Blu-ray', 'Blu-ray'),
                ('Remux', 'Remux'),
                ('Encode', 'Encode'),
                ('WEB-DL', 'WEB-DL'),
                ('WEBRip', 'WEBRip'),
                ('HDRip', 'HDRip'),
                ('HDTV', 'HDTV'),
                ('Other', 'Others'),
            ),
            **self.common_job_args(ignore_cache=True),
        )

    async def autodetect_source(self, _):
        for source, is_source in self.source_map.items():
            if is_source(self.release_name):
                _log.debug('Autodetected source: %r', source)
                return source

    source_map = {
        'Encode': lambda release: any(
            source in release.source
            for source in (
                'BluRay',
                'HD-DVD',
            )),
        'WEB-DL': lambda release: 'WEB-DL' in release.source,
        'WEBRip': lambda release: 'WEBRip' in release.source,
        # Not sure what "HDRip" is exactly and how to detect it.
        'HDRip': lambda release: 'Rip' in release.source,
        'HDTV': lambda release: 'HDTV' in release.source,
    }

    @functools.cached_property
    def codec_job(self):
        return jobs.dialog.ChoiceJob(
            name=self.get_job_name('codec'),
            label='Codec',
            precondition=self.make_precondition('codec_job'),
            autodetect=self.autodetect_codec,
            autofinish=True,
            options=(
                ('x264', 'x264'),
                ('x265', 'x265'),
                ('x266', 'x266'),
                ('H.264', 'H.264'),  # AVC aka H.264
                ('H.265', 'HEVC'),   # HEVC aka H.265
                ('AV1', 'AV1'),
                ('VC-1', 'VC-1'),
                ('MPEG-2', 'MPEG-2'),
            ),
            **self.common_job_args(ignore_cache=True),
        )

    async def autodetect_codec(self, _):
        for codec, is_codec in self.codec_map.items():
            if is_codec(self.release_name):
                _log.debug('Autodetected video codec: %r', codec)
                return codec

    codec_map = {
        # TODO: Add support for commented-out codecs in utils.video and ReleaseName.
        'x264': lambda release: release.video_format == 'x264',
        'x265': lambda release: release.video_format == 'x265',
        # 'x266': lambda release: release.video_format == 'x266',
        'H.264': lambda release: release.video_format == 'H.264',
        'H.265': lambda release: release.video_format == 'H.265',
        # 'AV1': lambda release: release.video_format == 'AV1',
        # 'VC-1': lambda release: release.video_format == 'VC-1',
        # 'MPEG-2': lambda release: release.video_format == 'MPEG-2',
    }

    @functools.cached_property
    def hdr_format_job(self):
        return jobs.dialog.ChoiceJob(
            name=self.get_job_name('hdr-format'),
            label='HDR format',
            precondition=self.make_precondition('hdr_format_job'),
            autodetect=self.autodetect_hdr_format,
            autofinish=True,
            options=(
                ('No', 'No'),
                ('HDR10', 'HDR10'),
                ('HDR10+', 'HDR10+'),
                ('Dolby Vision', 'DoVi'),
            ),
            **self.common_job_args(),
        )

    async def autodetect_hdr_format(self, _):
        for hdr_format, is_hdr_format in self.hdr_format_map.items():
            if is_hdr_format(self.release_name):
                _log.debug('Autodetected HDR format: %r', hdr_format)
                return hdr_format

    hdr_format_map = {
        'No': lambda release: release.hdr_format == '',
        'HDR10': lambda release: release.hdr_format == 'HDR10',
        'HDR10+': lambda release: release.hdr_format == 'HDR10+',
        'Dolby Vision': lambda release: release.hdr_format == 'DV',
    }

    @functools.cached_property
    def tags_job(self):
        return jobs.custom.CustomJob(
            name=self.get_job_name('tags'),
            label='Tags',
            precondition=self.make_precondition('tags_job'),
            prejobs=(
                self.imdb_job,
            ),
            worker=self.autodetect_tags,
            catch=(
                errors.RequestError,
            ),
            **self.common_job_args(),
        )

    async def autodetect_tags(self, _):
        json = await self._tracker.get_uhd_info(self.imdb_id)
        # Tags are comma-separated. We split them to get one tag per line, which
        # is easier on the eyes. Tags are interpreted as HTML because they may
        # contain entities like "&eacute;".
        tags = utils.html.as_text(json.get('tag', None)).split(',')
        _log.debug('Autodetected tags: %r', tags)
        return tags

    async def get_poster_from_tracker(self):
        await self.imdb_job.wait()
        json = await self._tracker.get_uhd_info(self.imdb_id)
        poster = json.get('photo', None)
        _log.debug('Poster from UHD: %r', poster)
        if poster:
            return {
                'poster': poster,
                'width': None,
                'height': None,
                'imghosts': (),
                'write_to': None,
            }

    @functools.cached_property
    def trailer_job(self):
        return jobs.custom.CustomJob(
            name=self.get_job_name('trailer'),
            label='Trailer',
            precondition=self.make_precondition('trailer_job'),
            prejobs=(
                self.imdb_job,
            ),
            worker=self.autodetect_trailer,
            catch=(
                errors.RequestError,
            ),
            **self.common_job_args(),
        )

    async def autodetect_trailer(self, _):
        json = await self._tracker.get_uhd_info(self.imdb_id)
        trailer_id = json.get('trailer', None)
        _log.debug('Autodetected trailer: %r', trailer_id)
        if trailer_id:
            return f'https://youtu.be/{trailer_id}'
        else:
            return ''

    @property
    def trailer_id(self):
        trailer_url = self.get_job_output(self.trailer_job, slice=0)
        if trailer_url:
            # Try to extract ID from trailer.
            if match := re.search('v=([a-zA-Z0-9_-]+)', trailer_url):
                return match.group(1)
            elif match := re.search('/([a-zA-Z0-9_-]+)$', trailer_url):
                return match.group(1)
            else:
                return trailer_url

    @functools.cached_property
    def description_job(self):
        return jobs.dialog.TextFieldJob(
            name=self.get_job_name('description'),
            label='Description',
            precondition=self.make_precondition('description_job'),
            prejobs=(
                self.upload_screenshots_job,
                self.mediainfo_job,
            ),
            text=self.generate_description,
            hidden=True,
            finish_on_success=True,
            read_only=True,
            **self.common_job_args(ignore_cache=True),
        )

    image_host_config = {
        'common': {'thumb_width': 350},
    }

    def generate_description(self):
        screenshot_tags = self._generate_description_screenshots()
        promotion_tag = (
            '[align=right][size=1]'
            f'Shared with [url={__homepage__}]{__project_name__}[/url]'
            '[/size][/align]'
        )

        # TODO: Include nfo?

        # TODO: Include mediainfo?

        return (
            f'[center]{screenshot_tags}[/center]'
            + '\n\n\n'
            + promotion_tag
        )

    def _generate_description_screenshots(self):
        assert self.upload_screenshots_job.is_finished
        return self.make_screenshots_grid(
            screenshots=self.upload_screenshots_job.uploaded_images,
            columns=2,
            horizontal_spacer='   ',
            vertical_spacer='\n\n',
        )

    release_name_translation = {
        'group': {
            re.compile(r'^NOGROUP$'): 'Unknown',
        },
    }

    @property
    def post_data(self):
        return {
            'submit': 'true',

            # "Movie" or "TV"
            'type': self.get_job_output(self.type_job, slice=0),

            # IMDb ID ("tt...")
            'imdbid': self.get_job_output(self.imdb_job, slice=0),

            # Original title
            'title': self.release_name.title,

            # English title
            'OtherTitle': self.release_name.title_aka,

            # Uploading Guide v2 says: "Disregard this field"
            'smalldesc': '',

            # Year
            'year': self.get_job_output(self.year_job, slice=0),

            # Season or `None` if it's a movie
            'season': (
                self.get_job_output(self.season_job, slice=0)
                if self.season_job else
                None
            ),

            # Quality (e.g. "1080p")
            'format': self.get_job_output(self.quality_job, slice=0),

            # Group
            'team': self.release_name.group,

            # Version (e.g. "Director's Cut")
            'Version': ' / '.join(self.get_job_output(self.version_job)),

            # Source ("Media" on the website) (e.g. "BluRay")
            'media': self.get_job_output(self.source_job, slice=0),

            # Codec (e.g. "x264")
            'codec': self.get_job_output(self.codec_job, slice=0),

            # HDR format (e.g. "HDR10" or "DoVi")
            'hdr': self.get_job_output(self.hdr_format_job, slice=0),

            # Tags
            'tags': ','.join(self.get_job_output(self.tags_job)),

            # Poster URL
            'image': self.get_job_output(self.poster_job, slice=0),

            # Trailer (YouTube ID)
            'trailer': self.trailer_id,

            # Mediainfo
            'mediainfo': self.get_job_output(self.mediainfo_job, slice=0),

            # Screenshots and release info
            'release_desc': self.get_job_output(self.description_job, slice=0),

            # Group with anything that has the same IMDB ID
            'auto_merge_group': 'on',

            # Internal release
            'internal': 'on' if self.options['internal'] else None,

            # No support for exclusive releases (this is intentional)
            # 'exclude': '0',

            # 3D version
            'd3d': '1' if self.options['3d'] else None,

            # Release contains Vietnamese Audio dub
            'vie': '1' if self.options['vie'] else None,

            # Scene release
            'scene': '1' if self.get_job_attribute(self.scene_check_job, 'is_scene_release') else None,

            # Upload anonymously
            'anonymous': '1' if self.options['anonymous'] else None,
        }

    @property
    def post_files(self):
        return {
            'file_input': {
                'file': self.torrent_filepath,
                'mimetype': 'application/x-bittorrent',
            },
        }
