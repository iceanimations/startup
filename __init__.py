import nuke
import os.path as osp
import subprocess
from site import addsitedir as asd

asd('R:/Python_Scripts/Nuke')
import createArchive
reload(createArchive)

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
    knobName = 'openLoc'
    if knobName not in nuke.Node.knobs(node):
        node.addKnob(nuke.PyScript_Knob(knobName, 'Open Location', openLoc%path))

def setupNuke():
    nuke.addOnCreate(readNode, nodeClass='Read')
    createArchive.setupNuke()
    
def getBackdrop():
    node = nuke.selectedNode()
    if node:
        bds = nuke.allNodes('BackdropNode')
        if bds:
            for bd in bds:
                if node in activateBackdrop(bd, False):
                    return bd
                
def activateBackdrop(node, select=True):
    nodes = []
    xmin = node.knob('xpos').value()
    xmax = xmin + node.knob('bdwidth').value()
    ymin = node.knob('ypos').value()
    ymax = ymin + node.knob('bdheight').value()
    node.knob('selected').setValue(True)
    for i in [i for i in nuke.allNodes() if i is not node]:
        ixmin = i.knob('xpos').value()
        ixmax = ixmin + i.screenWidth()
        iymin =  i.knob('ypos').value()
        iymax = iymin + i.screenHeight()
        if (ixmin >= xmin and ixmax < xmax) and (iymin >= ymin and iymax < ymax):
            nodes.append(i)
            if select:
                i.knob('selected').setValue(True)
            else:
                node.setSelected(False)
    return nodes

nuke.getBackdrop = getBackdrop
nuke.activateBackdrop = activateBackdrop