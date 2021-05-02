import cv2
import numpy as np
from tensorflow.keras.models import load_model


def preProcess(img):
    grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurImage = cv2.GaussianBlur(grayImage, (5, 5), 1)
    preProcessedImage = cv2.adaptiveThreshold(blurImage, 255, 1, 1, 9, 2)
    return preProcessedImage


def biggestContour(contours):
    rect = np.array([])
    maxArea = 0
    for i in contours:
        area = cv2.contourArea(i)
        if area > 50:
            perimeter = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.015 * perimeter, True)
            if area > maxArea and len(approx) == 4:
                rect = approx
                maxArea = area
    return rect, maxArea


def reorder(points):
    points = points.reshape((4, 2))
    newPoints = np.zeros((4, 1, 2), dtype=np.int32)
    add = points.sum(1)
    newPoints[0] = points[np.argmin(add)]
    newPoints[3] = points[np.argmax(add)]
    diff = np.diff(points, axis=1)
    newPoints[1] = points[np.argmin(diff)]
    newPoints[2] = points[np.argmax(diff)]
    return newPoints


def splitBoxes(img):
    rows = np.vsplit(img, 9)
    boxes = []
    for r in rows:
        cols = np.hsplit(r, 9)
        for c in cols:
            boxes.append(c)
    return boxes


def intializePredectionModel():
    model = load_model('myModel.h5')
    return model


def getPredection(boxes, model):
    result = []
    for image in boxes:
        img = np.asarray(image)
        img = img[4:img.shape[0] - 4, 4:img.shape[1] - 4]
        img = cv2.resize(img, (28, 28))
        img = img / 255
        img = img.reshape(1, 28, 28, 1)
        predictions = model.predict(img)
        classIndex = model.predict_classes(img)
        probabilityValue = np.amax(predictions)
        if probabilityValue > 0.9:
            result.append(classIndex[0])
        else:
            result.append(0)
    return result


def displayBoard(img, numbers):
    color = (255, 255, 0)
    w = int(img.shape[1] / 9)
    h = int(img.shape[0] / 9)
    for x in range(0, 9):
        for y in range(0, 9):
            if numbers[(y * 9) + x] != 0:
                cv2.putText(img, str(numbers[(y * 9) + x]), (x * w + int(w / 2) - 10, int((y + 0.8) * h)),
                            cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255, 255, 0),
                            2, cv2.LINE_AA)
    return img


def grid(img):
    color = (255, 255, 0)
    w = int(img.shape[1] / 9)
    h = int(img.shape[0] / 9)
    for i in range(0, 9):
        pt1 = (0, h * i)
        pt2 = (img.shape[1], h * i)
        pt3 = (w * i, 0)
        pt4 = (w * i, img.shape[0])
        cv2.line(img, pt1, pt2, color, 1)
        cv2.line(img, pt3, pt4, color, 1)
    cv2.line(img, (0, h * 3), (img.shape[1], h * 3), color, 3)
    cv2.line(img, (0, h * 6), (img.shape[1], h * 6), color, 3)
    cv2.line(img, (w * 3, 0), (w * 3, img.shape[0]), color, 3)
    cv2.line(img, (w * 6, 0), (w * 6, img.shape[0]), color, 3)
    cv2.line(img, (0, h * 9), (img.shape[1], h * 9), color, 3)
    cv2.line(img, (w * 9, 0), (w * 9, img.shape[0]), color, 3)
    return img