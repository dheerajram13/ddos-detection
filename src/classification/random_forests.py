from datetime import datetime
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score

class MachineLearning():

    def __init__(self):
        
        print("Loading dataset ...")
        
        self.flow_dataset = pd.read_csv('../../data/NF-UNSW-NB15.csv')

        self.flow_dataset.iloc[:, 0] = self.flow_dataset.iloc[:, 0].str.replace('.', '')
        self.flow_dataset.iloc[:, 2] = self.flow_dataset.iloc[:, 2].str.replace('.', '')

    def flow_training(self, n_estimators=10, criterion='entropy', max_depth=None):
        print("Flow Training with n_estimators={}, criterion={}, max_depth={} ...".format(n_estimators, criterion, max_depth))
        
        X_flow = self.flow_dataset.iloc[:, :-1].values
        X_flow = X_flow.astype('float64')

        y_flow = self.flow_dataset.iloc[:, -1].values

        X_flow_train, X_flow_test, y_flow_train, y_flow_test = train_test_split(X_flow, y_flow, test_size=0.25, random_state=0)

        classifier = RandomForestClassifier(n_estimators=n_estimators, criterion=criterion, max_depth=max_depth, random_state=0)
        flow_model = classifier.fit(X_flow_train, y_flow_train)

        y_flow_pred = flow_model.predict(X_flow_test)

        print("------------------------------------------------------------------------------")

        print("confusion matrix")
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

        return f1  

def main():
    start = datetime.now()
    
    ml = MachineLearning()
    
    n_estimators_values = [10, 50, 100]
    criterion_values = ['gini', 'entropy']
    max_depth_values = [None, 10, 20]

    best_f1 = -1  
    best_params = None
    
    for n_estimators in n_estimators_values:
        for criterion in criterion_values:
            for max_depth in max_depth_values:
                f1 = ml.flow_training(n_estimators, criterion, max_depth)
                if f1 > best_f1:
                    best_f1 = f1
                    best_params = (n_estimators, criterion, max_depth)
    
    end = datetime.now()
    print("Training time: ", (end-start)) 
    print("Best Parameter Combination (n_estimators, criterion, max_depth):", best_params)
    print("Best F1 Score:", best_f1)

if __name__ == "__main__":
    main()
