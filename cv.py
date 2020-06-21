import cv2
from matplotlib import pyplot as plt
import numpy as np

def findkeypoints(filename):
    img = cv2.imread(filename,0)
    sift = cv2.xfeatures2d.SIFT_create()
    kp, des = sift.detectAndCompute(img,None)
    return kp, des

def matchkeypoints(kp1, des1, kp2, des2):
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks=50)

    flann = cv2.FlannBasedMatcher(index_params,search_params)

    matches = flann.knnMatch(des1,des2,k=2)
    good = []
    for m,n in matches:
        if m.distance < 0.7*n.distance:
            good.append(m)
    return good

def findbestimg(filename):
    toolset = ['Retractors', 'Scissors', 'Clippers', 'Hemostats', 'Scalpels', 'Forceps', 'Hooks']
    mainkp, maindes = findkeypoints(filename)
    data = []
    for i in range(len(toolset)):
        tool = []
        data.append(tool)
        for j in range(6, 24):
            print("data_set/" + toolset[i] + "/" + str(j) + ".jpg")
            partkp, partdes = findkeypoints("data_set/" + toolset[i] + "/" + str(j) + ".jpg")
            data[i].append(len(matchkeypoints(mainkp, maindes, partkp, partdes)))
    best = []
    for i in range(len(toolset)):
        idx = 0
        length = 0
        for j in range(len(data[i])):
            if data[i][j] > length:
                length = data[i][j]
                idx = j
        best.append(idx + 6)
    return best

def maskimg(filename):
    kernele = np.ones((5,5),np.uint8)
    kerneld = np.ones((5,5),np.uint8)

    img = cv2.imread(filename)
    org = img
    table = img
    greenL = np.array([130, 120, 85])
    greenH = np.array([190, 180, 130])
    gmask = cv2.inRange(img, greenL, greenH)
    mask_rgb = cv2.cvtColor(gmask, cv2.COLOR_GRAY2BGR)
    img = img & mask_rgb

    ret, threshed_img = cv2.threshold(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 10, 255, cv2.THRESH_BINARY)
    
    #img = cv2.erode(threshed_img,kernele,iterations = 1)
    img = cv2.dilate(threshed_img,kerneld,iterations = 2)
    #plt.imshow(img), plt.show()
    image, contours, hier = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    resultimg = []
    centerpoints = []
    for c in contours:
        temp = org
        x, y, w, h = cv2.boundingRect(c)
        if(w>100 and h>100 and w<1000 and h<1000):

            black = np.zeros((1200, 1600, 3), np.uint8)
            #block = cv2.rectangle(black,(x,y),(x+w,y+h),(255, 255, 255), -1)
            rect = cv2.minAreaRect(c)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            block = cv2.drawContours(black,[box],0,(255,255,255),-1)
            #plt.imshow(block), plt.show()
            temp = temp & black
            #plt.imshow(temp), plt.show()
            resultimg.append(temp)

            #cv2.rectangle(org,(x,y),(x+w,y+h),(0,255,0),1)

            #rect = cv2.minAreaRect(c)
            #box = cv2.boxPoints(rect)
            #box = np.int0(box)

            cv2.drawContours(table,[box],0,(0,255,255),1)

            M = cv2.moments(c)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            center = (cx,cy)
            centerpoints.append(center)
            radius = 3
            cv2.circle(table,center,radius,(255,100,0),2)
        
    #plt.imshow(org), plt.show()
    return resultimg, centerpoints, table

def findtool(resultimg, centerpoints, table):
    toolset = ['Retractors', 'Scissors', 'Clippers', 'Hemostats', 'Scalpels', 'Forceps', 'Hooks']
    toolname = []
    for i in range(len(resultimg)):
        sift = cv2.xfeatures2d.SIFT_create()
        kp, des = sift.detectAndCompute(resultimg[i],None)
        cntnum = []
        for tool in toolset:
            count = 0
            for k in range(6, 24):
                #print("data_set/" + toolset[i] + "/" + str(j) + ".jpg")
                partkp, partdes = findkeypoints("data_set/" + tool + "/" + str(k) + ".jpg")
                count = count + len(matchkeypoints(kp, des, partkp, partdes))
            cntnum.append(count)

        idx = 0
        num = 0
        for m in range(len(cntnum)):
            if cntnum[m] > num:
                num = cntnum[m]
                idx = m
        print cntnum
        print(toolset[idx])
        toolname.append(toolset[idx])
        #toolset.remove(toolset[idx])
        #plt.imshow(resultimg[i]), plt.show()
    return toolname

def printname(centerpoints, table, toolname):
    for i in range(len(centerpoints)):
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(table, toolname[i], (centerpoints[i][0], centerpoints[i][1]), font, 2, (255,255,255), 5)
        print(toolname[i] + " at (" + str(centerpoints[i][0]) + ", " + str(centerpoints[i][1]) + ")")
    plt.imshow(table), plt.show()

if __name__ == '__main__':

    #print(findbestimg("5.jpg"))
    resultimg, centerpoints, table = maskimg("21.jpg")
    toolname = findtool(resultimg, centerpoints, table)
    printname(centerpoints, table, toolname)






        