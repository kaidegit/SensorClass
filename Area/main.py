import cv2 as cv
import numpy as np

# 读取图片
img = 'iPhoneX.jpg'
img = cv.imread(img)
cv.imshow('1', img)
# 转换成灰度
gray = cv.cvtColor(img.copy(), cv.COLOR_BGR2GRAY)
cv.imshow('2', gray)
# 二值化
ret, binary = cv.threshold(gray, 120, 255, cv.THRESH_BINARY)
cv.imshow('3', binary)
# 腐蚀膨胀
kernel = cv.getStructuringElement(cv.MORPH_RECT, (11, 11))
erode = cv.erode(binary, kernel)
cv.imshow('4', erode)
dilate = cv.dilate(erode, kernel)
cv.imshow('5', dilate)
# 找外轮廓 拟合直线
contours, _ = cv.findContours(dilate, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
approx = cv.approxPolyDP(contours[0], 5, True)
img_approx = cv.polylines(img.copy(), [approx], True, (0, 0, 255), 2)
cv.imshow('6', img_approx)
# 透视变幻
target = np.array([[0., 0.],
                   [0., img.shape[0] * 0.7071],
                   [img.shape[0], img.shape[0] * 0.7071],
                   [img.shape[0], 0.]], dtype=np.float32)
M = cv.getPerspectiveTransform(np.array(approx, dtype=np.float32), target)
perspective = cv.warpPerspective(dilate.copy(), M, (img.shape[0], int(img.shape[0] * 0.7071)), cv.INTER_LINEAR,
                                 cv.BORDER_CONSTANT)
perspective_color = cv.warpPerspective(img.copy(), M, (img.shape[0], int(img.shape[0] * 0.7071)), cv.INTER_LINEAR,
                                       cv.BORDER_CONSTANT)
cv.imshow('7', perspective)
# 找手机的外轮廓
perspective = cv.bitwise_not(perspective)
perspective = cv.erode(perspective, kernel)
perspective = cv.dilate(perspective, kernel)
contours, _ = cv.findContours(perspective, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
approx = cv.approxPolyDP(contours[0], 5, True)
img_approx = cv.polylines(perspective_color.copy(), [approx], True, (0, 0, 255), 2)
cv.imshow('8', img_approx)
# 找手机的四个顶点
x_min = 65535
x_max = 0
y_min = 65535
y_max = 0
for each in approx:
    if x_min > each.tolist()[0][0]:
        x_min = each.tolist()[0][0]
    if x_max < each.tolist()[0][0]:
        x_max = each.tolist()[0][0]
    if y_min > each.tolist()[0][1]:
        y_min = each.tolist()[0][1]
    if y_max < each.tolist()[0][1]:
        y_max = each.tolist()[0][1]
img_line = cv.line(perspective_color.copy(), (x_min, y_min), (x_max, y_min), (255, 0, 0))
img_line = cv.line(img_line, (x_min, y_max), (x_max, y_max), (255, 0, 0))
img_line = cv.line(img_line, (x_min, y_max), (x_min, y_min), (255, 0, 0))
img_line = cv.line(img_line, (x_max, y_min), (x_max, y_max), (255, 0, 0))
cv.imshow('9', img_line)
# 根据比例求面积
x = x_max - x_min
y = y_max - y_min
paper_height = perspective_color.shape[0]
paper_width = perspective_color.shape[1]
times = paper_height / 210
area = x * y / times / times
print(area, "mm^2")

while True:
    cv.waitKey(1)
