import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
from sklearn.impute import SimpleImputer

from helpers import DATASET_SIZE
from datetime import datetime

class RandomFClassifier:

    def __init__(self, dataset_path, dataset_size=DATASET_SIZE):
        print("Loading dataset ...")
        self.flow_dataset = pd.read_csv(dataset_path)
        self.flow_dataset.iloc[:, 0] = self.flow_dataset.iloc[:, 0].str.replace('.', '')
        self.flow_dataset.iloc[:, 2] = self.flow_dataset.iloc[:, 2].str.replace('.', '')
        self.flow_dataset = self.flow_dataset.head(dataset_size)

    def flow_training(self, n_estimators=10, criterion='entropy', max_depth=None):
        print("Flow Training with n_estimators={}, criterion={}, max_depth={} ...".format(n_estimators, criterion, max_depth))

        X_flow = self.flow_dataset.iloc[:, [0, 8, 11, 13]].values.astype('float64')
        y_flow = self.flow_dataset.iloc[:, -1].values
        imputer = SimpleImputer(strategy='mean')
        X_flow = imputer.fit_transform(X_flow)
        
        X_flow_train, X_flow_test, y_flow_train, y_flow_test = train_test_split(X_flow, y_flow, test_size=0.3, random_state=0)

        classifier = RandomForestClassifier(n_estimators=n_estimators, criterion=criterion, max_depth=max_depth, random_state=0)
        flow_model = classifier.fit(X_flow_train, y_flow_train)
        joblib.dump(flow_model, "./rf_trained_data.joblib")
        return self.evaluate_model(X_flow_test, y_flow_test, flow_model)  # Return the F1 score

    def train_classifier(self, classifier):
        print("------------------------------------------------------------------------------")
        print(f"{classifier.__class__.__name__.upper()} ...")
        self.classifier = classifier
        self.flow_model = self.classifier.fit(self.X_flow_train, self.y_flow_train)
        self.evaluate_model()

    def evaluate_model(self, X_test, y_test, model):
        print("------------------------------------------------------------------------------")
        y_flow_pred = model.predict(X_test)

        print("Confusion matrix")
        cm = confusion_matrix(y_test, y_flow_pred)
        print(cm)

        TP = cm[1, 1]  
        TN = cm[0, 0]  
        FP = cm[0, 1]  
        FN = cm[1, 0]  

        print("True Positives = {}".format(TP))
        print("True Negatives = {}".format(TN))
        print("False Positives = {}".format(FP))
        print("False Negatives = {}".format(FN))

        acc = accuracy_score(y_test, y_flow_pred)
        print("Success Accuracy = {:.2f} %".format(acc * 100))

        precision = precision_score(y_test, y_flow_pred)
        recall = recall_score(y_test, y_flow_pred)
        f1 = f1_score(y_test, y_flow_pred)

        print("Precision = {:.2f}".format(precision))
        print("Recall = {:.2f}".format(recall))
        print("F1-score = {:.2f}".format(f1))
        print("------------------------------------------------------------------------------")
        return f1 


def main():
    dataset_path = 'data/NF-UNSW-NB15.csv'
    start = datetime.now()
    rf_classifier = RandomFClassifier(dataset_path)
    rf_classifier.flow_training()
    # Save the training data
    n_estimators_values = [10, 50, 100]
    criterion_values = ['gini', 'entropy']
    max_depth_values = [20]

    best_f1 = 0  
    best_params = None
    
    for n_estimators in n_estimators_values:
        for criterion in criterion_values:
            for max_depth in max_depth_values:
                f1 = rf_classifier.flow_training(n_estimators, criterion, max_depth)
                if f1 is not None and f1 > best_f1:
                    best_f1 = f1
                    best_params = (n_estimators, criterion, max_depth)
    
    end = datetime.now()
    print("Random Forests")
    print("------------------------------------------------------------------------------")
    print("Training time: ", (end-start)) 
    print("Best Parameter Combination (n_estimators, criterion, max_depth):", best_params)
    print("Best F1 Score:", best_f1)

if __name__ == "__main__":
    main()
          
          