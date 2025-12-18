import numpy as np

def weighted_accuracy(y_true, y_pred):
    """
    Custom weighted accuracy metric.
    
    Class 0 weight = 1
    Class 1 weight = 2
    """
    total_weight = 0
    correct_weight = 0

    for true, pred in zip(y_true, y_pred):
        #weight based on true class
        weight = 2 if true == 1 else 1

        total_weight += weight

        if true == pred:
            correct_weight += weight

    return correct_weight / total_weight


y_true = np.array([0, 1, 1, 0, 1])
y_pred = np.array([0, 1, 0, 0, 1])

score = weighted_accuracy(y_true, y_pred)
print("Weighted Accuracy:", score)
