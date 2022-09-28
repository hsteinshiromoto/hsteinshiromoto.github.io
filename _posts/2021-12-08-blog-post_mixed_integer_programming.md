---
title: 'Mixed Integer Programming'
date: 2021-12-08
layout: posts
permalink: posts/2021/12/08/blog-post_mixed_integer_programming
categories: 
  - mathematics
tags:
  - optimization
  - gurobi
  - python
---

Mixed Integer Programming (MIP) are a form of optimization that is formulated using a combination of equations that are continous and discrete.

MIPs typically appear when one or more decision variable is boolean, ie, assume value 0 or 1. This type of optimization problem is formulated as, find $x\in\mathbb{R}^n$ such that

$$\begin{array}{rll}
\min& x^T Q x + q^Tx\\
\text{subject to}& l \leq x \leq u & (\text{bound constraints})\\
&x^T Q x + q^T x \leq b & (\text{quadratic constraints})\\
&\exists i\in[1,n]\subset\mathbb{N}\text{ such that } x_i\in\mathbb{Z} &(\text{integrality constraints}),
\end{array}$$

where $x=(x_1,\ldots,x_n)$ is the vector of decision variables, $Q\in\mathbb{R}^{n\times n}$ is the matrix of coefficients of the objective function, $q\in\mathbb{R}^n$ is the vector of coefficients of the linear part of the objective function, $l\in\mathbb{R}^n$ is the vector of lower bounds, $u\in\mathbb{R}^n$ is the vector of upper bounds, and $b\in\mathbb{R}^n$ is the vector of the right-hand side of the quadratic constraints.

An example of the implementation of the above formulation is shown in the notebook below.

{% gist 20e5d8fa03362a6e12dd5d8cdc4165df %}