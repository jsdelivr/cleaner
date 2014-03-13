#requires python > 2.5 or so i think for glob

import os
from glob import glob
from fnmatch import fnmatch

def clean_task(path=[], exclude=[], cwd="", minsize=10):
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

    for path in pathes:
        if any( fnmatch(path, x) for x in exclude ):
            continue
        #current path dont match exclude filter we're good to start wreckin havoc
        try:
            if os.path.getsize(path) > minsize:
                open(path, 'w').close() #empty the file
                modified.append(path)
        except OSError:
            pass #what do?

    return modified