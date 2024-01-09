import pandas as pd
from sklearn.metrics import confusion_matrix, accuracy_score, roc_auc_score
import numpy as np

## helpers
def _make_grouped_confusion_matrices(df, protected_attribute, privileged_group, labels, positive_label, y_true, normalize=None):
    """
    Returns confusion matrices for priv and unpriv groups

    Args:
        df (pandas.DataFrame): The DataFrame containing the data.
        protected_attribute (str): The name of the protected attribute column.
        privileged_group: The privileged group value in the protected attribute column.
        labels (str): The name of the selected column for labels.
        positive_label: a label that indicates a positive outcome
        y_true (pandas.DataFrame): pandas DataFrame holding correct predictions
        normalize (str): either None meaning confusion matrices are in tp, fp, etc. 'true' if tpr, fpr, etc

    Returns:
        tuple: (cm of priv, cm of unpriv)
    """
    privileged_df = df[df[protected_attribute] == privileged_group]
    y_pred_priviledged = privileged_df[labels]
    unprivileged_df = df[df[protected_attribute] != privileged_group]
    y_pred_unpriviledged = unprivileged_df[labels]

    priviledged_yt = y_true[y_true[protected_attribute] == privileged_group]
    y_true_priviledged = priviledged_yt[labels]
    unprivileged_yt = y_true[y_true[protected_attribute] != privileged_group]
    y_true_unpriviledged = unprivileged_yt[labels]

    # print(y_true_priviledged, y_pred_priviledged)
    # print(y_true_unpriviledged, y_pred_unpriviledged)
    cm_priv = confusion_matrix(y_true_priviledged, y_pred_priviledged, normalize=normalize)
    cm_unpriv = confusion_matrix(y_true_unpriviledged, y_pred_unpriviledged, normalize=normalize)
    return (cm_priv, cm_unpriv)



def _calculate_priv_unpriv_difference(df, protected_attribute, privileged_group, labels, positive_label, y_true, metric_func):
    """
    Calculate the difference between a given metric for the privileged and unprivileged groups in a dataset.

    Args:
        df (pandas.DataFrame): The input dataset.
        protected_attribute (str): The name of the protected attribute column.
        privileged_group (any): The value of the protected attribute that denotes the privileged group.
        labels (str): The name of the column containing the predicted labels.
        positive_label (any): The value of the positive label.
        y_true (pandas.Series): The true labels.
        metric_func (callable): The metric function to use (e.g., f1_score, roc_auc_score).

    Returns:
        float: The difference between the metric calculated on the privileged and unprivileged groups.
    """
    privileged_group_df = df[df[protected_attribute] == privileged_group]
    unprivileged_group_df = df[df[protected_attribute] != privileged_group]

    # Extract 'labels' column for privileged and unprivileged groups
    y_pred_privileged = privileged_group_df[labels]
    y_true_privileged = y_true[y_true.index.isin(privileged_group_df.index)][labels]
    y_pred_unprivileged = unprivileged_group_df[labels]
    y_true_unprivileged = y_true[y_true.index.isin(unprivileged_group_df.index)][labels]

    # Calculate metric for privileged and unprivileged groups
    metric_privileged = metric_func(y_true_privileged, y_pred_privileged, positive_label=positive_label)
    metric_unprivileged = metric_func(y_true_unprivileged, y_pred_unprivileged, positive_label=positive_label)

    # Calculate metric difference
    metric_difference = metric_privileged - metric_unprivileged

    return metric_difference



## preliminary definitions using df and y_true
def positive_predicted_value(df, protected_attribute, privileged_group, labels, positive_label, y_true, **kwargs):
    """
    Returns positive_predicted_value for priv and unpriv groups

    Args:
        df (pandas.DataFrame): The DataFrame containing the data.
        protected_attribute (str): The name of the protected attribute column.
        privileged_group: The privileged group value in the protected attribute column.
        labels (str): The name of the selected column for labels.
        positive_label: a label that indicates a positive outcome
        y_true (pandas.DataFrame): pandas DataFrame holding correct predictions

    Returns:
        tuple: (PPV of priv, PPV of unpriv)
    """
    (cm_priv, cm_unpriv) = _make_grouped_confusion_matrices(df, protected_attribute, privileged_group, labels, positive_label, y_true)
    # TP / (TP + FP)
    priv_return = cm_priv[1][1] / (cm_priv[1][1] + cm_priv[0][1])
    unpriv_return = cm_unpriv[1][1] / (cm_unpriv[1][1] + cm_unpriv[0][1])
    return (priv_return, unpriv_return)



