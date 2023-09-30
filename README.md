# ddos-detection
DDOS Detection using ML 

Installation steps:
    1. Create an Python env (3.9).
    2. Install the modules from requirements.txt
    3. Download csv from https://rdm.uq.edu.au/files/c31a9f50-ef99-11ed-ab7b-c7846b13c8a9 and save it in  the data folder. (Don't commit this file to github)

Todo: 
    1. Read data from CSV(from the data folder) using pands, select the features and perform the train, test split. 
    This code is common for all the ML algos so better create a single function or class which can be resuse. (Aditya) 
    2. Implement the naive bayes  in the naive_bayes.py file. (Aditya)
    3. Implement SVM and Random forests in the respective files in the classication folder. (Meet)
    4. Work on the Ryu and mininet topology. 

How to commit: 
**Don't comit directly to the main branch. 
Before you commit, create a feature branch from master for example svm_feature and then work on the changes and push to the feature branch. Create a PR from the feature branch and master. 



