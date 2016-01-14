import os
import sys
import subprocess
import encodings.aliases


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


'''#'''
HOUDINI_MAJOR_RELEASE = '15'
HOUDINI_MINOR_RELEASE = '0'
HOUDINI_BUILD_VERSION = '326'


#
HOUDINI_INSTALL_PATH = 'c:\Houdini\\'
HOUDINI_PROD_PATH = r'i:\HoudiniProjects'

HOUDINI_BUILD_PREFIX = ''
HOUDINI_BUILD = '%s%s.%s.%s' % (HOUDINI_BUILD_PREFIX, HOUDINI_MAJOR_RELEASE, HOUDINI_MINOR_RELEASE, HOUDINI_BUILD_VERSION)

'''#The path where houdini was installed'''

HFS = '%s%s'%(HOUDINI_INSTALL_PATH, HOUDINI_BUILD)
os.environ['HFS'] = HFS

'''setup path location'''

HB = HFS + '\BIN'
os.environ['PATH'] = os.path.pathsep.join([HB, os.environ['PATH']])

'''#setup QLIB library'''
QLIB = 'i:/qlib'
QOTL = QLIB + '/otls'
HTOA = 'C:/htoa/htoa-1.8.0_r1522_houdini-15.0.179.25/htoa-1.8.0_r1522_houdini-15.0.179.25'
ARNOLD_PATH = 'C:/htoa/htoa-1.8.0_r1522_houdini-15.0.179.25/htoa-1.8.0_r1522_houdini-15.0.179.25/scripts/bin'
os.environ['PATH'] = os.path.pathsep.join([ARNOLD_PATH, os.environ['PATH']])
os.environ['PATH'] = os.path.pathsep.join([HFS, os.environ['PATH']])

'''#setup houdini path variables
#The search path for factory and custom shelves and shelf tools'''
os.environ['HOUDINI_TOOLBAR_PATH'] = os.path.pathsep.join(['%s/toolbar' % HOUDINI_PROD_PATH, '@/toolbar', '%s/toolbar' % QLIB,'@/toolbar'])

'''#The path of directories where HOUDINI searhes for scripts'''
os.environ['HOUDINI_SCRIPT_PATH'] = os.path.pathsep.join(['%s/scripts' % HOUDINI_PROD_PATH, '@/scripts', '%s/scripts'%QLIB, '@/scripts'])

'''#The path of directories where HOUDINI searhes for custom plugins'''
os.environ['HOUDINI_DSO_PATH'] = os.path.pathsep.join(['%s/dso' % HOUDINI_PROD_PATH, '@/dso'])

'''#The search path of directories where HOUDINI searhes for vex code'''
os.environ['HOUDINI_VEX_PATH'] = os.path.pathsep.join(['%s/vex/^' % HOUDINI_PROD_PATH, '.', '@/vex/^'])

'''#The path of directories where HOUDINI searhes for otl files'''
os.environ['HOUDINI_OTLSCAN_PATH'] = os.path.pathsep.join(['%s/otls' % HOUDINI_PROD_PATH, '@/otls', '%s/base' % QOTL, '%s/future' % QOTL, '%s/experimental' % QOTL, '@/otls'])

#The path of directories where HOUDINI searhes for gallery files
os.environ['HOUDINI_GALLERY_PATH']=os.path.pathsep.join(['%s/gallery'%HOUDINI_PROD_PATH, '@/gallery', '%s/gallery'%QLIB, '@/gallery'])

#The path of directories where HOUDINI searhes for icon files
os.environ['HOUDINI_UI_ICON_PATH']=os.path.pathsep.join(['%s/icon'%HOUDINI_PROD_PATH, '@/^'])

#The path of directories where HOUDINI searhes for configuration files
os.environ['HOUDINI_PATH']=os.path.pathsep.join(['%s/'%HOUDINI_PROD_PATH, '&', '%s'%HTOA])

#disable license script
os.environ['HOUDINI_SCRIPT_LICENSE'] = 'hescape'



'''#run application'''
if __name__ ==  '__main__':
    getEnvironment()
    startpath = ['%s/hmaster' % HB] + sys.argv[1:]
    #enableHouModule()
    printInfo()
    subprocess.Popen(startpath)
