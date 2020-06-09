'''
Created on 2020-05-07
@author: zhengjin
@desc: 获取验证码的单个字符
'''

import cv2
import os
import uuid

import numpy as np
import tensorflow.keras as keras


def split_verifycode(img_path):
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

    # 提取单个字符
    chars_list = []
    contours, hierarchy = cv2.findContours(thresh1, 2, 2)

    for cnt in contours:
        # 最小的外接矩形
        x, y, w, h = cv2.boundingRect(cnt)
        if x != 0 and y != 0 and w*h >= 100:
            chars_list.append((x, y, w, h))
    sorted_chars_list = sorted(chars_list, key=lambda x: x[0])

    for i, item in enumerate(sorted_chars_list):
        x, y, w, h = item
        save_path = '/tmp/test/chars/char_%d.jpg' % i
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


def resplit_with_parts(img_path, parts):
    image = cv2.imread(img_path, 0)
    height, width = image.shape

    start = 0
    # 将图片重新分裂成parts部分
    step = width // parts
    for _ in range(parts):
        cv2.imwrite('/tmp/test/char_%d.jpg' %
                    uuid.uuid1(), image[:, start:start+step])
        start += step
    os.remove(img_path)


# rename and convert to 16*20 size
def convert(dir, file):
    img_path = os.path.join(dir, file)
    image = cv2.imread(img_path, 0)
    # 二值化
    ret, thresh = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    img = cv2.resize(thresh, (16, 20), interpolation=cv2.INTER_AREA)

    # 保存图片
    cv2.imwrite(img_path, img)


def read_data(dir, file):
    '''
    读取图片的数据, 并转化为0-1值
    '''
    img_path = os.path.join(dir, file)
    image = cv2.imread(img_path, 0)
    # 二值化
    ret, thresh = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    bin_values = [1 if pixel == 255 else 0 for pixel in thresh.ravel()]

    return bin_values


def pre_handler_verifycode_main():
    '''
    字符前置处理：去掉噪声图片，处理黏连图片
    '''
    dir_path = '/tmp/test'
    for f_path in os.listdir(dir_path):
        remove_edge_image(os.path.join(dir_path, f_path))
    for f_path in os.listdir(dir_path):
        resplit(os.path.join(dir_path, f_path))


def split_verifycode_main():
    '''
    字符切割, 获得单个字符
    '''
    # img_path = 'data/verifycode_01/1GDH.jpg'
    dir_path = 'data/verifycode_01'
    img_paths = [os.path.join(dir_path, img) for img in os.listdir(dir_path)]
    for img_path in img_paths[:10]:
        split_verifycode(img_path)


def cnn_predict(verifycode_path):
    dir = '/tmp/test/chars'
    files = os.listdir(dir)

    # 清空原有的文件
    if files:
        for file in files:
            os.remove(os.path.join(dir, file))

    split_verifycode(verifycode_path)

    files = os.listdir(dir)
    if not files:
        raise Exception('chars dir (%s) are empty' % dir)

    for file in files:
        # 去除噪声图片
        remove_edge_image(os.path.join(dir, file))

    # 对黏连图片进行重分割
    for file in os.listdir(dir):
        resplit(os.path.join(dir, file))
    # 将图片统一调整至16*20大小
    for file in os.listdir(dir):
        convert(dir, file)

    # 图片中的字符代表的向量
    files = sorted(os.listdir(dir), key=lambda x: x.split('.')[0])
    print('predict for char files:', files)
    table = np.array([read_data(dir, file)
                      for file in files]).reshape(-1, 20, 16, 1)

    # 模型保存地址
    model_path = '/tmp/test/verifycode_Keras.h5'
    # 载入模型
    cnn = keras.models.load_model(model_path)
    # 模型预测
    y_pred = cnn.predict(table)
    predictions = np.argmax(y_pred, axis=1)

    # 标签字典
    vals = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F',
            'G', 'H', 'J', 'K', 'L', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'X', 'Y', 'Z']
    label_dict = dict(zip(range(len(vals)), vals))

    return ''.join([label_dict[pred] for pred in predictions])


def cnn_predict_main():
    dir = 'data/verifycode_01'

    limit = 10
    correct = 0
    files = os.listdir(dir)[:limit]
    for i, file in enumerate(files):
        file_path = os.path.join(dir, file)
        true_label = file.split('.')[0]
        print('cnn predict for verifycode:', file_path)
        pred = cnn_predict(file_path)

        if true_label == pred:
            correct += 1
        print(i+1, (true_label, pred), true_label == pred, correct)

    total = min(len(os.listdir(dir)), limit)
    print('\n总共图片: %d张\n识别正确: %d张\n识别准确率: %.2f%%.'
          % (total, correct, correct*100/total))


if __name__ == '__main__':

    # split_verifycode_main()
    # pre_handler_verifycode_main()

    cnn_predict_main()

    print('split verify code demo done.')
