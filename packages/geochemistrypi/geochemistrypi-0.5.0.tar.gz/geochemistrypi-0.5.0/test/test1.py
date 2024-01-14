import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import SGDClassifier



# data = pd.read_excel("./Data_Binary_Classification.xlsx")
# data = pd.read_excel("./Data_Multi_Classification.xlsx")
data = pd.read_excel("./Data_Regression.xlsx")
# X = data.iloc[:, 7:10]
# y = data.iloc[:, 11]
# # y = data.iloc[:, 2]

# print(X)
# print(y)
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# model = LinearRegression()
# # model = SGDClassifier()
# model.fit(X_train, y_train)
# print(model.coef_)
# print(type(model.coef_))
# print(model.coef_.shape)
# print(model.intercept_)
# print(type(model.intercept_))
# print(model.intercept_.shape)

# y_pred = model.predict(X_test)


# Use PCA to reduce the dimensionality of the data set
from sklearn.decomposition import PCA
X = data.iloc[:, 7:11]
print(X)
X.isnull().any().any()
pca = PCA(n_components=2)
X = pca.fit_transform(X)