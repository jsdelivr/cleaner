#requires python > 2.5 or so i think for glob
import os, logging
from glob2 import glob
from fnmatch import fnmatch

def clean_task(path=[], exclude=[], cwd="", minsize=10,catch=False):
    """
    Start cleaning in the given path

    path    -- Array of paths or string path to clean (changed files)
    exclude -- Array of filters to exclude
    minsize -- minimum size of a file in bytes before we attempt compressing
    """

    #wrap it up
    if type(path) == str:
        path = [path]
    
    if type(cwd) == str:
        if not cwd.endswith("/"):
            cwd += "/"
        path = [cwd+x for x in path]

    #resolve to a list of target pathes
    pathes = [item for some_path in map(glob, path) for item in some_path]

    modified = []

    logging.info("Checking the dirty %d files", len(pathes))

    for path in pathes:
        # not file or matches an exclude pattern
        if not os.path.isfile(path) or any( fnmatch(path, x) for x in exclude ):
            continue
        #current path dont match exclude filter we're good to start wreckin havoc
        try:
            if os.path.getsize(path) > minsize:
                open(path, 'w').close() #empty the file
                modified.append(path)
                logging.debug("Nullified " + path)
        except OSError, e:
            if not catch:
                raise e

    return modified