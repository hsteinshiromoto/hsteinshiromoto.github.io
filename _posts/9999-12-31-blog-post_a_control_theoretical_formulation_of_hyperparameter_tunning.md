---
title: 'A Control Theoretical Formulation of Hyperparameter Tunning'
date: 9999-12-31
layout: posts
permalink: posts/9999/12/31/blog-post_a_control_theoretical_formulation_of_hyperparameter_tunning
tags: 
  - control theory
  - machine learning
  - hyperparameter tunning
  - optimization
categories:
  - mathematics
---

In the development of a machine learning model, its hyperparameters are optimized to obtain the best performance metric of choice. In this post, we will discuss how to fomulate the search of these hyperparameters in terms of a control theorical problem. The advantage of this formulation is to be able to use the current model performance metric as a feedback to improve the search of the optimal hyperparameter.

Let $f$ represent a model in consideration, $\hat{y}$ be the prediction of $f$ on the predictors $x$ and $\theta$ be the hyperparameters of $f$. Then, we define $\hat{y}=f(x,\theta)$. Let also $p:\mathbb{R}^n \to \mathbb{R}$ be the performance metric of $f$, and $y$ be the true target associated with the predictors $x$. Then, we define $p(f,y,\hat{y},\theta)$.

The difference equation that describes the new model is given by
$$f_+=S(f,\theta)$$
where $S$ is the system that trains new models.

The hyperparameter $\theta$ is calculated by the controller $C$ that takes the error $e$ as input and outputs the new hyperparameter $\theta$
$$\theta=C(e)$$