def false_discovery_rate(df, protected_attribute, privileged_group, labels, positive_label, y_true, **kwargs):
    """
    Returns false_discovery_rate for priv and unpriv groups

    Args:
        df (pandas.DataFrame): The DataFrame containing the data.
        protected_attribute (str): The name of the protected attribute column.
        privileged_group: The privileged group value in the protected attribute column.
        labels (str): The name of the selected column for labels.
        positive_label: a label that indicates a positive outcome
        y_true (pandas.DataFrame): pandas DataFrame holding correct predictions

    Returns:
        tuple: (FDR of priv, FDR of unpriv)
    """
    (cm_priv, cm_unpriv) = _make_grouped_confusion_matrices(df, protected_attribute, privileged_group, labels, positive_label, y_true)
    # FP / (FP + TP)
    priv_return = cm_priv[0][1] / (cm_priv[1][1] + cm_priv[0][1])
    unpriv_return = cm_unpriv[0][1] / (cm_unpriv[1][1] + cm_unpriv[0][1])
    return (priv_return, unpriv_return)



def negative_predictive_value(df, protected_attribute, privileged_group, labels, positive_label, y_true, **kwargs):
    """
    Returns negative_predictive_value for priv and unpriv groups

    Args:
        df (pandas.DataFrame): The DataFrame containing the data.
        protected_attribute (str): The name of the protected attribute column.
        privileged_group: The privileged group value in the protected attribute column.
        labels (str): The name of the selected column for labels.
        positive_label: a label that indicates a positive outcome
        y_true (pandas.DataFrame): pandas DataFrame holding correct predictions

    Returns:
        tuple: (NPV of priv, NPV of unpriv)
    """
    (cm_priv, cm_unpriv) = _make_grouped_confusion_matrices(df, protected_attribute, privileged_group, labels, positive_label, y_true)
    # TN / (TN + FN)
    priv_return = cm_priv[0][0] / (cm_priv[1][0] + cm_priv[0][0])
    unpriv_return = cm_unpriv[0][0] / (cm_unpriv[1][0] + cm_unpriv[0][0])
    return (priv_return, unpriv_return)



def false_omission_rate(df, protected_attribute, privileged_group, labels, positive_label, y_true, **kwargs):
    """
    Returns false_omission_rate for priv and unpriv groups

    Args:
        df (pandas.DataFrame): The DataFrame containing the data.
        protected_attribute (str): The name of the protected attribute column.
        privileged_group: The privileged group value in the protected attribute column.
        labels (str): The name of the selected column for labels.
        positive_label: a label that indicates a positive outcome
        y_true (pandas.DataFrame): pandas DataFrame holding correct predictions

    Returns:
        tuple: (FOR of priv, FOR of unpriv)
    """
    (cm_priv, cm_unpriv) = _make_grouped_confusion_matrices(df, protected_attribute, privileged_group, labels, positive_label, y_true)
    # FN / (TN + FN)
    priv_return = cm_priv[1][0] / (cm_priv[1][0] + cm_priv[0][0])
    unpriv_return = cm_unpriv[1][0] / (cm_unpriv[1][0] + cm_unpriv[0][0])
    return (priv_return, unpriv_return)



## metrics just using predicted values (df)
def selection_rate(data, positive_label):
    """
    Calculate the selection rate for a column in a DataFrame based on a positive label.

    Args:
        data (pandas.Series): The column data.
        positive_label: The positive label to calculate the selection rate for.

    Returns:
        float: The selection rate as a proportion between 0 and 1.

    Example:
        df = pd.DataFrame(data)
        privileged_df = df[df[protected_attribute] == privileged_group]
        privileged_selection_rate = selection_rate(privileged_df[labels], positive_label)
    """
    total_samples = len(data)
    positive_samples = sum(data == positive_label)

    return positive_samples / total_samples



