---
toc: true
toc_label: "Table of Contents"
title: 'Using a Cost Functional to Optimize Hyperparameters Using Cross Validation'
date: 2023-04-20
layout: posts
permalink: posts/2023/04/20/blog-post_using_a_cost_functional_to_optimize_hyperparameters_using_cross_validation
tags: 
  - optimization
  - cross_validation
  - Python
categories:
  - coding
---

This blog post discusses the importance of cost functions in mathematical optimization and how it applies to machine learning problems. The author argues that formulating the optimization of the performance metrics of a machine learning classifier in terms of a cost function is better than optimizing a single metric because it provides a more comprehensive and flexible framework for optimization, can help to address the trade-off between model complexity and performance, and can lead to better performance and generalization. An example of this formulation is provided for a binary classifier.

## What is a cost function?

In mathematical optimization, a cost function is a mathematical function that represents the cost or objective to be minimized or maximized in a given optimization problem. The cost function defines the relationship between the input variables and the output values of the problem. In optimization problems, the goal is to find the input values that minimize or maximize the cost function, subject to certain constraints. The cost function plays a crucial role in defining the optimization problem and in guiding the search for the optimal solution. The choice of the cost function depends on the nature of the problem and the desired optimization criteria. In many real-world problems, the cost function may be a complex, nonlinear function that requires advanced mathematical tools and techniques to be analyzed and optimized.

## Advantages of Using a Cost Functional to Optimize Hyperparameters Using Cross Validation

Formulating the optimization of the performance metrics of a machine learning classifier in terms of a cost function is better than optimizing a single metric for several reasons.

Firstly, machine learning problems often involve multiple metrics that need to be optimized simultaneously, such as accuracy, precision, recall, F1-score, and others. However, optimizing a single metric in isolation may not necessarily lead to the best overall performance of the classifier. For example, optimizing only for accuracy may lead to a model that performs poorly on a specific class or in a specific context.

Secondly, a cost function can provide a more comprehensive and flexible framework for optimization. By defining a cost function that combines multiple metrics and incorporates domain-specific constraints and preferences, we can optimize the model for a specific task and context in a more principled and efficient way.

Thirdly, a cost function can also help to address the trade-off between model complexity and performance. By penalizing complex models that are prone to overfitting, we can ensure that the model is not only accurate but also robust and generalizable.

Overall, formulating the optimization of the performance metrics of a machine learning classifier in terms of a cost function provides a more principled, flexible, and effective approach to model optimization that can lead to better performance and generalization.

## Example

An implementation of this formulation is shown below for a binary classifier.

Import the required libraries.
```python
import sklearn.metrics as sm
from sklearn.datasets import make_classification
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
from collections.abc import Iterable, Callable
import pandas as pd
import numpy as np

from abc import ABC, abstractmethod
```

Define an abstract cost function.
```python
class CostFunction(ABC):
    """Abstract class for cost functions"""
    def __init__(self, metrics: Iterable[str], M: 'np.ndarray[float]') -> None:
        """_summary_

        Args:
            metrics (Iterable[str]): Iterable of strings of the form (metric_name).
            M (np.ndarray[float]): Positive definite matrix of size len(metrics).

        Raises:
            ValueError: _description_

        Returns:
            _type_: _description_
        """
        self.metrics = metrics
        self.M = M or np.identity(len(metrics))  # type: ignore
        self._check_positive_definite(self.M)
    
    @abstractmethod
    def functional(self, y_true: 'np.ndarray[float]', y_pred: 'np.ndarray[float]') -> float:
        """_summary_

        Args:
            y_true (np.ndarray[float]): Array-like of true labels of length N.
            y_pred (np.ndarray[float]): Array-like of predicted labels of length N.
        """
        pass
    
    @staticmethod
    def _to_array(y: Iterable[float]) -> 'np.ndarray[float]':
        return np.fromiter(y, float)
    
    @staticmethod
    def _check_positive_definite(M: 'np.ndarray[float]') -> None:
        if not np.all(np.linalg.eigvals(M) > 0):
            raise ValueError(f'Matrix {M} is not positive definite')

    def make_scorer(self) -> Callable:
        return sm.make_scorer(self.functional, greater_is_better=False)

    def __call__(self, y_true: Iterable[float], y_pred: Iterable[float]) -> float:
        y_pred_array = self._to_array(y_pred)
        y_true_array = self._to_array(y_true)
            
        return self.functional(y_true_array, y_pred_array)
```

