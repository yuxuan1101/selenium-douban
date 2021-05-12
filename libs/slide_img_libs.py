import numpy as np
import cv2
import urllib.request as request
from matplotlib import pyplot as plt

def show(slide, target, position):
    _, temp_w, temp_h = slide.shape[::-1]
    _, target_w, target_h = target.shape[::-1]
    print(slide.shape[::-1])
    print(target.shape[::-1])
    max_loc = (int(position['x'] * target_w), int(position['y'] * target_h))
    top_left = max_loc
    bottom_right = (top_left[0] + temp_w, top_left[1] + temp_h)
    matched = target.copy()
    cv2.rectangle(matched,top_left, bottom_right, 255, 2)

    plt.subplot(221),plt.imshow(target)
    plt.title('target'), plt.xticks([]), plt.yticks([])
    plt.subplot(222),plt.imshow(slide)
    plt.title('slide'), plt.xticks([]), plt.yticks([])
    plt.subplot(223),plt.imshow(matched)
    plt.title('matched'), plt.xticks([]), plt.yticks([])
    plt.suptitle('match result')
    plt.show()

def edge(img):
    # 灰度
    imgray = cv2.cvtColor(img.copy(),cv2.COLOR_BGR2GRAY)
    # 双边滤波
    blur = cv2.bilateralFilter(imgray, 9, 75, 75)
    # 边界检测
    edges = cv2.Canny(blur,100,200)
    return edges

def match(temp, img):
    img = img.copy()
    method = cv2.TM_CCOEFF_NORMED

    # Apply template Matching
    res = cv2.matchTemplate(img,temp,method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    return max_loc

def url2image(url):
    response = request.urlopen(url)
    img_array = np.array(bytearray(response.read()), dtype=np.uint8)
    return cv2.imdecode(img_array, cv2.IMREAD_COLOR)

def check_position(slide, target):
    max_loc = match(edge(slide), edge(target))
    _, img_w, img_h = target.shape[::-1]
    return {'x': max_loc[0]/ img_w, 'y': max_loc[1]/ img_h}

__all__ = ['check_position', 'show', 'url2image']

