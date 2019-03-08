import cv2
import numpy
#numpy is only used to create an ndarray for displaying the segmented image.

threshvals = {}


def createhist(img):
    row, col = img.shape
    y = [0] * 256
    for i in range(0, row):
        for j in range(0, col):
            y[img[i, j]] += 1
    return y


def pixels(hist):
    cnt = 0
    for i in range(0, len(hist)):
        if hist[i] > 0:
            cnt += hist[i]
    return cnt


def weight(s, e):
    w = 0
    for i in range(s, e):
        w += hist[i]
    return w


def mean(s, e):
    m = 0
    w = weight(s, e)
    for i in range(s, e):
        m += hist[i] * i

    return m / float(w)


def variance(s, e):
    v = 0
    m = mean(s, e)
    w = weight(s, e)
    for i in range(s, e):
        v += ((i - m) ** 2) * hist[i]
    v /= w
    return v


def findthresh():
    pcnt = pixels(hist)
    for i in range(1, len(hist)):
        wb = weight(0, i) / float(pcnt)
        mb = mean(0, i)
        vb = variance(0, i)

        wf = weight(i, len(hist)) / float(pcnt)
        mf = mean(i, len(hist))
        vf = variance(i, len(hist))

        wcv = wb * (vb) + wf * (vf)
        bcv = wb * wf * (mb - mf) ** 2

        threshvals[i] = wcv


def optimalthresh():
    minwcv = sorted(threshvals.values())[0]
    for key,value in threshvals.iteritems():
        if value == minwcv:
            return key


image = cv2.imread('backg.jpg',0)
hist = createhist(image)
findthresh()
optimalval = optimalthresh()
row, col = image.shape
y = numpy.zeros((row,col))
for i in range(0, row):
    for j in range(0, col):
        if image[i, j] >= optimalval:
            y[i, j] = 255
        else:
            y[i, j] = 0
cv2.imshow("image", y)
cv2.waitKey(0)