def parity_vals(df, protected_attribute, privileged_group, labels, positive_label, **kwargs):
    """
    Calculate the parity difference for a selected column based on the protected attribute and privileged group.

    Args:
        df (pandas.DataFrame): The DataFrame containing the data.
        protected_attribute (str): The name of the protected attribute column.
        privileged_group: The privileged group value in the protected attribute column.
        labels (str): The name of the selected column for labels.
        positive_label: a label that indicates a positive outcome

    Returns:
        (parity_difference, parity_ratio)
    """
    return (parity_difference(df, protected_attribute, privileged_group, labels, positive_label), parity_ratio(df, protected_attribute, privileged_group, labels, positive_label))



def parity_difference(df, protected_attribute, privileged_group, labels, positive_label, **kwargs):
    """
    Calculate the parity difference for a selected column based on the protected attribute and privileged group.

    Args:
        df (pandas.DataFrame): The DataFrame containing the data.
        protected_attribute (str): The name of the protected attribute column.
        privileged_group: The privileged group value in the protected attribute column.
        labels (str): The name of the selected column for labels.
        positive_label: a label that indicates a positive outcome

    Returns:
        float: The parity difference as a proportion between -1 and 1.
    """
    privileged_df = df[df[protected_attribute] == privileged_group]
    privileged_selection_rate = selection_rate(privileged_df[labels], positive_label)

    unprivileged_df = df[df[protected_attribute] != privileged_group]
    unprivileged_selection_rate = selection_rate(unprivileged_df[labels], positive_label)

    return privileged_selection_rate - unprivileged_selection_rate



def parity_ratio(df, protected_attribute, privileged_group, labels, positive_label, **kwargs):
    """
    Calculate the parity difference for a selected column based on the protected attribute and privileged group.

    Args:
        df (pandas.DataFrame): The DataFrame containing the data.
        protected_attribute (str): The name of the protected attribute column.
        privileged_group: The privileged group value in the protected attribute column.
        labels (str): The name of the selected column for labels.
        positive_label: a label that indicates a positive outcome

    Returns:
        float: The parity ratio as a proportion between 0 and 1.
    """
    privileged_df = df[df[protected_attribute] == privileged_group]
    privileged_selection_rate = selection_rate(privileged_df[labels], positive_label)

    unprivileged_df = df[df[protected_attribute] != privileged_group]
    unprivileged_selection_rate = selection_rate(unprivileged_df[labels], positive_label)

    return privileged_selection_rate / unprivileged_selection_rate



## metrics using df and y_true
def predictive_parity(df, protected_attribute, privileged_group, labels, positive_label, y_true, **kwargs):
    """
    Calculates PPV difference and ratio between priv and unpriv groups

    Args:
        df (pandas.DataFrame): The DataFrame containing the data.
        protected_attribute (str): The name of the protected attribute column.
        privileged_group: The privileged group value in the protected attribute column.
        labels (str): The name of the selected column for labels.
        positive_label: a label that indicates a positive outcome
        y_true (pandas.DataFrame): pandas DataFrame holding correct predictions

    Returns:
        tuple: PPV difference, PPV ratio
    """
    (ppv_priv, ppv_unpriv) = positive_predicted_value(df, protected_attribute, privileged_group, labels, positive_label, y_true)
    return (ppv_priv - ppv_unpriv, ppv_priv / ppv_unpriv)



def conditional_use_accuracy_difference(df, protected_attribute, privileged_group, labels, positive_label, y_true, **kwargs):
    """
    Calculates total difference between ppv and npv for priv and unpriv group

    Args:
        df (pandas.DataFrame): The DataFrame containing the data.
        protected_attribute (str): The name of the protected attribute column.
        privileged_group: The privileged group value in the protected attribute column.
        labels (str): The name of the selected column for labels.
        positive_label: a label that indicates a positive outcome
        y_true (pandas.DataFrame): pandas DataFrame holding correct predictions

    Returns:
        float: total difference between ppv and npv for priv and unpriv group
    """
    (ppv_priv, ppv_unpriv) = positive_predicted_value(df, protected_attribute, privileged_group, labels, positive_label, y_true)
    (npv_priv, npv_unpriv) = negative_predictive_value(df, protected_attribute, privileged_group, labels, positive_label, y_true)
    return ppv_priv - ppv_unpriv + npv_priv - npv_unpriv



