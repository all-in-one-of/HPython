import os
import sys
import subprocess
import encodings.aliases
import setupConstants


def printInfo():
    print(os.environ['HOUDINI_TOOLBAR_PATH'])
    print 'HOUDINI_SCRIPT_PATH: %s' % os.environ['HOUDINI_SCRIPT_PATH']
    print 'HOUDINI_DSO_PATH: %s' % os.environ['HOUDINI_DSO_PATH']
    print 'HOUDINI_VEX_PATH: %s' % os.environ['HOUDINI_VEX_PATH']
    print 'HOUDINI_OTLSCAN_PATH: %s' % os.environ['HOUDINI_OTLSCAN_PATH']
    print 'HOUDINI_GALLERY_PATH: %s' % os.environ['HOUDINI_GALLERY_PATH']
    print 'HOUDINI_UI_ICON_PATH: %s' % os.environ['HOUDINI_UI_ICON_PATH']
    print 'HOUDINI_PATH: %s' % os.environ['HOUDINI_PATH']
    print 'PATH: %s' % os.environ['PATH']
    print 'Name is %s' % __name__
    parsePathVariable()


def printencoding():
    arr = encodings.aliases.aliases
    keys = list(arr.keys())
    keys.sort()
    for key in keys:
        print '%s => %s' % (key, arr[key])


def parsePathVariable():
    l = os.environ['PATH']
    paths = l.split(os.pathsep)
    for el in paths:
        print el

def getEnvironment():
    for i in os.environ.keys():
        print 'key %s is: %s ' % (i, os.environ.get(i))



def enableHouModule():
    '''Set up the environment so that "import hou" works.'''
    import sys, os

    # Importing hou will load in Houdini's libraries and initialize Houdini.
    # In turn, Houdini will load any HDK extensions written in C++.  These
    # extensions need to link against Houdini's libraries, so we need to
    # make sure that the symbols from Houdini's libraries are visible to
    # other libraries that Houdini loads.  So, we adjust Python's dlopen
    # flags before importing hou.
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
        import hou
    finally:
        if hasattr(sys, "setdlopenflags"):
            sys.setdlopenflags(old_dlopen_flags)


'''#run application'''
if __name__ ==  '__main__':
    setupConstants()
    getEnvironment()
    startpath = ['%s/hmaster' % setupConstants.HB] + sys.argv[1:]
    #enableHouModule()
    printInfo()
    subprocess.Popen(startpath)
