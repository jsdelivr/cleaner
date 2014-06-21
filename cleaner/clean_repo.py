import git, logging, os
import subprocess, shlex, yaml

from cleaner.utils import group
from cleaner import Cleaner

class Clean_Repo(Cleaner):
    """
    Cleans matched files in a git repo and commits them
    Assumes git config set with required privs for pushing
    """
    branch = "master"
    remote = "origin"
    automatically_push = True
    commit_msg = "Automatic cleaning since {hexsha}"

    def __init__(self, config={}):
        Cleaner.__init__(self, config)
        self.repo = git.Repo(self.cwd)
        self.remote = getattr(self.repo.remotes, self.remote) #or remote/whatev

    def before_clean(self):
        self.repo.git.checkout(self.branch)
        logging.info("Checked out %s branch", self.branch)
        #pull latest version of repo
        self.pull()

    def _clean(self, path, catch=False):
        self.before_clean()
        # mods = clean_task(path=path, exclude=self.exclude_pattern, cwd=self.cwd, minsize=self.min_file_size)
        # if len(mods) > 0:
        #     self.commit(mods)
        # else:
        #     logging.info("No staged commits after checking path; continuing...")

        self.kill_history(path) #needs to be applied after the commits
        self.post_clean()

    def pull(self):
        self.last_seen_commit = self.repo.head.commit
        self.remote.pull()

    def commit(self, changed):
        """
        Commit our changes
        I don't think we have to worry about pottential merge conflicts as the files we change are suppose
        to be stable
        """
        index = self.repo.index

        #as changed adds the cwd and sometimes "/" we have to adjust it as gitpython wants it relative to the repo
        cwdlen = len(self.cwd)
        if not self.cwd.endswith("/"):
            cwdlen += 1
        changed = [change[cwdlen:] for change in changed]

        # this is a little dirty but gitpython is a bit finicky with adding more than a couple thousand files at a time
        def add(files):
            for items in group( int(max(min(1000, len(files)/2.0), 1)), files):
                try:
                    index.add(items)
                except:
                    if len(items) > 1:
                        add(items)
                    else:
                        logging.error("Could not add file %s for some reason......", items[0])

        logging.info("Begining to git add %d items. This may take a while...", len(changed))
        add(changed)

        last = self.last_seen_commit
        #see http://pythonhosted.org/GitPython/0.3.1/reference.html#module-git.objects.commit for extensions
        data = {
            "hexsha": last.hexsha,
            "author": str(last.author),
            "summary": last.summary,
            "message": last.message,
            "changed": changed
        }
        logging.info("Committing changes")
        index.commit( self.commit_msg.format(**data) ) #, parent_commits=(last.hexsha)
        if self.automatically_push:
            logging.info("Pushing changes to remote")
            self.remote.push()
        else:
            logging.info("Changes committed but not pushed...")

    destroy_commits = "" #for instance HEAD~5

    def kill_history(self, path):
        """
            Essentially just an automation of https://github.com/zuha/Zuha/wiki/Git-Reduce-Repo-Size
        """
        commands = []
        anticwd = (os.path.abspath("") + "\\").replace("\\", "/") #help shell

        hist_script = yaml.load(open("cleaner/kill_history.yml"))
        for cmd in hist_script: #format the commands
            last = None
            for p in path:
                c = cmd.copy()
                c["command"] = cmd["command"].format(path=p, anticwd=anticwd, cwd=self.cwd)
                if last == c:
                    break
                else:
                    last = c
                    commands.append(c)

        for cmd in commands: #now run em
            try:
                logging.info("Running command: '%s' in %s", cmd["command"], self.cwd)
                process = subprocess.Popen(shlex.split(cmd["command"]), cwd=self.cwd)
                process.wait() #wait for command to finish executing
            except Exception, e:
                if "catch_exception" not in cmd or not cmd["catch_exception"]:
                    raise e
