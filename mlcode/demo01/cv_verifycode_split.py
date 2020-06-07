'''
Created on 2020-05-07
@author: zhengjin
@Desc: 获取验证码的单个字符（字符切割）
'''

import cv2


def split_verify_code(img_path):
    # 以灰度模式读取图片
    gray = cv2.imread(img_path, 0)

    # 将图片的边缘变为白色
    height, width = gray.shape
    for i in range(width):
        gray[0, i] = 255
        gray[height - 1, i] = 255
    for j in range(height):
        gray[j, 0] = 255
        gray[j, width-1] = 255

    # 中值滤波
    blur = cv2.medianBlur(gray, 3)  # 模板大小3*3
    # 二值化
    ret, thresh1 = cv2.threshold(blur, 200, 255, cv2.THRESH_BINARY)

    contours, hierarchy = cv2.findContours(thresh1, 2, 2)

    idx = 1
    for cnt in contours:
        # 最小的外接矩形
        x, y, w, h = cv2.boundingRect(cnt)
        if x != 0 and y != 0 and w*h >= 100:
            print(x, y, w, h)
            cv2.imwrite('/tmp/test/char%d.jpg' % idx, thresh1[y:y+h, x:x+w])
            idx += 1


if __name__ == '__main__':
    img_path = 'data/verifycode_01/1KT7.jpg'
    split_verify_code(img_path)
    print('split verify code demo done.')
