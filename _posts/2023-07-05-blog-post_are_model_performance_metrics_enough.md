---
title: "Are Model Performance Metrics Enough?"
date: 2023-07-05
permalink: posts/2023/07/05/are_model_performance_metrics_enough
categories: 
  - management
  - opinion
  - machine learning
  - performance
  - evaluation
toc: true
toc_label: "Table of Contents"
toc_sticky: true
---

My model has a "good enough" performance, is this sufficient for deployment? This post highlights the limitations of relying solely on performance metrics when assessing the readiness of a machine learning model for deployment. It emphasizes the importance of considering both correctness and performance as separate components in the evaluation process. By visualizing the relationship between correctness and performance in different regions, the blog post illustrates the need for critical evaluation and avoiding overconfidence in performance metrics. Furthermore, it emphasizes the impact of business assumptions on correctness and stresses the significance of scientifically-based decision-making.

# Introduction

In general, we are inclined to assume that if the performance metrics of a model is above a certain threshold, then it is ready to be moved to the next stage of the development. As I show in this blog post, we must be more critical about this criterion, because performance metric only measures a part of a data science problem.


While working in a project in which the main deliverable is a machine learning model, the data scientist frequently needs to answer the question if the model performance is good enough. Implicitly, it is assumed that the metric chosen to measure the model performance also captures all the pieces of information about the of the process that generate the data and its characteristics such as distribution, dependencies etc. This assumption can be understood as the causal relationship: if the performance metrics is high, then the model is correct.

An illustration for the aforementioned implicit assumption is shown in the figure below

![Causal relationship between model performance and correcteness](https://raw.githubusercontent.com/hsteinshiromoto/blog/dev/images/are_model_performance_metrics_enough/correctnessvsperformance.svg)

If such a causal relationship is true, then a high performance necessarily implies that the predictions obtained from the model correspond to th reality. To see why this assumption is strong, one can verify that a performance metric is not a sufficient condition for a good prediction, otherwise we would never face problems such as target leakage, and overfitting.

# Perfomance x Correcteness

Since we know that the model performance metric does not encapsulate all the pieces of information that are necessary to decided if a model is good enough for deployment, we need to understand what we can and cannot decided based on the performance metric, and what pieces of information are missing to make that decision. I propose to decompose the question "Is the model performance metric good enough to deployment?" into two components:

1. Correcteness: How correct is the scientific methodology used to build the model?
2. Performance: How can I improve the model performance?

We also need to keep in mind that the performance metric does not necessarily increase with the more correct the model methodology is. For example, IT/coding issues can lead to poor model performance.

Based on the above, we can visualize the relationship between correcteness and performance in a Cartesian plane below

![Regions divisions](https://raw.githubusercontent.com/hsteinshiromoto/blog/dev/images/are_model_performance_metrics_enough/correctnessvsperformance_regions.svg)

The regions can be described as follows:

* **Start Region**. This is where the data science work normally starts. With poor knowledge of the data or the modelling methodology, the data scientist will make incorrect decision and the model built tends to have a poor performance.


* **Learning Region**. In this region, the data scientist starts to learn about the problem, the data, and the model methodology. Here, one can see a large number of hypotheses being formulated and tested. Many of these, will guide the work towards a more correct methodology. The improvements will come with the correct implementation of these methodologies.

* **Deployment Region**. Here, the work has enough quality to be put into operation, when evaluated in terms of correcteness and performance metrics.
  
* **Fool's Region**. In this quadrant, one's lack of care with respect to the correcteness of methodology leads to think that the model is ready for deployment, because the performance shows a value that is better than the defined threshold.

## The Dunning-Krueger Effect

The division in four regions allows us to see similarities with the [Dunning-Krueger](https://[dx.doi.org/](https://doi.org/10.1037/0022-3514.77.6.1121)) effect, a cognitive bias phenomenon that explains the difference between one's perceived knowledge and one's actual knowledge of a subject.

In a nutshell, the Dunning-Krueger effect states that our ability to perceive our knowledge does not grows linearly with the actual acquired knowledge: when we have "very limited knowledge" of a subject, we are inclined to think that we are "highly skilled" on this subject. For example, the majority of drivers believe that their driving skills are above average [citation needed]. The following figure illustrates the relationship between perceived knowledge and actual knowledge.

![Dunning Kruger](https://raw.githubusercontent.com/hsteinshiromoto/blog/dev/images/are_model_performance_metrics_enough/dunning_kruger.svg)

In our case, the fool's region coincides with the top of graph, when the "actual knowledge is low".

## The role of business assumptions

It is worth to note that many business assumptions and/or decision will tend to have a negative impact on the model correctness, as these tend not to be scientifically based.

![Regions divisions](https://raw.githubusercontent.com/hsteinshiromoto/blog/dev/images/are_model_performance_metrics_enough/correctnessvsperformance_regions_bas.svg)

One example of a common business assumption that is overlooked is the dependency of time on the prediction. In a marketing campaign setting, a machine learning model is often used to identify the most suitable customers. Frequently, the model predicting the customer behaviour does not take into account previous customers reactions to similar campaigns.

# Conclusion

In conclusion, relying solely on performance metrics to determine model readiness for deployment is insufficient. Evaluating correctness and performance as separate components is essential. The relationship between correctness and performance, visualized in different regions, emphasizes the need for critical evaluation and avoiding the "Fool's Region" of overconfidence. Additionally, considering business assumptions and decisions that impact correctness is crucial. A comprehensive assessment of both correctness and performance metrics is necessary to make informed deployment decisions and ensure the model's validity.