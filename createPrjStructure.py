import os, sys
import hou
import re
import tempfile

#full os path to the root of the project directory
directory=['cache', 'geo', 'ifd', 'images', 'pclouds', 'textures', 'shadows']
''' create project structure in HIP directory'''
def createProjectStructure():
    #Get full qualificated file name
    p = hou.hipFile.path()

    if len(p) == 0:
        hou.ui.displayMessage('hipFile is invalid', buttons=('Ok',))
        return
    pattern = re.compile('([^/]*$)')
    if re.search(pattern, p):
        name = re.search(pattern, p).group(1)
        path = p.replace(name, '')
    for dir in directory:
        wdir = os.path.join(path, dir)
        print 'create path is: %s' % wdir
        if not os.path.exists(wdir):os.mkdir(wdir)
    hou.ui.displayMessage('Directory project''s structure was successfully created in the directory %s' % path, buttons=('Ok',))

def HDA_addVersion(threshold = 10):
    if hou.ui.displayMessage('Are you shure you want to create a snew version of HDA?', buttons=("Yes", "No")) == 1:
        print 'The creation new HDA cancelled.'
        return None

    checkFork = False
    checkLock = False
    tempHDAPath = ''
    tempPath = ''

    selected_nodes = hou.selectedNodes()
    if not selected_nodes:
        hou.ui.displayMessage('Please select HDA node', buttons=("Ok",))
    else:
        for node in selected_nodes:
            hdaDef = node.type().definition()
            if hdaDef:
                libPath = hdaDef.libraryFilePath()
                pattern = re.compile('([^/]*$)')
                if re.search(pattern, libPath):
                    hdaFileName = re.search(pattern, libPath).group(1)
                    hdaDirPath = libPath.replace(hdaFileName, '')
                    hdaName = hdaFileName.replace('.otl', '')
                    hdaNameComponents = hdaName.split('_')
                    #check lenght
                    if len(hdaNameComponents) != 6:
                        print 'Unfortunalety, you have not the correct name of asset'
                        print 'You can not create new version of the asset'
                        continue
                    # [0] prefix [1] name [2] fork ver  [3] major ver [4] minor ver [5] work ver
                    if hdaNameComponents[5].isdigit():
                        workVersion = int(hdaNameComponents[5])
                    else:workVersion = None

                    if hdaNameComponents[4].isdigit():
                        minorVersion = int(hdaNameComponents[4 ])
                    else:minorVersion = None

                    majorVersion = hdaNameComponents[3].replace('v', '')
                    if majorVersion.isdigit():
                        majorVersion = int(majorVersion)
                    else:majorVersion = None
                    forkVersion = hdaNameComponents[2].replace('f','')
                    if not forkVersion.isdigit():
                        forkVersion = None
                    else:
                        forkVersion = int(forkVersion)

                    if(forkVersion != None) and (minorVersion != None) and (majorVersion != None) and (workVersion != None):
                        #check fork
                        if forkVersion != 0:
                            if hou.ui.displayMessage("You HDA has a fork. Do you want to continue?", buttons=("Yes", "No")) == 0:
                                print "The creation the new version HDA %s was skipped." % hdaName
                                continue

                        tupleofValid = HDA_getValidVersion(forkVersion, hdaDirPath, hdaNameComponents, majorVersion,
                                                           minorVersion, threshold, workVersion)
                        #warning of the chance of forking
                        warningFork = tupleofValid[1]
                        if warningFork > 0:
                            if hou.ui.displayMessage("You HDA will have a fork.Do you want to continue?", buttons=("Yes", "No")) == 0:
                                print "The creation the new version HDA %s was skipped." % hdaName
                                continue
                        newLibPath = tupleofValid[0]
                        #check lock
                        if HDA_IsUnlockedAsset(node):
                            tempPath =  tempfile.mktemp().replace('\\','/')
                            tempHDAPath = '%s_%s' % (tempPath, hdaFileName)
                            #save temp HDA
                            hdaDef.save(str('%s' % tempHDAPath), node)
                            #import again and set definition
                            hou.hda.installFile(str(tempHDAPath), None, False, True)
                            #clear definition preference
                            hdaDef = node.type().definition()
                            hdaDef.serIsPreferred(False)
                            checkLock = True
                        #Copy HDA
                        hdaDef.copyToHDAFile(str(newLibPath))
                        #import again and set definition
                        hou.hda.installFile(str(newLibPath), None, False, True)
                        #clear definition preference
                        hdaDef = node.type().definition()
                        hdaDef.serIsPreferred(False)
                        #REmove temp HDA or unlock HDA for edit
                        if checkLock:
                            hou.hda.uninstallFile(str(tempHDAPath))
                            try:
                                os.remove(tempHDAPath)
                            except:
                                print 'The operation was not completed successfully. Cannot delete file.'

                        else:
                            node.allowEditingOfContens()

                        #info
                        print 'The operation completed successfully.'
                        print 'The new version is here: %s' % (newLibPath)

                        #
                    else:
                        print 'Unfortunatly, you have not the correct name of HDA: %s' % (hdaName)
                        print 'The new version will not be created.'
            else:
                hou.ui.displayMessage('Please, select root of HDA node(s)', buttons=('Ok',))
                continue


def HDA_IsUnlockedAsset(node):
    #This function returneds True when HDA is unlock
    return not node.isLocked() and node.type().definition() is not None

def HDA_getValidVersion(threshold, hdaDirPath, prefixName, label, forkVersion,  majorVersion, minorVersion, workVersion):
    #THis function works in two modes. Firstly, if fork == 0 - it will return the correct file name or will recursion,
    #that creates a fork. If the fork > 0 it is the simple increase in the fork. The name remains the same version.

    res = ''
    new_WorkVersion = workVersion
    new_minorVersion = minorVersion
    new_majorVersion = majorVersion
    if forkVersion == 0:
        if (workVersion + 1 >= threshold ):
            new_WorkVersion = 0
            if (minorVersion + 1 >= threshold):
                new_minorVersion = 0
                new_majorVersion += 1
            else:
                new_minorVersion += 1
        else:
            new_WorkVersion += 1

    filePath = '%s%s_%s_f%s_v%s_%s_%s.otl' % (hdaDirPath, prefixName, label, forkVersion, new_majorVersion, new_minorVersion, new_WorkVersion)
    checkFile = os.path.exists(filePath)
    if not checkFile:
        return filePath, forkVersion
    else:
        forkVersion += 1
        res = HDA_getValidVersion(threshold, hdaDirPath, prefixName, label, forkVersion, majorVersion, minorVersion, workVersion)
    return res

if(__name__ == '__main__'):
    createProjectStructure()
    exit()
    if os.environ.has_key('HIP'):
        print 'current HIP variable is: %s' % os.environ['HIP']

    HDA_addVersion()