import shutil, errno, os

def copy(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc: # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else: raise

def merge(src_dir, dest_dir):
	#http://stackoverflow.com/questions/7419665/python-move-and-overwrite-files-and-folders
	for src_dir, dirs, files in os.walk(src_dir):
	    dst_dir = src_dir.replace(src_dir, dest_dir)
	    if not os.path.exists(dst_dir):
	        os.mkdir(dst_dir)
	    for file_ in files:
	        src_file = os.path.join(src_dir, file_)
	        dst_file = os.path.join(dst_dir, file_)
	        if os.path.exists(dst_file):
	            os.remove(dst_file)
	        shutil.move(src_file, dst_dir)