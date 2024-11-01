# -*- coding: utf-8 -*-

Original file is located at
    https://colab.research.google.com/drive/1yVTM6O1av-Butm_2BTVQRR5twbyl25tL
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV,train_test_split
from imblearn.over_sampling import SMOTE  # imblearn library can be installed using pip install imblearn
from imblearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier
from sklearn import ensemble
from sklearn.ensemble import AdaBoostClassifier
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# Importing dataset and examining it
dataset = pd.read_csv("/content/drive/MyDrive/DataSets/diabetes_012_health_indicators_BRFSS2015.csv")
pd.set_option('display.max_columns', None) # to make sure you can see all the columns in output window
print(dataset.head())
print(dataset.shape)
print(dataset.info())
print(dataset.describe())

# Dividing dataset into label and feature sets
X = dataset.drop('Diabetes_012', axis = 1) # Features
Y = dataset['Diabetes_012'] # Labels
print(type(X))
print(type(Y))
print(X.shape)
print(Y.shape)

#list of top features that have high correlation between features and target
features = dataset.corr()['Diabetes_012'].sort_values()
features

high_corr_features = features[features >= 0.2].index
print(high_corr_features)

# Selecting high correlation features
X = dataset[high_corr_features].drop('Diabetes_012', axis=1)

# Normalizing numerical features so that each feature has mean 0 and variance 1
feature_scaler = StandardScaler()
X_scaled = feature_scaler.fit_transform(X)

X_train, X_test, Y_train, Y_test = train_test_split( X_scaled, Y, test_size = 0.2, random_state = 100)# splitting

"""##Implementing Logistic Regression"""

# Tuning eta0, max_iter, alpha, and l1_ratio parameters and implementing cross-validation using Grid Search
model = Pipeline([
        ('balancing', SMOTE(random_state = 101)),   # Synthetic Minority Oversampling Technique
        ('classification', SGDClassifier(loss = 'log', penalty = 'elasticnet', random_state = 1))
    ])
grid_param = {'classification__eta0': [0.01,.1,1,10,100], 'classification__max_iter' : [100,500],
              'classification__alpha': [0.01,.1,1,10,100], 'classification__l1_ratio': [0,0.3,0.5,0.7,1]}

gd_sr = GridSearchCV(estimator=model, param_grid=grid_param, scoring='recall_macro', cv=5,n_jobs=-1)

"""
In the above GridSearchCV(), scoring parameter should be set as follows:
scoring = 'accuracy' when you want to maximize prediction accuracy
scoring = 'recall' when you want to minimize false negatives
scoring = 'precision' when you want to minimize false positives
scoring = 'f1' when you want to balance false positives and false negatives (place equal emphasis on minimizing both)
"""

gd_sr.fit(X_scaled, Y)

best_parameters = gd_sr.best_params_
print("Best parameters: ", best_parameters)

best_result = gd_sr.best_score_ # Mean cross-validated score of the best_estimator
print("Best result: ", best_result)

"""##Implementing Random Forest Classifier"""

# Using pipeline
from imblearn.pipeline import Pipeline
RF_classifier5 = Pipeline([('balancing', SMOTE(random_state = 101)),('classification', ensemble.RandomForestClassifier(criterion='entropy', max_features='auto', random_state=1))]) # building classifier
no_trees = {'classification__n_estimators': [10,20,30,40,50,100]}
grid_search3 = GridSearchCV(estimator=RF_classifier5, param_grid=no_trees, scoring='recall_macro', cv=5)
grid_search3.fit(X_scaled, Y)

best_parameters = grid_search3.best_params_
print(best_parameters)
best_result = grid_search3.best_score_
print(best_result)

"""##Implementing AdaBoost"""

## Implementing AdaBoost
# Tuning the AdaBoost parameter 'n_estimators' and implementing cross-validation using Grid Search
model = Pipeline([
        ('balancing', SMOTE(random_state = 101)),
        ('classification', AdaBoostClassifier(random_state=1))
    ])
grid_param = {'classification__n_estimators': [2,3,4,5,10,20,30,40,50,100]}

gd_sr = GridSearchCV(estimator=model, param_grid=grid_param, scoring='recall_macro', cv=5)

"""
In the above GridSearchCV(), scoring parameter should be set as follows:
scoring = 'accuracy' when you want to maximize prediction accuracy
scoring = 'recall' when you want to minimize false negatives
scoring = 'precision' when you want to minimize false positives
scoring = 'f1' when you want to balance false positives and false negatives (place equal emphasis on minimizing both)
"""

gd_sr.fit(X_scaled, Y)

best_parameters = gd_sr.best_params_
print(best_parameters)

best_result = gd_sr.best_score_ # Mean cross-validated score of the best_estimator
print(best_result)

featimp = pd.Series(gd_sr.best_estimator_.named_steps["classification"].feature_importances_, index=list(X)).sort_values(ascending=False) # Getting feature importances list for the best model
print(featimp)
