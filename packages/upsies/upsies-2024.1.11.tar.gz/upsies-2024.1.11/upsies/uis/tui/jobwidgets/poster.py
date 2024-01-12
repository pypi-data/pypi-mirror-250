import functools

from .... import utils
from . import JobWidgetBase

import logging  # isort:skip
_log = logging.getLogger(__name__)


class PosterJobWidget(JobWidgetBase):

    is_interactive = False

    def setup(self):
        self.job.signal.register('obtaining', self.handle_obtaining)
        self.job.signal.register('downloading', self.handle_downloading)
        self.job.signal.register('resizing', self.handle_resizing)
        self.job.signal.register('uploading', self.handle_uploading)
        self.job.signal.register('uploaded', self.handle_uploaded)

    def handle_obtaining(self):
        self.job.info = 'Searching'

    def handle_downloading(self, url):
        self.job.info = f'Downloading {url}'

    def handle_resizing(self, filepath):
        self.job.info = f'Resizing {utils.fs.basename(filepath)}'

    def handle_uploading(self, imghost):
        self.job.info = f'Uploading to {imghost.name}'

    def handle_uploaded(self, url):
        self.invalidate()

    @functools.cached_property
    def runtime_widget(self):
        return None
