from functions import *
import solver

model = intializePredectionModel()


img = cv2.imread( r"C:\Users\ARJUN\SudokuArjun\test.jpeg")
img = cv2.resize(img, (450, 450))
imgBlank = np.zeros((450, 450, 3), np.uint8)
preProcessedImage = preProcess(img)
# cv2.imshow('Pre Processed Image', preProcessedImage)
imgContours = img.copy()
imgBigContour = img.copy()
contours, hierarchy = cv2.findContours(preProcessedImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 3)

rect, maxArea = biggestContour(contours)

if rect.size != 0:
    rect = reorder(rect)
    cv2.drawContours(imgBigContour, rect, -1, (0, 0, 255), 25)
    pts1 = np.float32(rect)
    pts2 = np.float32([[0, 0], [450, 0], [0, 450], [450, 450]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgWarpColored = cv2.warpPerspective(img, matrix, (450, 450))
    imgWarped = cv2.cvtColor(imgWarpColored, cv2.COLOR_BGR2GRAY)

    detectedImage = imgBlank.copy()
    solvedImage = imgBlank.copy()

    boxes = splitBoxes(imgWarped)

    numbers = getPredection(boxes, model)

    detectedImage = displayBoard(detectedImage, numbers)
    numbers = np.asarray(numbers)
    posArray = np.where(numbers > 0, 0, 1)
    board = np.array_split(numbers, 9)

    solver.solve(board)

    flatList = []
    for sublist in board:
        for item in sublist:
            flatList.append(item)
    solvedNumbers = flatList * posArray
    solvedImage = displayBoard(solvedImage, solvedNumbers)

    dst = np.float32(rect)
    src = np.float32([[0, 0], [450, 0], [0, 450], [450, 450]])
    matrix = cv2.getPerspectiveTransform(src, dst)
    inverseWarpedImage = img.copy()
    inverseWarpedImage = cv2.warpPerspective(solvedImage, matrix, (450, 450))
    inversePerspective = cv2.addWeighted(inverseWarpedImage, 1, img, 0.5, 1)

    detectedBoard = grid(detectedImage)
    # cv2.imshow('Question', detectedBoard)

    solvedBoard = grid(solvedImage)
    cv2.imshow('Solution', inversePerspective)

else:
    print("No Sudoku Found")

cv2.waitKey(0)
