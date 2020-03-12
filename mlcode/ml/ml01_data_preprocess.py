# %%
# 数据预处理
import numpy as np
import pandas as pd

# %%
# 导入数据集
import os
data_path = os.path.join(os.getenv('PYPATH'), 'mlcode/ml/data/Data.csv')
dataset = pd.read_csv(data_path)
dataset.shape

# %%
dataset

# %%
arr = list(range(10))
print(arr)
print(arr[:-1])
arr[len(arr) - 1], arr[-1]

# %%
X = dataset.iloc[:, :-1].values
X

# %%
# Purchased (label)
Y = dataset.iloc[:, 3].values
Y

# %%
X[:, 1:3]

# %%
# 处理丢失数据
from sklearn.impute import SimpleImputer
imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
imputer.fit(X[:, 1:3])
X[:, 1:3] = imputer.transform(X[:, 1:3])
X

# %%
# 解析分类数据
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
labelencoder_X = LabelEncoder()
X[:, 0] = labelencoder_X.fit_transform(X[:, 0])
X

# %%
# 特征值数字化
from sklearn.compose import ColumnTransformer
categorical_features = [0]
onehotencoder = OneHotEncoder()
clt = ColumnTransformer(
    [('name', onehotencoder, categorical_features)], remainder='passthrough')
X = clt.fit_transform(X)
X

# %%
labelencoder_Y = LabelEncoder()
Y = labelencoder_Y.fit_transform(Y)
Y

# %%
# 拆分数据集为训练集合和测试集合
from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y, test_size=0.2, random_state=0)
X_train, X_test, Y_train, Y_test

# %%
# 特征量化
from sklearn.preprocessing import StandardScaler
sc_X = StandardScaler()
X_train = sc_X.fit_transform(X_train)
X_test = sc_X.transform(X_test)
X_train, X_test

# %%
print('data preprocess demo done')


# %%
# OneHotEncoder 将分类特征的每个元素转化为一个可直接计算的数值
from sklearn import preprocessing
enc = preprocessing.OneHotEncoder(categorical_features = [0])
arr = [[0, 0, 3], [1, 1, 0], [0, 2, 1], [1, 0, 2]]
# fit来学习编码
enc.fit(arr)
# 进行编码
enc.transform([[0, 1, 3]]).toarray()

# %%
enc = preprocessing.OneHotEncoder(handle_unknown='ignore')
enc.fit([['male', 0, 3], ['male', 1, 0], ['female', 2, 1], ['female', 0, 2]])
enc.categories_

# %%
enc.transform([['male', 0, 3], ['none', 1, 0], ['male', 0, 2]]).toarray()
enc.get_feature_names()

# %%
# ColumnTransformer
from sklearn.compose import ColumnTransformer
categorical_features = [0]
enc = OneHotEncoder(handle_unknown='ignore')
clt = ColumnTransformer(
    [('name', enc, categorical_features)], remainder='passthrough')

clt.fit([[0, 0, 3],
         [1, 1, 0],
         [0, 2, 1],
         [1, 0, 2]])

clt.transform([[0, 2, 3]])

# %%
# fit_transform
enc = OneHotEncoder(sparse=False)
ans = enc.fit_transform([[0, 0, 3],
                         [1, 1, 0],
                         [0, 2, 1],
                         [1, 0, 2]])
ans

# %%
enc = OneHotEncoder()
ans = enc.fit_transform([[0, 0, 3],
                         [1, 1, 0],
                         [0, 2, 1],
                         [1, 0, 2]])
ans.toarray()


# %%
# StandardScaler 去均值和方差归一化
from sklearn.preprocessing import StandardScaler
data = [[0, 0], [0, 0], [1, 1], [1, 1]]
scaler = StandardScaler()
scaler.fit(data)

# %%
scaler.mean_

# %%
scaler.transform(data)

# %%
scaler.transform([[2, 2]])

# %%
print('scikit-learn end')
