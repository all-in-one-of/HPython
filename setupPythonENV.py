import os, sys

DEFAULT_PATH_TO_PYTHON_HOUDINI = 'C:\Houdini\15.0.326\python27'
DEFAULT_PATH_TO_PYTHON_SYSTEM = 'C:\Houdini\15.0.326\python27'
os.environ['PYTHONPATH'] = os.path.pathsep.join([r'C:\Houdini\15.0.326\houdini\python2.7libs'])
sys.path.append(r'C:\Houdini\15.0.326\houdini\python2.7libs')