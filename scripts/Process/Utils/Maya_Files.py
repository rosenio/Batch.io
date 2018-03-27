import os

def recursive_glob(rootdir='.', suffix=''):
    return [os.path.join(looproot, filename)
            for looproot, _, filenames in os.walk(rootdir)
            for filename in filenames if (filename.endswith(suffix) and not 'incrementalSave' in looproot)]