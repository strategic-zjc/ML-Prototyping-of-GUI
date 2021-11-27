import copy

from GUIDetection.procAppScreenshot import *
from CNNClassifier.classifier import *
from KNNAlgo.Utils.Node import *
from KNNAlgo.Utils.NodeUtils import *
import sys
from KNNAlgo.Aggregate import *
from KNNAlgo.Utils.HierarchyUtil import *

def runApplication(filePath):
    compon = processScreenshot(filePath)
    img_color = cv2.imread(filePath)
    GUINodes = rectViewsToNodes(compon, img_color)
    rect = Rect(0,0,img_color.shape[1], img_color.shape[0])
    inNode = GUINode(rect = rect)
    inNode.children.extend(GUINodes)
    rootNode = aggragate(inNode)

    drawHierarchy(img_color, rootNode)


    # following is more detailed implementation which generates codes, utilizing ocr to detect text and
    # and uses class type to create a runnable project....
    # left to implement.......

if __name__ == '__main__':
    argc = len(sys.argv)
    print(argc)
    if(argc == 1):
        print(f'Please input a file path to start running')
    else:
        filename = sys.argv[1]
        print(filename)
        runApplication(filename)
    # filename = r'C:\Users\86134\Desktop\autotest_tool\ML_GUI_Prototype\screenshot\com.crunchyroll.crmanga_1.png'
    # filename = r'C:\Users\86134\Desktop\autotest_tool\ML_GUI_Prototype\screenshot\com.dropbox.android_2.png'
    # filename = r'C:\Users\86134\Desktop\autotest_tool\ML_GUI_Prototype\screenshot\com.amazon.mShop.android.shopping_2.png'
    # filename = r'C:\Users\86134\Desktop\autotest_tool\ML_GUI_Prototype\screenshot\codeadore.textgram_2.png'
    # filename = r'C:\Users\86134\Desktop\autotest_tool\ML_GUI_Prototype\screenshot\com.infonow.bofa_1.png'
    # filename = r'C:\Users\86134\Desktop\autotest_tool\ML_GUI_Prototype\screenshot\com.netflix.mediaclient_1.png'
    # filename = r'C:\Users\86134\Desktop\autotest_tool\ML_GUI_Prototype\screenshot\com.crunchyroll.crmanga_2.png'
    # filename = r'C:\Users\86134\Desktop\autotest_tool\ML_GUI_Prototype\screenshot\com.giphy.messenger_1.png'
    # filename = r'C:\Users\86134\Desktop\autotest_tool\ML_GUI_Prototype\screenshot\com.allfootball.news_2.png'
    # filename = r'C:\Users\86134\Desktop\autotest_tool\ML_GUI_Prototype\screenshot\com.reddit.frontpage_2.png'
    # filename = r'C:\Users\86134\Desktop\autotest_tool\ML_GUI_Prototype\screenshot\com.allfootball.news_3.png'
    # filename = r'C:\Users\86134\Desktop\autotest_tool\ML_GUI_Prototype\screenshot\com.apalon.ringtones_1.png'
    # runApplication(filename)
