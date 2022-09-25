---
title: 'Hypothesis Tests Part 1: Bayesian Inference'
date: 2020-04-17
permalink: /posts/2020/04/17/hypothesis_tests_part_1_bayesian_inference
categories:
  - statistics
tags:
  - hypothesis_tests
  - Bayes
---

Every quantity that is estimated from data, such as the mean or the variance, is subject to uncertainties of the measurements due to data collection. If a different sample of measurements is collected, value  fluctuations will certainly give rise to a different set of measurements, even if the experiments are performed under the same conditions. The use of different data samples to measure the same value results in a sampling distribution that characterize the quantity in consideration. This distribution is used to characterize the "true" value of the quantity in consideration. This blog post is dedicated to present how the collected data is employed to test hypotheses of the quantity being measured.

Hypothesis testing is the process that establishes whether the measurement of a given quantity, such as the mean, is consistent with respect to another set of observations or a distribution. The process of hypothesis testing requires a considerable amount of care in the definition the hypothesis to test and in drawing conclusions. Hypothesis tests can be divided into two main schools of thought based on Bayesian or Statistical inference. [1]

For a given hypothesis $H$ to be tested, it can be formulated in the following form

* $H_0$ (null hypothesis): The quantity in consideration is no different from the other set
* $H_1$ (alternative hypothesis): The quantity in consideration is different from the other set

In this blog post, I present an example of hypothesis testing using Bayesian inference. In a future version, I will present an example using statistical inference.

Table of Contents:

- [1. General Overview](#1-general-overview)
- [2. Example](#2-example)
- [3. References](#3-references)
- [4. Further Reading](#4-further-reading)
- [5. Appendix](#5-appendix)
  - [5.1. Code to generate the prior distribution](#51-code-to-generate-the-prior-distribution)
- [6. Code to calculate the conditional probability of the null hypothesis](#6-code-to-calculate-the-conditional-probability-of-the-null-hypothesis)

# 1. General Overview

In the Bayesian inference framework, the problem is formulated as follows: The goal is to calculate the conditional probability for a hypothesis being true, given a certain outcome of an experiment or measurement

$$
P(H_0|O)=\dfrac{P(O|H_0)P(H_0)}{P(O)}
$$

where $P(H_0)$ is the probability of the null hypothesis, $P(O)$ is the probability of observation and 

$$P(H_0|O)$$ 

is the probability of the null (respectively, alternative) hypothesis be true given the outcome

By fixing a _critical value_ $\alpha$, one either can verify whether the probability of the hypothesis 

$$P(H_0|O)$$

is higher or smaller than $\alpha$. Then, one accepts the null hypothesis if 

$$P(H_0|O)\geq\alpha\;.$$

# 2. Example

Consider a coin that has been tossed 100 times. Given that number of tails is 70, is this coin fair?

Assumptions: 

* Only two outcomes are possible: heads or tails
* Coin toss does not affect other tosses, i.e. coin tosses are independent of each other. 
* All coin tosses come from the same distribution. 

Thus, the random variable coin toss is an example of an iid variable. Under these assumptions the selected likelihood is the binomial distribution:

$$ P(y|\theta, N)=\dfrac{N!}{y!(N-y)!}\theta^y(1-\theta)^{N-y}\;, $$

where
* $y$ is the number of tails
* $\theta$ proportion of tails
* $N$ is the number of tosses

The hypothesis to be tested is the following:

* $H_0$: $\theta=0.5$
* $H_1$: $\theta\neq0.5$

The hypothesis $H_0$ will be rejected if

$$P(H_0|O)\leq0.5 = \alpha.$$

Under this hypothesis formulation, let the observations be the parameters $y$ and $N$, the conditional probability of $H_0$ is given by

$$P(H_0|O) = P(\theta=0.5|N=100,y=70)$$

The conditional probability of $\theta$ is calculated as

$$
P(\theta|N,y) = \dfrac{P(y|\theta,N)P(\theta)}{\displaystyle\int_0^1 P(y|\theta,N)P(\theta)\,d\theta}\;.
$$

The prior distribution is chosen as the beta distribution

$$ P(\theta)=\dfrac{\Gamma(\alpha+\beta)}{\Gamma(\alpha)\Gamma(\beta)}\theta^{\alpha-1}(1-\theta)^{\beta-1}\;, $$

where
* $\Gamma$ is the gamma function
* $\alpha$ and $\beta$ are parameters.

The following graph plots the prior for difference choices of the parameters $\alpha$ and $\beta$.

![svg](https://raw.githubusercontent.com/hsteinshiromoto/blog/master/notebooks/statistical_tests/prior_distribution.svg)



The posterior probability is

$$ P(\theta|N,y)=\dfrac{\theta^{y+\alpha-1}(1-\theta)^{N-y+\beta-1}}{\displaystyle \int_0^1\theta^{y+\alpha-1}(1-\theta)^{N-y+\beta-1}\;d\theta} $$

By letting $\alpha=\beta=1$, the prior distribution becomes a uniform distribution, and the probability of $\theta=0.5$ is upper bounded by

$$ P(0.49\leq\theta\leq0.51|N=100,y=30)=\dfrac{\displaystyle\int_{0.49}^{0.51}\theta^{30}(1-\theta)^{70}\;d\theta}{\displaystyle\int_0^1\theta^{30}(1-\theta)^{70}\;d\theta} \;=5.158837081428554\times10^{-5}\;.$$

Since the probability of the null hypothesis is less than 50%, hypothesis $H_0$ is rejected.

# 3. References

* [1] L.-G. Johansson. "Philosophy of Science for Scientists". Springer. 2016

# 4. Further Reading

* O. Martin. "Bayesian Analysis with Python". Packt. 2ed. 2018
* A. Gelman, J. B. Carlin, H. S. Stern, D. B. Dunson, A. Vehtari, D. B. Rubin. "Bayesian Data Analysis". CRC Press. 3ed. 2014


# 5. Appendix

## 5.1. Code to generate the prior distribution

```python
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

params = [0.5, 1, 2, 3]
x = np.linspace(0, 1, 100)
f, ax = plt.subplots(len(params), len(params), sharex=True, sharey=True, figsize=(20, 20), constrained_layout=True)
for i in range(4):
   for j in range(4):
        a = params[i]
        b = params[j]
        y = stats.beta(a, b).pdf(x) 
        ax[i,j].plot(x, y, linewidth=4)
        ax[i,j].plot(0, 0, label="α = {:2.1f}\nβ = {:2.1f}".format(a, b), alpha=0)
        ax[i,j].legend() 
ax[1,0].set_yticks([])
ax[1,0].set_xticks([0, 0.5, 1])
f.text(0.5, -0.025, 'θ', ha='center')
f.text(-0.025, 0.5, 'p(θ)', ha='left', va='center', rotation=0)
plt.savefig("prior_distribution.svg")
```

# 6. Code to calculate the conditional probability of the null hypothesis

```python
import scipy.integrate as integrate

integrate.quad(lambda theta: theta**30*(1-theta)**70, 0.49, 0.51)[0] / integrate.quad(lambda theta: theta**30*(1-theta)**70, 0, 1)[0]
```