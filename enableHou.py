import sys, os

    # Importing hou will load in Houdini's libraries and initialize Houdini.
    # In turn, Houdini will load any HDK extensions written in C++.  These
    # extensions need to link against Houdini's libraries, so we need to
    # make sure that the symbols from Houdini's libraries are visible to
    # other libraries that Houdini loads.  So, we adjust Python's dlopen
    # flags before importing hou.
'''#'''
HOUDINI_MAJOR_RELEASE = '15'
HOUDINI_MINOR_RELEASE = '0'
HOUDINI_BUILD_VERSION = '326'


#
HOUDINI_INSTALL_PATH = 'c:/Houdini/'
HOUDINI_BUILD_PREFIX = ''
HOUDINI_BUILD = '%s%s.%s.%s' % (HOUDINI_BUILD_PREFIX, HOUDINI_MAJOR_RELEASE, HOUDINI_MINOR_RELEASE, HOUDINI_BUILD_VERSION)
HFS = '%s%s'%(HOUDINI_INSTALL_PATH, HOUDINI_BUILD)
os.environ['HFS'] = HFS

if hasattr(sys, "setdlopenflags"):
    old_dlopen_flags = sys.getdlopenflags()
    import DLFCN
    sys.setdlopenflags(old_dlopen_flags | DLFCN.RTLD_GLOBAL)

try:
    import hou
except ImportError:
        # Add $HFS/houdini/python2.7libs to sys.path so Python can find the
        # hou module.
    sys.path.append(os.environ['HFS'] + "/houdini/python%d.%dlibs" % sys.version_info[:2])
    print os.environ['HFS'] + "/houdini/python%d.%dlibs" % sys.version_info[:2]
    import hou
finally:
    if hasattr(sys, "setdlopenflags"):
        sys.setdlopenflags(old_dlopen_flags)

