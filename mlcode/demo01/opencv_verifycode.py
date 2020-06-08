'''
Created on 2020-05-07
@author: zhengjin
@Desc: 获取验证码的单个字符
'''

import cv2
import os
import uuid


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

    for cnt in contours:
        # 最小的外接矩形
        x, y, w, h = cv2.boundingRect(cnt)
        if x != 0 and y != 0 and w*h >= 100:
            save_path = '/tmp/test/char_%d.jpg' % uuid.uuid1()
            print('split char saved:', save_path)
            cv2.imwrite(save_path, thresh1[y:y+h, x:x+w])


def remove_edge_image(img_path):
    '''
    删除噪声图片
    '''
    image = cv2.imread(img_path, 0)
    height, width = image.shape

    # 检查图片4个点的像素是否为黑色
    corner_list = [image[0, 0] < 127, image[height-1, 0] < 127,
                   image[0, width-1] < 127, image[height-1, width-1] < 127]
    if sum(corner_list) >= 3:
        print('remove edge image:', img_path)
        os.remove(img_path)


def resplit_with_parts(img_path, parts):
    image = cv2.imread(img_path, 0)
    height, width = image.shape

    start = 0
    step = width // parts
    for _ in range(parts):
        cv2.imwrite('/tmp/test/char_%d.jpg' %
                    uuid.uuid1(), image[:, start:start+step])
        start += step
    os.remove(img_path)


def resplit(img_path):
    '''
    处理黏连图片，根据图片的长度，进行拆分
    '''
    image = cv2.imread(img_path, 0)
    height, width = image.shape

    if width >= 64:
        print('image resplit with 4 parts.')
        resplit_with_parts(img_path, 4)
    elif width >= 48:
        print('image resplit with 3 parts.')
        resplit_with_parts(img_path, 3)
    elif width >= 24:
        print('image resplit with 2 parts.')
        resplit_with_parts(img_path, 2)
    else:
        print('image without resplit.')


def split_verifycode_main():
    '''
    字符切割，获得单个字符
    '''
    # img_path = 'data/verifycode_01/1GDH.jpg'
    dir_path = 'data/verifycode_01'
    img_paths = [os.path.join(dir_path, img) for img in os.listdir(dir_path)]
    for img_path in img_paths[:10]:
        split_verify_code(img_path)


def pre_handler_verifycode_main():
    '''
    字符前置处理：去掉噪声图片，处理黏连图片
    '''
    dir_path = '/tmp/test'
    for f_path in os.listdir(dir_path):
        remove_edge_image(os.path.join(dir_path, f_path))
    for f_path in os.listdir(dir_path):
        resplit(os.path.join(dir_path, f_path))


if __name__ == '__main__':

    split_verifycode_main()
    pre_handler_verifycode_main()
    print('split verify code demo done.')