Define a specific cost function for a classifier. The default performance metrics to optimize for are accuracy, f1, precision, recall, log loss and rocauc.
```python
class ClassificationCostFunction(CostFunction):
    def __init__(self, metrics: Iterable[str], M: 'np.ndarray[float]' = None, metric_class_opt_val_map: dict[str, tuple[str, float]]=None, proba_threshold: float = 0.5):
        """Defines cost functional for optimization of multiple metrics. 
        Since this is defined as a loss function, cross validation returns the negative of the score [1].

        Args:
            metrics (Iterable[str]): Iterable of strings of the form (metric_name).
            M (np.ndarray[float]): Positive definite matrix of size len(metrics).
            metric_class_map (dict[str, str], optional): Dictionary mapping metric to class or probability of the form {'metric': 'class' or 'proba'}. Defaults to {}.
            proba_threshold (float, optional): Probability threshold used to convert probabilities into classes. Defaults to 0.5.
            
        References:
            [1] https://github.com/scikit-learn/scikit-learn/issues/2439
            
        Example:
            >>> y_true = [0, 0, 0, 1, 1]
            >>> y_pred = [0.46, 0.6, 0.29, 0.25, 0.012]
            >>> threshold = 0.5
            >>> metrics = ["f1_score", "roc_auc_score"]
            >>> cf = ClassificationCostFunction(metrics)
            >>> np.isclose(cf(y_true, y_pred), 1.41, rtol=1e-01, atol=1e-01)
            True
            >>> X, y = make_classification()
            >>> model = LogisticRegression()
            >>> model.fit(X, y)
            >>> y_proba = model.predict_proba(X)[:, 1]
            >>> cost = cf(y, y_proba)
            >>> f1 = getattr(sm, "f1_score")
            >>> roc_auc = getattr(sm, "roc_auc_score")
            >>> y_pred = np.where(y_proba > 0.5, 1, 0)
            >>> scorer_output = np.sqrt((f1(y, y_pred) - 1.0)**2 + (roc_auc(y, y_proba) - 1.0)**2)
            >>> np.isclose(cost, scorer_output)
            True
        """
        super().__init__(metrics, M)
        self.proba_threshold = proba_threshold
        self.metric_class_opt_val_map = metric_class_opt_val_map or {
            "accuracy_score": ("class", 1),
            "f1_score": ("class", 1),
            "log_loss": ("class", 0),
            "precision_score": ("class", 1),
            "recall_score": ("class", 1),
            "roc_auc_score": ("proba", 1),
        }
        
    def _to_class(self, array: 'np.ndarray[float]', metric: str) -> 'np.ndarray[float]':
        # sourcery skip: inline-immediately-returned-variable
        output = np.where(array > self.proba_threshold, 1, 0) if self.metric_class_opt_val_map[metric][0] == "class" else array
        
        return output
    
    
    def functional(self, y_true: 'np.ndarray[float]', y_pred: 'np.ndarray[float]') -> float:
        
        self._check_positive_definite(self.M)

        opt_values = np.array([self.metric_class_opt_val_map[metric][1] for metric in self.metrics])

        metric_values = np.array([getattr(sm, metric)(y_true, self._to_class(y_pred, metric)) for metric in self.metrics])

        return np.sqrt(np.dot(np.dot(metric_values - opt_values, self.M), metric_values - opt_values))
            
```

Run the code in a grid search strategy.
```python
metrics = [
        "accuracy_score",
        "f1_score",
        "log_loss",
        "precision_score",
        "recall_score",
        "roc_auc_score"
]

param_grid = {"C": [0.5, 1]}

scorer = ClassificationCostFunction(metrics, proba_threshold=0.5)
cv = GridSearchCV(LogisticRegression(), param_grid, scoring=scorer.make_scorer())

X, y = make_classification()
cv.fit(X, y)
pd.DataFrame.from_dict(cv.cv_results_)
```

|   mean_fit_time  |   std_fit_time  |   mean_score_time  |   std_score_time  |   param_C   |   params  |   split0_test_score  |   split1_test_score  |   split2_test_score  |   split3_test_score  |   split4_test_score  |   mean_test_score  |   std_test_score  |   rank_test_score  |      |
|------------------|-----------------|--------------------|-------------------|-------------|-----------|----------------------|----------------------|----------------------|----------------------|----------------------|--------------------|-------------------|--------------------|------|
|   0              |   0.009353      |   0.003661         |   0.008929        |   0.002612  |   0.5     |   {'C': 0.5}         |   -1.732076          |   -6.922296          |   -1.732076          |   -3.464335          |   -3.461615        |   -3.462480       |   1.895201         |   1  |
|   1              |   0.006416      |   0.000833         |   0.006427        |   0.000340  |   1       |   {'C': 1}           |   -1.732076          |   -8.654072          |   -1.732076          |   -3.464335          |   -3.461615        |   -3.808835       |   2.543282         |   2  |
|                  |                 |                    |                   |             |           |                      |                      |                      |                      |                      |                    |                   |                    |      |

## Conclusion

In conclusion, cost functions play a critical role in mathematical optimization problems and are essential in guiding the search for the optimal solution. In machine learning problems, where multiple performance metrics need to be optimized simultaneously, using a cost function provides a more principled and efficient way to optimize the model for a specific task and context. Furthermore, it helps to address the trade-off between model complexity and performance, ensuring that the model is not only accurate but also robust and generalizable. By using a cost function to optimize performance metrics, machine learning practitioners can achieve better performance and generalization on their models, making it a valuable tool for model optimization.