def treatment_equality(df, protected_attribute, privileged_group, labels, positive_label, y_true, **kwargs):
    """
    Calculates FN / FP for priv and unpriv groups

    Args:
        df (pandas.DataFrame): The DataFrame containing the data.
        protected_attribute (str): The name of the protected attribute column.
        privileged_group: The privileged group value in the protected attribute column.
        labels (str): The name of the selected column for labels.
        positive_label: a label that indicates a positive outcome
        y_true (pandas.DataFrame): pandas DataFrame holding correct predictions

    Returns:
        tuple: FN / FP for priv and unpriv groups
    """
    (cm_priv, cm_unpriv) = _make_grouped_confusion_matrices(df, protected_attribute, privileged_group, labels, positive_label, y_true)
    # FN / FP
    priv_ret = cm_priv[1][0] / cm_priv[0][1]
    unpriv_ret = cm_unpriv[1][0] / cm_unpriv[0][1]
    return (priv_ret, unpriv_ret)



def equal_odds_difference(df, protected_attribute, privileged_group, labels, positive_label, y_true, **kwargs):
    """
    Calculates equal_odds_difference between privileged_group and unpr

    Args:
        df (pandas.DataFrame): The DataFrame containing the data.
        protected_attribute (str): The name of the protected attribute column.
        privileged_group: The privileged group value in the protected attribute column.
        labels (str): The name of the selected column for labels.
        positive_label: a label that indicates a positive outcome
        y_true (pandas.DataFrame): pandas DataFrame holding correct predictions

    Returns:
        float: the equal odds difference between privileged group and unpr

    Example:
        df = pd.DataFrame(data)
        y_true = pd.DataFrame(data_true)
        protected_attribute = 'gender'
        privileged_group = 'male'
        selected_column = 'hired'
        positive_label = True
        eod = equal_odds_difference(df, protected_attribute, privileged_group, labels, positive_label, y_true)
    """
    (cm_priv, cm_unpriv) = _make_grouped_confusion_matrices(df, protected_attribute, privileged_group, labels, positive_label, y_true, normalize='true')
    return cm_priv[1][1] - cm_unpriv[1][1]



def average_odds_difference(df, protected_attribute, privileged_group, labels, positive_label, y_true, **kwargs):
    """
    Calculates average_odds_difference between privileged_group and unpr

    Args:
        df (pandas.DataFrame): The DataFrame containing the data.
        protected_attribute (str): The name of the protected attribute column.
        privileged_group: The privileged group value in the protected attribute column.
        labels (str): The name of the selected column for labels.
        positive_label: a label that indicates a positive outcome
        y_true (pandas.Data): pandas DataFrame holding correct predictions

    Returns:
        float: the average odds difference between privileged group and unpr

    Example:
        df = pd.DataFrame(data)
        y_true = pd.DataFrame(data_true)
        protected_attribute = 'gender'
        privileged_group = 'male'
        selected_column = 'hired'
        positive_label = True
        eod = average_odds_difference(df, protected_attribute, privileged_group, labels, positive_label, y_true)
    """
    (cm_priv, cm_unpriv) = _make_grouped_confusion_matrices(df, protected_attribute, privileged_group, labels, positive_label, y_true, normalize='true')
    tpr_diff = cm_priv[1][1] - cm_unpriv[1][1]
    fpr_diff = cm_priv[0][1] - cm_unpriv[0][1]
    return (tpr_diff + fpr_diff) / 2



