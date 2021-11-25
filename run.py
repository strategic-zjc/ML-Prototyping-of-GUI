import copy

from GUIDetection.procAppScreenshot import *
from CNNClassifier.classifier import *
from KNNAlgo.Utils.Node import *
from KNNAlgo.Utils.NodeUtils import *
from KNNAlgo.Aggregate import *


def drawHierarchy(img, rootNode):
    imgC = copy.deepcopy(img)
    for child in rootNode.children:
        drawGUIBoundingRectLeaf(imgC, child)
    for child in rootNode.children:
        drawGUIBoundingRectContainer(imgC,child)
    showImageId(imgC, 'hierarchy')
def drawGUIBoundingRectLeaf(img, node):
    children = node.children
    if len(children) == 0:
        ImageUtil.drawRect(img, node.rect, ColorUtil.cColortoInt(CColor.Red))
    for child in children:
        drawGUIBoundingRectLeaf(img, child)
def drawGUIBoundingRectContainer(img, node):
    children = node.children
    if len(children) != 0:
        ImageUtil.drawRect(img, node.rect, ColorUtil.cColortoInt(CColor.Green), thickness= 3)
    for child in children:
        drawGUIBoundingRectContainer(img, child)


def runApplication(filePath):
    compon = processScreenshot(filePath)
    img_color = cv2.imread(filePath)
    GUINodes = rectViewsToNodes(compon, img_color)
    rect = Rect(0,0,img_color.shape[1], img_color.shape[0])
    Node = GUINode(rect = rect)
    Node.children.extend(GUINodes)
    rootNode = aggragate(Node)
    drawHierarchy(img_color, rootNode)
    # following is more detailed implementation which generates codes, utilizing ocr to detect text and
    # and uses class type to create a runnable project....
    # left to implement.......

if __name__ == '__main__':
    # filename = r'C:\Users\86134\Desktop\autotest_tool\ML_GUI_Prototype\screenshot\com.crunchyroll.crmanga_1.png'
    # filename = r'C:\Users\86134\Desktop\autotest_tool\ML_GUI_Prototype\screenshot\com.dropbox.android_2.png'
    # filename = r'C:\Users\86134\Desktop\autotest_tool\ML_GUI_Prototype\screenshot\com.amazon.mShop.android.shopping_2.png'
    # filename = r'C:\Users\86134\Desktop\autotest_tool\ML_GUI_Prototype\screenshot\codeadore.textgram_2.png'
    filename = r'C:\Users\86134\Desktop\autotest_tool\ML_GUI_Prototype\screenshot\com.infonow.bofa_1.png'
    # filename = r'C:\Users\86134\Desktop\autotest_tool\ML_GUI_Prototype\screenshot\com.netflix.mediaclient_1.png'
    # filename = r'C:\Users\86134\Desktop\autotest_tool\ML_GUI_Prototype\screenshot\com.crunchyroll.crmanga_2.png'
    # filename = r'C:\Users\86134\Desktop\autotest_tool\ML_GUI_Prototype\screenshot\com.giphy.messenger_1.png'
    # filename = r'C:\Users\86134\Desktop\autotest_tool\ML_GUI_Prototype\screenshot\com.allfootball.news_2.png'
    # filename = r'C:\Users\86134\Desktop\autotest_tool\ML_GUI_Prototype\screenshot\com.reddit.frontpage_2.png'
    filename = r'C:\Users\86134\Desktop\autotest_tool\ML_GUI_Prototype\screenshot\com.allfootball.news_3.png'
    runApplication(filename)
