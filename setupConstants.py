import os

def setupConstants():
    global HB
    '''#'''
    HOUDINI_MAJOR_RELEASE = '15'
    HOUDINI_MINOR_RELEASE = '0'
    HOUDINI_BUILD_VERSION = '326'
    #
    HOUDINI_INSTALL_PATH = 'c:\Houdini\\'
    HOUDINI_PROD_PATH = r'i:\HoudiniProjects'
    HOUDINI_BUILD_PREFIX = ''
    HOUDINI_BUILD = '%s%s.%s.%s' % (
    HOUDINI_BUILD_PREFIX, HOUDINI_MAJOR_RELEASE, HOUDINI_MINOR_RELEASE, HOUDINI_BUILD_VERSION)
    '''#The path where houdini was installed'''
    HFS = '%s%s' % (HOUDINI_INSTALL_PATH, HOUDINI_BUILD)
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
    os.environ['HOUDINI_TOOLBAR_PATH'] = os.path.pathsep.join(
            ['%s/toolbar' % HOUDINI_PROD_PATH, '@/toolbar', '%s/toolbar' % QLIB, '@/toolbar'])
    '''#The path of directories where HOUDINI searhes for scripts'''
    os.environ['HOUDINI_SCRIPT_PATH'] = os.path.pathsep.join(
            ['%s/scripts' % HOUDINI_PROD_PATH, '@/scripts', '%s/scripts' % QLIB, '@/scripts'])
    '''#The path of directories where HOUDINI searhes for custom plugins'''
    os.environ['HOUDINI_DSO_PATH'] = os.path.pathsep.join(['%s/dso' % HOUDINI_PROD_PATH, '@/dso'])
    '''#The search path of directories where HOUDINI searhes for vex code'''
    os.environ['HOUDINI_VEX_PATH'] = os.path.pathsep.join(['%s/vex/^' % HOUDINI_PROD_PATH, '.', '@/vex/^'])
    '''#The path of directories where HOUDINI searhes for otl files'''
    os.environ['HOUDINI_OTLSCAN_PATH'] = os.path.pathsep.join(
            ['%s/otls' % HOUDINI_PROD_PATH, '@/otls', '%s/base' % QOTL, '%s/future' % QOTL, '%s/experimental' % QOTL,
             '@/otls'])
    # The path of directories where HOUDINI searhes for gallery files
    os.environ['HOUDINI_GALLERY_PATH'] = os.path.pathsep.join(
            ['%s/gallery' % HOUDINI_PROD_PATH, '@/gallery', '%s/gallery' % QLIB, '@/gallery'])
    # The path of directories where HOUDINI searhes for icon files
    os.environ['HOUDINI_UI_ICON_PATH'] = os.path.pathsep.join(['%s/icon' % HOUDINI_PROD_PATH, '@/^'])
    # The path of directories where HOUDINI searhes for configuration files
    os.environ['HOUDINI_PATH'] = os.path.pathsep.join(['%s/' % HOUDINI_PROD_PATH, '&', '%s' % HTOA])
    # disable license script
    os.environ['HOUDINI_SCRIPT_LICENSE'] = 'hescape'