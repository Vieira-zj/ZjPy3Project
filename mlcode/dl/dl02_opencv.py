# pre-conditions:
# pip install opencv-python
# pip install tqdm
#
# PetImages 目录 猫和狗的图像
# https://download.microsoft.com/download/3/E/1/3E1C3F21-ECDB-4869-8368-6DEBA77B919F/kagglecatsanddogs_3367a.zip
#

# %%
import numpy as np
import matplotlib.pyplot as plt
import os
import cv2
from tqdm import tqdm
np.__version__

# %%
DATADIR = os.path.join(
    os.getenv('HOME'), 'Downloads/tmp_files/ml_data/PetImages')
CATEGORIES = ['Dog', 'Cat']

for category in CATEGORIES:
    path = os.path.join(DATADIR, category)
    for img in os.listdir(path):
        img_array = cv2.imread(os.path.join(path, img),
                               cv2.IMREAD_GRAYSCALE)
        plt.imshow(img_array, cmap='gray')
        plt.show()
        break
    break

# %%
img_array.shape

# %%
# 图像变小 灰度
IMG_SIZE = 50
new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
plt.imshow(new_array, cmap='gray')
plt.show()

# %%
IMG_SIZE = 100
new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
plt.imshow(new_array, cmap='gray')
plt.show()

# %%
new_array.shape

# %%
# todo:
