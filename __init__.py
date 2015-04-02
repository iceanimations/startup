import nuke
import os.path as osp
import subprocess

openLoc = '''
import subprocess
command = 'explorer %s'
print command
subprocess.call(command)
'''

def readNode():
    node = nuke.thisNode()
    path = node.knob('file').getValue()
    if path:
        path = osp.dirname(path).replace('/', '\\\\')
    node.addKnob(nuke.PyScript_Knob('openLoc', 'Open Location', openLoc%path))

def setupNuke():
    nuke.addOnCreate(readNode, nodeClass='Read')
    
def getBackdrop():
    node = nuke.selectedNode()
    if node:
        bds = nuke.allNodes('BackdropNode')
        if bds:
            for bd in bds:
                if node in bd.getNodes():
                    return bd
nuke.getBackdrop = getBackdrop