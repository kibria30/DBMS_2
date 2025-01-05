from sklearn import datasets
from sklearn.model_selection import train_test_split
import numpy as np
from DecisionTree import DecisionTree
from sklearn.metrics import precision_score
from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import fbeta_score

data = datasets.load_iris()
X, y = data.data, data.target

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=1234
)

clf = DecisionTree(max_depth=5)
clf.fit(X_train, y_train)
predictions = clf.predict(X_test)

def accuracy(y_test, y_pred):
    return np.sum(y_test == y_pred) / len(y_test)

acc = accuracy(y_test, predictions)
print("accuracy: ", acc)

precision = precision_score(y_test, predictions, average='weighted')
print("precision: ", precision)

# Function to calculate F1 score
def f1_score(y_test, y_pred):
    cm = confusion_matrix(y_test, y_pred)
    TP = cm[1, 1]  # True Positives
    FP = cm[0, 1]  # False Positives
    FN = cm[1, 0]  # False Negatives
    precision = TP / (TP + FP) if (TP + FP) > 0 else 0
    recall = TP / (TP + FN) if (TP + FN) > 0 else 0
    if precision + recall == 0:
        return 0  # Avoid division by zero
    return 2 * (precision * recall) / (precision + recall)

# Function to calculate D2H
def distance_to_heaven(y_test, y_pred):
    cm = confusion_matrix(y_test, y_pred)
    TP = cm[1, 1]
    FP = cm[0, 1]
    FN = cm[1, 0]
    precision = TP / (TP + FP) if (TP + FP) > 0 else 0
    recall = TP / (TP + FN) if (TP + FN) > 0 else 0
    return np.sqrt((1 - recall)**2 + (1 - precision)**2)

# Calculate metrics
f1 = f1_score(y_test, predictions)
d2h = distance_to_heaven(y_test, predictions)

# Output results
print(f"F1 Score: {f1}")
print(f"Distance to Heaven (D2H): {d2h}")