import GUIDetection.RectUtils.RectUtil
from KNNAlgo.Utils.Node import *
from KNNAlgo.Utils.NodeUtils import *
import os
from GUIDetection.procAppScreenshot import *
from KNNAlgo.Utils.HierarchyUtil import *
MINED_DIR = r'C:\Users\86134\Desktop\autotest_tool\ReDraw-Final-Google-Play-Dataset'

MAX_AGGREGATE_DEPTH = 3


def canAggregate(inputNodes, lastNodeCnt):
    print(f'unmatched input nodes is {len(inputNodes)}')
    if len(inputNodes) == 0:
        return False
    if len(inputNodes) == lastNodeCnt:
        # no more aggragate
        return False
    return True

def unionRectAreaRate(rect1, rect2):
    x1, y1 = rect1.x, rect1.y

    x2, y2 = rect2.x, rect2.y

    dx1, dy1 = x1 + rect1.width, y1 + rect1.height
    dx2, dy2 = x2 + rect2.width, y2 + rect2.height
    ox1, oy1 = x1 + rect1.width/2, y1 + rect1.height/2
    ox2, oy2 = x2 + rect2.width/2, y2 + rect2.height/2
    if abs(ox2-ox1) <= (rect1.width/2 + rect2.width/2) and abs(oy2-oy1) <= (rect1.height/2+rect2.height/2):
        cx = max(x1,x2)
        cy = max(y1,y2)
        ex = min(dx1, dx2)
        ey = min(dy1, dy2)
        union = abs(cx-ex) * abs(cy-ey)
        total = rect1.area() + rect2.area() - union

        return union / total
    else:
        return 0


def matchScore(inputNodes, targetNode):
    # match componet has best IOU score, so the implements is shown as below
    targetLeafNodes = leafNode(targetNode)

    unionAreas = 0
    for inputNode in inputNodes:
        bestUnionRate = 0
        for targetNode in targetLeafNodes:
            tmpUnion = unionRectAreaRate(inputNode.rect, targetNode.rect)
            assert tmpUnion <= 1
            if tmpUnion > bestUnionRate:
                 bestUnionRate  = tmpUnion
        unionAreas += bestUnionRate
    return unionAreas / len(inputNodes)



def containsAnyInputNodes(aContainer, inputNodes):
    conInputNodes = []
    for inputNode in inputNodes:
        if aContainer.contains(inputNode):
            conInputNodes.append(inputNode)
    return conInputNodes

def aggragate(inputGUINode):
    containerList = []
    inputNodes = inputGUINode.children
    lastNodeCnt = -1
    while canAggregate(inputNodes, lastNodeCnt):
        lastNodeCnt = len(inputNodes)
        score = 0
        matchXmlPath = ''
        matchImgPath = ''
        matchHierarchy = None
        for root, dirs, files in os.walk(MINED_DIR):
            for file in files:
                if file[0] != '.' and file.endswith('.xml'):
                    filename, ext = os.path.splitext(file)
                    suffix = filename.split('_')[-1]
                    assert ext == '.xml'
                    imgPath =os.path.join(root, 'screenshot_' + suffix+ '.png')
                    xmlPath = os.path.join(root,file)
                    # print(imgPath)
                    parser = XmlParser(xmlPath)
                    hierarchy = parser.getHierarchy()
                    tmpScore = matchScore(inputNodes, hierarchy)
                    if(tmpScore >= score):
                        score = tmpScore
                        matchXmlPath = xmlPath
                        matchImgPath = imgPath
                        matchHierarchy = hierarchy

        print(f'matched screenshot {matchImgPath}')
        screen_img = cv2.imread(matchImgPath)
        # showImage(img)

        # use hierarchy to aggregate
        containerTarget = containerNode(matchHierarchy)
        containerTarget = sorted(containerTarget, key=lambda x: x.dep, reverse= True)

        for container in containerTarget:
            containsNodes = containsAnyInputNodes( container, inputNodes)
            if(len(containsNodes) != 0):

                print(f'matched container type {container.classType}')

                # resizeRect = findBoundOfNode(containsNodes)
                # resizeRect = expandPx(resizeRect, px = 20)
                resizeRect = container.rect
                node = GUINode(rect=resizeRect)
                node.classType = container.classType
                node.dep = containsNodes[0].dep
                for containNode in containsNodes:
                    inputNodes.remove(containNode)
                    containNode.dep +=1
                    containNode.parent = node
                node.children.extend(containsNodes)
                containerList.append(node)
                showSelectedScreenLeafNodesAndTargetLayout(screen_img, matchHierarchy, container)
                break
        # sorted target here
    inputGUINode.children = inputNodes
    inputGUINode.children.extend(containerList)
    return inputGUINode
