import logging
from cleaner.utils.clean_task import clean_task

class Cleaner():
    """
    Cleans matched files in a git repo and commits them
    Assumes git config set with required privs for pushing
    """
    exclude_pattern = ["*.ini"]
    general_pattern = ["**"]
    cwd = "" #wherever this project is relative to the repo
    min_file_size = 10

    def __init__(self, config={}):
        #set attributes from config
        for k,v in config.iteritems():
            if v is not None:
                setattr(self, k, v)

    def before_clean(self):
        pass

    def _clean(self, path, catch):
        self.before_clean()
        mods = clean_task(path=path, exclude=self.exclude_pattern, cwd=self.cwd, minsize=self.min_file_size,catch=catch)
        self.post_clean()

    def clean(self, files, catch=False):
        self._clean(files, catch)

    def cleanAll(self, catch=False):
        self._clean(self.general_pattern, catch)

    def post_clean(self):
        pass
