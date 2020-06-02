# %%
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
np.__version__, cv2.__version__

# %%
# 读取训练数据集和标签
file_labels = os.listdir('data/knn_icode_label')



# %%
# 训练模型，用的是k相邻算法


# %%
# 测试集
dir_path = 'data/knn_icode_test'
test_imgs = os.listdir(dir_path)
len(test_imgs)

# %%
test_img_path = os.path.join(dir_path, test_imgs[4])
test_img_path


# %%
# 处理图片
img = cv2.imread(test_img_path)
plt.imshow(img)

# %%
# 图片高度 宽度 通道数
rows, cols, ch = img.shape
rows, cols, ch

# %%
# 转为灰度图
im_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# 二值化，就是黑白图。字符变成白色的，背景为黑色
_, im_inv = cv2.threshold(im_gray, 127, 255, cv2.THRESH_BINARY_INV)
# 应用高斯模糊对图片进行降噪。高斯模糊的本质是用高斯核和图像做卷积。就是去除一些斑斑点点的。因为二值化难免不够完美，去燥使得二值化结果更好
kernel = 1/16*np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]])
im_blur = cv2.filter2D(im_inv, -1, kernel)
# 再进行一次二值化
_, im_res = cv2.threshold(im_blur, 127, 255, cv2.THRESH_BINARY)
plt.imshow(im_res)


# %%
# 提取轮廓
contours, hierarchy = cv2.findContours(
    im_res, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
len(contours)

# %%
# 切割图片字符位置和宽度
ws = []  # 图片宽度
valid_contours = []  # 图片
for contour in contours:
    # 画矩形用来框住单个字符，x,y,w,h四个参数分别是该框的x,y坐标和w,h宽高
    x, y, w, h = cv2.boundingRect(contour)
    if w < 7:
        continue
    valid_contours.append(contour)
    ws.append(w)

w_min = min(ws)
w_max = max(ws)
w_min, w_max, len(valid_contours)

# %%
# 获取各切割区域位置和长宽
result = []

if len(valid_contours) >= 4:
    for contour in valid_contours:
        x, y, w, h = cv2.boundingRect(contour)
        box = np.int0([[x, y], [x+w, y], [x+w, y+h], [x, y+h]])
        result.append(box)
elif len(valid_contours) == 3:
    for contour in valid_contours:
        x, y, w, h = cv2.boundingRect(contour)
        if w == w_max:
            box_left = np.int0([[x, y], [x+w/2, y], [x+w/2, y+h], [x, y+h]])
            box_right = np.int0(
                [[x+w/2, y], [x+w, y], [x+w, y+h], [x+w/2, y+h]])
            result.append(box_left)
            result.append(box_right)
        else:
            box = np.int0([[x, y], [x+w, y], [x+w, y+h], [x, y+h]])
            result.append(box)
elif len(valid_contours) == 2:
    for contour in valid_contours:
        x, y, w, h = cv2.boundingRect(contour)
        if w == w_max and w_max >= w_min * 2:
            box_left = np.int0([[x, y], [x+w/3, y], [x+w/3, y+h], [x, y+h]])
            box_mid = np.int0(
                [[x+w/3, y], [x+w*2/3, y], [x+w*2/3, y+h], [x+w/3, y+h]])
            box_right = np.int0(
                [[x+w*2/3, y], [x+w, y], [x+w, y+h], [x+w*2/3, y+h]])
            result.append(box_left)
            result.append(box_mid)
            result.append(box_right)
        elif w_max < w_min * 2:
            box_left = np.int0([[x, y], [x+w/2, y], [x+w/2, y+h], [x, y+h]])
            box_right = np.int0(
                [[x+w/2, y], [x+w, y], [x+w, y+h], [x+w/2, y+h]])
            result.append(box_left)
            result.append(box_right)
        else:
            box = np.int0([[x, y], [x+w, y], [x+w, y+h], [x, y+h]])
            result.append(box)
elif len(valid_contours) == 1:
    contour = valid_contours[0]
    x, y, w, h = cv2.boundingRect(contour)
    box0 = np.int0([[x, y], [x+w/4, y], [x+w/4, y+h], [x, y+h]])
    box1 = np.int0([[x+w/4, y], [x+w*2/4, y], [x+w*2/4, y+h], [x+w/4, y+h]])
    box2 = np.int0([[x+w*2/4, y], [x+w*3/4, y],
                    [x+w*3/4, y+h], [x+w*2/4, y+h]])
    box3 = np.int0([[x+w*3/4, y], [x+w, y], [x+w, y+h], [x+w*3/4, y+h]])
    result.extend([box0, box1, box2, box3])

boxes = sorted(result, key=lambda x: x[0][0])
# 如果没有识别出4个字符，直接结束
if len(boxes) != 4:
    print('cannot get code')
boxes

# %%
# 调用模型进行识别
for box in boxes:
    # 获取字符长宽
    roi = im_res[box[0][1]:box[3][1], box[0][0]:box[1][0]]
    # 重新设长宽
    roistd = cv2.resize(roi, (30, 30))
    # 将图片转成像素矩阵
    sample = roistd.reshape((1, 900)).astype(np.float32)
    print(sample.shape)

    # 调用训练好的模型识别
    ret, results, neighbours, distances = model.findNearest(sample, k=3)
    # 获取对应标签id
    label_id = int(results[0, 0])
    # 根据id得到识别出的结果
    label = id_label_map[label_id]
    # 存放识别结果
    result.append(label)
