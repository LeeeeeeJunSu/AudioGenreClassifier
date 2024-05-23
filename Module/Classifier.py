# Implement the SVM
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Root Folder를 Python Path에 추가
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

class SVM:
    def __init__(self, kernel='rbf', gamma='scale'):
        self.kernel = kernel
        self.gamma = gamma
        self.scaler = StandardScaler()
        self.svm_model =  SVC(kernel=self.kernel, gamma=self.gamma)

    def train(self, X_train, y_train):
        X_train = self.scaler.fit_transform(X_train)
        self.svm_model.fit(X_train, y_train)

    def predict(self, X_test):
        X_test = self.scaler.transform(X_test)
        return self.svm_model.predict(X_test)