def average_odds_ratio(df, protected_attribute, privileged_group, labels, positive_label, y_true, **kwargs):
    """
    Calculates average_odds_ratio between privileged_group and unpr

    Args:
        df (pandas.DataFrame): The DataFrame containing the data.
        protected_attribute (str): The name of the protected attribute column.
        privileged_group: The privileged group value in the protected attribute column.
        labels (str): The name of the selected column for labels.
        positive_label: a label that indicates a positive outcome
        y_true (pandas.Data): pandas DataFrame holding correct predictions

    Returns:
        float: the average odds ratio between privileged group and unpr

    Example:
        df = pd.DataFrame(data)
        y_true = pd.DataFrame(data_true)
        protected_attribute = 'gender'
        privileged_group = 'male'
        selected_column = 'hired'
        positive_label = True
        eod = average_odds_ratio(df, protected_attribute, privileged_group, labels, positive_label, y_true)
    """
    (cm_priv, cm_unpriv) = _make_grouped_confusion_matrices(df, protected_attribute, privileged_group, labels, positive_label, y_true, normalize='true')
    tpr_ratio = cm_priv[1][1] / cm_unpriv[1][1]
    fpr_ratio = cm_priv[0][1] / cm_unpriv[0][1]
    return (tpr_ratio + fpr_ratio) / 2



def overall_accuracy(df, labels, y_true, **kwargs):
    """
    Calculate overall accuracy of df compared to y_true

    Args:
        df (pandas.DataFrame): The DataFrame containing the data.
        labels (str): The name of the selected column for labels.
        y_true (pandas.DataFrame): pandas DataFrame holding correct predictions

    Returns:
        float: the accuracy difference between priv and unpriv groups

    Example:
        df = pd.DataFrame(data)
        y_true = pd.DataFrame(data_true)
        protected_attribute = 'gender'
        privileged_group = 'male'
        labels = 'hired'
        positive_label = True
        ac = overall_accuracy(df, labels, y_true)
    """
    return accuracy_score(y_true[labels], df[labels])



def accuracy_difference(df, protected_attribute, privileged_group, labels, positive_label, y_true, **kwargs):
    """
    Calculates the difference in accuracy between the privileged and unprivileged groups for a given binary classification
    problem.

    Args:
        df (pandas.DataFrame): The dataset.
        protected_attribute (str): The column name of the protected attribute.
        privileged_group (any): The privileged group for the protected attribute.
        labels (str): The column name of the predicted labels.
        positive_label (any): The positive label (usually True or 1).
        y_true (pandas.Series): The ground truth labels.

    Returns:
        float: The difference in accuracy between the privileged and unprivileged groups.
    """
    return _calculate_priv_unpriv_difference(df, protected_attribute, privileged_group, labels, positive_label, y_true, (lambda x, y, **kwargs: accuracy_score(x, y)))



## inequality
def gini_coefficient(df, scores=None, **kwargs):
    """
    Calculate the Gini coefficient for the given scores and protected attribute.

    Args:
        df (pandas.DataFrame): The DataFrame containing the data.
        protected_attribute (str): The name of the protected attribute column.
        privileged_group (any): The privileged group value in the protected attribute column.
        scores (str): The name of the selected column for scores.

    Returns:
        tuple: (Gini coefficient of priv, Gini coefficient of unpriv)

    Raises:
        ValueError: If the scores column is not present
    """
    if scores is None:
        raise ValueError('scores was not provided')
    
    def gini(x):
        total = 0
        for i, xi in enumerate(x[:-1], 1):
            total += np.sum(np.abs(xi - x[i:]))
        return total / (len(x)**2 * np.mean(x))

    return gini(df[scores])



def theil_index(df, protected_attribute, privileged_group, scores=None, **kwargs):
    """
    Calculates the Theil index for a given dataset, protected attribute, and privileged group.

    Args:
        df (pandas.DataFrame): The DataFrame containing the data.
        protected_attribute (str): The name of the protected attribute column.
        privileged_group (str): The value of the privileged group in the protected attribute column.
        scores (str): The name of the column containing the scores.
        **kwargs: Additional keyword arguments to be passed to the function.

    Returns:
        float: The Theil index.

    Raises:
        ValueError: If the scores column is not present
    """
    if scores is None:
        raise ValueError('scores was not provided')

    priv_scores = df.loc[df[protected_attribute] == privileged_group][scores]
    unpriv_scores = df.loc[df[protected_attribute] != privileged_group][scores]

    priv_count = priv_scores.count()
    unpriv_count = unpriv_scores.count()

    priv_mean = priv_scores.mean()
    unpriv_mean = unpriv_scores.mean()

    priv_norm = priv_scores / priv_mean
    unpriv_norm = unpriv_scores / unpriv_mean

    priv_ln = priv_norm.apply(np.log)
    unpriv_ln = unpriv_norm.apply(np.log)

    priv_sum = priv_norm * priv_ln
    unpriv_sum = unpriv_norm * unpriv_ln

    priv_term = (priv_sum.sum() / priv_count) if priv_count > 0 else 0
    unpriv_term = (unpriv_sum.sum() / unpriv_count) if unpriv_count > 0 else 0

    theil_index = priv_term - unpriv_term

    return theil_index



