import git

from cleaner.utils.clean_task import clean_task


class Clean_Repo():
    """
    Cleans matched files in a git repo and commits them
    Assumes git config set with required privs for pushing
    """
    exclude_pattern = ['*.ini']
    cwd = "repo" #wherever this project is relative to the repo
    branch = "master"

    #see pythonhosted.org/GitPython/0.3.1/tutorial.html#the-commit-object
    commit_msg = "Automatic cleaning since {hexsha}"

    def __init__(self):
        self.repo = git.Repo(self.cwd)
        self.remote = self.repo.remotes.origin #or remote/whatev

    def before_clean(self):
        self.repo.checkout(self.branch)
        #pull latest version of repo
        self.pull()

    def _clean(self, *args, **kwargs):
        self.before_clean()
        mods = clean_task(*args, **kwargs)
        self.commit(mods)
        self.post_clean()

    def clean(self, files):
        self._clean(path=files, exclude=self.exclude_pattern, cwd=self.cwd)

    def cleanAll(self):
        self._clean(path=["files/*/**"], exclude=self.exclude_pattern, cwd=self.cwd)

    def post_clean(self):
        pass

    def pull(self):
        self.last_seen_commit = repo.head.commit
        self.remote.pull()

    def commit(self, changed):
        """
        Commit our changes
        I don't think we have to worry about pottential merge conflicts as the files we change are suppose
        to be stable
        """
        index = self.repo.index
        index.add(changed)
        commit = index.commit(self.commit_msg.format(self.last_seen_commit))
        self.remote.push()
