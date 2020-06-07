# %%
import matplotlib.pyplot as plt
import os
import cv2
cv2.__version__

# %%
img_path = 'data/verifycode_01/1GDH.jpg'
os.path.exists(img_path)

# %%
# 灰度模式读取图片
gray = cv2.imread(img_path, 0)
plt.imshow(gray)

# %%
# 验证码的边缘设置为白色（255）
height, width = gray.shape
for i in range(width):
    gray[0, i] = 255
    gray[height-1, i] = 255
for j in range(height):
    gray[j, 0] = 255
    gray[j, width-1] = 255

plt.imshow(gray)

# %%
# 中值滤波处理 模板大小 3*3
blur = cv2.medianBlur(gray, 3)
plt.imshow(gray)

# %%
# 二值化处理，将图像由灰度模式转化至黑白模式
ret, thresh1 = cv2.threshold(blur, 200, 255, cv2.THRESH_BINARY)
plt.imshow(thresh1)

# %%
# 提取单个字符
contours, hierarchy = cv2.findContours(thresh1, 2, 2)

for idx, cnt in enumerate(contours):
    x, y, w, h = cv2.boundingRect(cnt)
    if x != 0 and y != 0 and w*h >= 100:
        tmp_split = thresh1[y:y+h, x:x+w]
        cv2.imwrite('/tmp/test/char%d.jpg' % idx, tmp_split)

print('split char saved')

# %%
print('split verify code demo done.')
