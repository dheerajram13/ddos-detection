from datetime import datetime
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score

class MachineLearning():

    def __init__(self):
        
        print("Loading dataset ...")
        
        self.flow_dataset = pd.read_csv('../../data/NF-UNSW-NB15.csv')

        self.flow_dataset.iloc[:, 0] = self.flow_dataset.iloc[:, 0].str.replace('.', '')
        self.flow_dataset.iloc[:, 2] = self.flow_dataset.iloc[:, 2].str.replace('.', '')

    def flow_training(self):

        print("Flow Training ...")
        
        X_flow = self.flow_dataset.iloc[:, :-1].values
        X_flow = X_flow.astype('float64')

        y_flow = self.flow_dataset.iloc[:, -1].values

        X_flow_train, X_flow_test, y_flow_train, y_flow_test = train_test_split(X_flow, y_flow, test_size=0.25, random_state=0)

        classifier = GaussianNB()
        flow_model = classifier.fit(X_flow_train, y_flow_train)

        y_flow_pred = flow_model.predict(X_flow_test)

        print("------------------------------------------------------------------------------")

        print("Confusion matrix")
        cm = confusion_matrix(y_flow_test, y_flow_pred)
        print(cm)

        acc = accuracy_score(y_flow_test, y_flow_pred)
        print("Accuracy = {0:.2f} %".format(acc*100))

        precision = precision_score(y_flow_test, y_flow_pred)
        recall = recall_score(y_flow_test, y_flow_pred)
        f1 = f1_score(y_flow_test, y_flow_pred)

        print("Precision = {0:.2f}".format(precision))
        print("Recall = {0:.2f}".format(recall))
        print("F1 Score = {0:.2f}".format(f1))

        print("------------------------------------------------------------------------------")
    
def main():
    start = datetime.now()
    
    ml = MachineLearning()
    ml.flow_training()

    end = datetime.now()
    print("Training time: ", (end-start)) 

if __name__ == "__main__":
    main()
