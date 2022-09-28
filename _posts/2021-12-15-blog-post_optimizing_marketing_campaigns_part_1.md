---
title: 'Optimizing Marketing Campaigns Part 1: Clustering'
date: 2021-12-15
layout: posts
permalink: posts/2021/12/15/blog-post_optimizing_marketing_campaigns_part_1
tags: 
  - marketing
  - optimization
  - mixed integer programming
  - python
  - gurobi
categories:
  - case study
---

In this series of posts, we analyze how to maximize the profit of marketing campaigns using mathematical optimization techniques. In the first part, we use optimize the profit of campaign for a cluster of customers. To do this, we model the profit and cost of the campaigns of two products. Furthermore, the constraints on maximum number of offers, budget and return on investment are also modelled and considered to maximize the profit.

- [1. Modelling the Profit](#1-modelling-the-profit)
- [2. Modelling the Constraints](#2-modelling-the-constraints)
  - [2.1. Maximum Number of Offers for each Cluster](#21-maximum-number-of-offers-for-each-cluster)
  - [2.2. Maximum Budget](#22-maximum-budget)
  - [2.3. Minimum Number of Offers of each Product](#23-minimum-number-of-offers-of-each-product)
  - [2.4. Minimum ROI](#24-minimum-roi)
  - [2.5. Recap of the Optimization Model](#25-recap-of-the-optimization-model)
- [3. Data](#3-data)
- [4. Python Implementation](#4-python-implementation)
- [5. In the Next Post](#5-in-the-next-post)
- [6. References](#6-references)

The estimated individual expected profit can be determined with machine learning models. For example, a response model such as uplift model can be used to estimate the individual expected profit.

The key idea is to cluster the estimated individual expected profits and then consider the cluster centroids as representative of the data for all the individual customers within a single cluster. This aggregation enables the problem to be formulated as a linear programming problem so that rather than assigning offers to individual customers, the model identifies proportions within each cluster for each product offer that maximizes the marketing campaign return on investment while considering the business constraints. 

From the technical viewpoint, the model is formulated as a [mixed-integer linear programming](https://hsteinshiromoto.github.io/posts/2021/12/08/blog-post_mixed_integer_programming) problem. 

# 1. Modelling the Profit

Maximize total expected profit from marketing campaign and heavily penalize any correction to the budget. Let $K$ be the set of clusters and $J$ the set of products, we define the profit function as

$$
\max_{y,z} \sum_{k \in K} \sum_{j \in J} \pi_{k,j} \cdot y_{k,j} - M \cdot z\;
\tag{Profit}
$$
where

* $\pi_{k,j}$: is the expected profit to the bank from the offer of product $j \in J$ to an average customer of cluster $k \in K$.

* $y_{k,j} \geq 0$: is the number of customers in cluster $k \in K$ that are offered product $j \in J$.

* $M$: Big M penalty. This penalty is associated with corrections on the budget that are necessary to satisfy other business constraints.

* $z \geq 0$: Increase in budget in order to have a feasible campaign.

# 2. Modelling the Constraints

## 2.1. Maximum Number of Offers for each Cluster
Maximum number of offers of products for each cluster is limited by the number of customers in the cluster.

$$
\sum_{j \in J} y_{k,j} \leq N_{k} \quad \forall k \in K\;,
\tag{Max Number of Offers}
$$
where $N_k$ is the number of customers in cluster $k \in K$.

## 2.2. Maximum Budget
The marketing campaign budget constraint enforces that the total cost of the campaign should be less than the budget campaign. There is the possibility of increasing the budget to ensure the feasibility of the model, the minimum number of offers for all the product may require this increase in the budget.

$$
\sum_{k \in K} \sum_{j \in J} \nu_{k,j} \cdot y_{k,j} \leq B + z\;,
\tag{Max Budget}
$$
where $\nu_{k,j}$ is the average variable cost associated with the offer of product $j \in J$ to an average customer of cluster $k \in K$ and $B$ is the marketing campaign budget.

## 2.3. Minimum Number of Offers of each Product

Minimum number of offers of each product.

$$
\sum_{k \in K} y_{k,j} \geq Q_{j}  \quad \forall j \in J\;,
\tag{Min Number of Offers}
$$
where $Q_j$ is the minimum number of offers of product $j \in J$ to be made.

## 2.4. Minimum ROI

The minimum ROI constraint ensures that the ratio of total profits over cost is at least one plus the corporate hurdle rate.

$$
\sum_{k \in K} \sum_{j \in J} \pi_{k,j} \cdot y_{k,j} \geq (1+R) \cdot \sum_{k \in K} \sum_{j \in J} \nu_{k,j} \cdot y_{k,j}\;,
\tag{Minimum ROI}
$$
where $R$ is the corporate hurdle rate. This hurdle rate is used for the ROI calculation of the marketing campaign.

## 2.5. Recap of the Optimization Model

The optimization model is formulated as a mixed-integer linear programming problem. The objective function is defined as the maximum expected profit from the marketing campaign. The constraints are defined as the maximum number of offers of each product for each cluster, the budget, the minimum ROI, and the minimum number of offers of each product.

$$\begin{array}{rlr}
\max_{y,z}&\sum_{k \in K} \sum_{j \in J} \pi_{k,j} \cdot y_{k,j} - M \cdot z&\text{(Profit)}\\
\text{s.t.}&\sum_{j \in J} y_{k,j} \leq N_{k} \quad \forall k \in K&\text{(Max Number of Offers)}\\
&\sum_{k \in K} \sum_{j \in J} \nu_{k,j} \cdot y_{k,j} \leq B + z&\text{(Max Budget)}\\
&\sum_{k \in K} y_{k,j} \geq Q_{j}&\text{(Min Number of Offers)}\\
&\sum_{k \in K} \sum_{j \in J} \pi_{k,j} \cdot y_{k,j} \geq (1+R) \cdot \sum_{k \in K} \sum_{j \in J} \nu_{k,j} \cdot y_{k,j}&\text{(Minimum ROI)}
\end{array}$$

# 3. Data

We consider two products, ten customers, and two clusters of customers. The corporate hurdle-rate is twenty percent.

The following table defines the expected profit of an average customer in each cluster when offered a product.

| <i></i> | Product 1 | Product 2 |
| --- | --- |  --- |
| cluster 1 | $2 000 | $1 000 |
| cluster 2 | $3 000 | $2 000 |

The expected cost of offering a product to an average customer in a cluster is determined by the following table.

| <i></i> | Product 1 | Product 2 |
| --- | --- |  --- |
| cluster 1 | $200 | $100 |
| cluster 2 | $300 | $200 |

The budget available for the marketing campaign is $200.

The number of customers in each cluster is given by the following table.

| <i></i> | Num. Customers | 
| --- | --- |
| cluster 1 | 5 |
| cluster 2 | 5 | 

The minimum number of offers of each product is provided in the following table,

| <i></i> | Min Offers | 
| --- | --- |
| product 1 | 2 |
| product 2 | 2 | 

# 4. Python Implementation

<div class="fluidMedia" style="height: 100vh;">
    <iframe src="https://nbviewer.org/github/hsteinshiromoto/blog/blob/master/posts/2021-12-31-blog-post_optimizing_marketing_campaigns_part_1/2021-12-31-blog-post_optimizing_marketing_campaigns_part_1.ipynb" style='height: 100%; width: 100%;' frameborder="0" id="iframe"> </iframe>
</div>

# 5. In the Next Post

We will learn how to optimize the campaigns at an individual customer level.

# 6. References

* https://gurobi.github.io/modeling-examples/marketing_campaign_optimization/marketing_campaign_optimization.html

* M.-D. Cohen, "*Exploiting response models—optimizing cross-sell and up-sell opportunities in banking*", Information Systems 29 (2004) 327–341