from datetime import datetime
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score

class MachineLearning():

    def __init__(self):

        print("Loading dataset ...")

        self.flow_dataset = pd.read_csv('../../data/NF-UNSW-NB15.csv')
        self.flow_dataset = self.flow_dataset.head(400000)

        self.flow_dataset.iloc[:, 0] = self.flow_dataset.iloc[:, 0].str.replace('.', '')
        self.flow_dataset.iloc[:, 2] = self.flow_dataset.iloc[:, 2].str.replace('.', '')

        self.X_flow = self.flow_dataset.iloc[:, :-1].values
        self.X_flow = self.X_flow.astype('float64')

        self.y_flow = self.flow_dataset.iloc[:, -1].values

        self.X_flow_train, self.X_flow_test, self.y_flow_train, self.y_flow_test = train_test_split(self.X_flow, self.y_flow, test_size=0.3, random_state=0)

    def RF(self):

        print("------------------------------------------------------------------------------")
        print("RANDOM FOREST ...")

        self.classifier = RandomForestClassifier(n_estimators=10, criterion="entropy", random_state=0)
        self.Confusion_matrix()

    def NB(self):

        print("------------------------------------------------------------------------------")
        print("NAIVE BAYES ...")

        self.classifier = GaussianNB()
        self.Confusion_matrix()
    
    def SVM(self):

        print("------------------------------------------------------------------------------")
        print("SUPPORT VECTOR MACHINE ...")
        
        self.classifier = SVC(kernel='rbf', random_state=0)
        self.Confusion_matrix()

    def Confusion_matrix(self):

        self.flow_model = self.classifier.fit(self.X_flow_train, self.y_flow_train)

        self.y_flow_pred = self.flow_model.predict(self.X_flow_test)

        print("------------------------------------------------------------------------------")

        print("confusion matrix")
        cm = confusion_matrix(self.y_flow_test, self.y_flow_pred)
        print(cm)

        acc = accuracy_score(self.y_flow_test, self.y_flow_pred)
        print("Success Accuracy = {0:.2f} %".format(acc*100))
        fail = 1.0 - acc
        print("Fail Accuracy = {0:.2f} %".format(fail*100))

def main():

    start_script = datetime.now()
    ml = MachineLearning()

    start = datetime.now()
    ml.RF()
    end = datetime.now()
    print("LEARNING and PREDICTING Time: ", (end-start))

    start = datetime.now()
    ml.NB()
    end = datetime.now()
    print("LEARNING and PREDICTING Time: ", (end-start))

    start = datetime.now()
    ml.SVM()
    end = datetime.now()
    print("LEARNING and PREDICTING Time: ", (end-start))

    end_script = datetime.now()
    print("Script Time: ", (end_script-start_script))

if __name__ == "__main__":
    main()