def _f1_score(y_true, y_pred, positive_label):
    """
    Calculate the F1 score for a binary classification problem.

    Args:
        y_true (array-like): Ground truth labels.
        y_pred (array-like): Predicted labels.
        positive_label (any): Positive label (usually True or 1)

    Returns:
        float: The F1 score.
    """
    tp = sum((yt == positive_label and yp == positive_label) for yt, yp in zip(y_true, y_pred))
    fp = sum((yt != positive_label and yp == positive_label) for yt, yp in zip(y_true, y_pred))
    fn = sum((yt == positive_label and yp != positive_label) for yt, yp in zip(y_true, y_pred))

    if tp == 0:
        return 0

    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    f1 = 2 * precision * recall / (precision + recall)

    return f1



def f1_score(df, labels, positive_label, y_true, **kwargs):
    """
    Calculate the F1 score for binary classification.

    Args:
        df (pandas.DataFrame): The input dataframe.
        labels (str): The name of the column containing the predicted labels.
        positive_label (any): The value representing the positive label.
        y_true (pandas.DataFrame): The true df.

    Returns:
        float: The F1 score.

    Example:
        data = pd.DataFrame({'labels': [0, 1, 1, 0], 'predictions': [0, 1, 1, 0]})
        true_labels = data['labels']
        predicted_labels = data['predictions']
        score = f1_score(data, 'predictions', 1, true_labels)
    """
    return _f1_score(y_true[labels], df[labels], positive_label)



def predictive_equality(df, protected_attribute, privileged_group, labels, positive_label, y_true, **kwargs):
    """
    Calculate the difference in F1 score between a privileged group and an unprivileged group.

    Args:
        df (pandas DataFrame): The dataset.
        protected_attribute (str): The name of the protected attribute column.
        privileged_group (any): The privileged group value for the protected attribute.
        labels (str): The name of the predicted label column.
        positive_label (any): The positive label value.
        y_true (pandas Series): The true label values.

    Returns:
        float: The difference in F1 score.
    """
    return _calculate_priv_unpriv_difference(df, protected_attribute, privileged_group, labels, positive_label, y_true, _f1_score)



def roc_auc_difference(df, protected_attribute, privileged_group, labels, positive_label, y_true, **kwargs):
    """
    Calculate the difference in ROC AUC score between the privileged group and the unprivileged group.

    Args:
        df (pandas.DataFrame): Dataset.
        protected_attribute (str): Name of the protected attribute column.
        privileged_group (any): Value of the privileged group.
        labels (str): Name of the column containing predicted scores.
        positive_label (any): Value of the positive label.
        y_true (array-like): Ground truth labels.

    Returns:
        float: The difference in ROC AUC score between the privileged group and the unprivileged group.
    """
    return _calculate_priv_unpriv_difference(df, protected_attribute, privileged_group, labels, positive_label, y_true, (lambda x, y, **kwargs: roc_auc_score(x, y)))



def roc_auc(df, labels, y_true, **kwargs):
    """
    Calculate the ROC AUC (Area Under the Receiver Operating Characteristic Curve) score.

    Args:
        df (pandas.DataFrame): The input dataframe.
        labels (str): The name of the column containing the predicted labels.
        y_true (pandas.DataFrame): The true labels.

    Returns:
        float: The ROC AUC score.

    Example:
        data = pd.DataFrame({'labels': [0, 1, 1, 0], 'predictions': [0.2, 0.8, 0.6, 0.4]})
        true_labels = data['labels']
        predicted_labels = data['predictions']
        score = roc_auc(data, 'predictions', true_labels)
    """
    return roc_auc_score(y_true[labels], df[labels])
