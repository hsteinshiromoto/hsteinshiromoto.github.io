---
title: 'Hypothesis Tests Part 2: Statistical Inference'
date: 2020-05-21
layout: posts
permalink: /posts/2020/05/21/statistical_tests_part_2_statistical_inference
categories:
  - statistics
tags:
  - hypothesis_tests
---

In this post, I present an overview of statistical tests. The goal of calculating a test statistic is to decided if the null hypothesis is true. Once value of the test-statistic is obtained, it is compared with a pre-defined critical value. If the test statistic is found to be greater than the critical value, then hypothesis is rejected.

- [1. The Statistical Inference Setting](#1-the-statistical-inference-setting)
- [2. Tests](#2-tests)
  - [2.1. T-test](#21-t-test)
    - [2.1.1. Population and Sample](#211-population-and-sample)
    - [2.1.2. Different Samples](#212-different-samples)
  - [2.2. ANOVA](#22-anova)
  - [2.3. $\chi^2$ Test](#23-chi2-test)
- [3. Errors](#3-errors)
- [4. Dealing with Non-normal Distributions](#4-dealing-with-non-normal-distributions)
- [5. Further Reading](#5-further-reading)

# 1. The Statistical Inference Setting

A null hypothesis, proposes that no (statistical) significant difference exists between two sets of observations. Example:

* $H_0$: The means of the two sets are equal
* $H_1$: The means of the two sets are not equal

To decide if the null hypothesis must be rejected, a test statistic is calculated. This number is used to compare with the *critical value* which is a pre-defined threshold used to decide if the null hypothesis must be rejected.

In general, critical values are the boundaries of *critical regions*. If the value of the test statistic falls within one of these regions, then the null hypothesis is rejected.

If the considered data follow a set of assumptions regarding its distribution, one interpretation for the rejection of the null hypothesis can be stated as follows: The probability of the null hypothesis be true is smaller than a probability $\alpha$. Therefore, this hypothesis must be reject.

From the statistical inference viewpoint, hypothesis testing is the process that establishes whether the measurement of a given statistic, such as the sample mean, is consistent with a theoretical distribution. The process of hypothesis testing requires a considerable amount of care in the definition the hypothesis to test and in drawing conclusions.

Let $E\subset\mathbb{R}^n$, and $f:E\times\mathbb{R}^n\to\mathbb{R}$ be a probability distribution function. Every hypothesis consists of an assumption about the parameter $\lambda$ of the distribution $x\mapsto f(x, \lambda)$.

The null hypothesis $H_0$ is made with respect to the parameter $\lambda$ and formulated as

$$ H_0: \lambda=\lambda_0\;,$$
for a given $\lambda_0\in\mathbb{R}^n$. The alternative hypothesis is given as

$$ H_1: \lambda\neq\lambda_0\;. $$

Since the null hypothesis makes a statement about the probability density in the sample space, it also predicts the probability for observing a point $x\in E$. This probability is used to define the rejection region $S_c\subset E$ with a significance level $\alpha\in(0,1)$ as

$$ P(x\in S_c\|H_0)=\alpha\;. $$

In other words, $S_c$ is defined as the probability to observe a point $x$ within $S_c$ equals to $α$, under the assumption that $H_0$ is true. If the point $X$ from the sample actually falls into the region $S_c$, then the hypothesis $H_0$ is rejected. Note that this equation does not define the critical region $S_c$ uniquely.

The probability $P(x\in S_c\|H_0)$ is also known as **p-value**: the probability, under the null hypothesis $H_0$, about the unknown distribution $f$ of the random variable, for the variable to be observed as a value equal to or more extreme than the values observed $x\in S_c$.

In practice, the distribution $f$ is not available due to the lack of knowledge of the population. Instead one constructs a test statistic $T:\mathbb{R}^n\to\mathbb{R}$, and defines a region $U$ of the variable $T$ that corresponds to the critical region $S_c$, i.e., $x\mapsto T(x), S_c(x)\mapsto U(x)$. The null hypothesis is rejected, whenever $T\in U$

The hypothesis test using statistical inference process can be summarized in three steps.

1. Determine the statistics to use for the null hypothesis. The choice of statistic means that we are in a position to use the theoretical distribution function for that statistic to tell whether the actual measurements are consistent with its expected distribution, according to the null hypothesis.

2. Determine the probability or confidence level for the agreement between the statistic and its expected distribution under the null hypothesis. This confidence level defines a range of values for the statistics that are consistent with its expected distribution. This range is called *acceptable region* for the statistic. Values of the statistics outside of the acceptable range define the *rejection region*.

3. At this point two cases are possible:

    3.1. The measure value of the statistic falls into the rejection region. This means that the distribution function of the statistic of interest, under the null hypothesis, does not allow the measured value at the confidence level $\alpha$. In this case the null hypothesis must be rejected at the stated confidence level $\alpha$. 
    
    3.2. The measured value of the statistic is within the acceptable region. In this case the null hypothesis cannot be rejected. Sometimes this situation can be referred to as the null hypothesis being acceptable. This is, however, not the same as stating that the null hypothesis is the correct hypothesis and that the null hypothesis is accepted. In fact, there could be other hypotheses that could be acceptable and one cannot be certain that the null hypothesis tested represents the parent model for the data.

# 2. Tests

## 2.1. T-test

### 2.1.1. Population and Sample

In this scenario, assuming that samples are taken from a population that is normally distributed. The hypothesis to be tested is whether the population mean $\bar{x}$ is equal to a predefined value $\mu_0$:

* $H_0$: $\bar{x}=\mu_0$
* $H_1$: $\bar{x}\neq\mu_0$

When the population variance is unknown, the population variance can only be estimated from the data via the sample variance $s^2$, and it is necessary to allow for such uncertainty when estimating the distribution of the sample mean. This additional uncertainty leads to a deviation of the distribution function from the simple Gaussian shape to the Student's t-distribution

$$ T=\dfrac{\bar{x}-\mu_0}{s/\sqrt{n}} $$

### 2.1.2. Different Samples

Given two groups (1, 2), this test is only applicable when:

* the two sample sizes (that is, the number n of participants of each group) are equal;
* it can be assumed that the two distributions have the same variance;

The $t$ statistic to test whether the means are different can be calculated as follows: 

$$ T=\dfrac{\bar{x}_1-\bar{x}_2}{s_p\sqrt{2/n}}\;, $$

where

$$ s_p^2=\dfrac{s_1^2+s_2^2}{2} $$

and $s_p$ is the pooled standard deviation for $n = n_1 = n_2$ and $s_1$ and $s_2$ are the unbiased estimators of the variances of the two samples. 

## 2.2. ANOVA

Is used to analyze the differences among group means in a sample. To use this statistical test. The hypothesis being tested in ANOVA is

* Null: All groups have the same mean
* Alternate: There exists one group with a statistically significantly different mean
 
The statistics that measures the significance is called F-statistics which is used to compare factors from the total standard deviation. For comparing two groups, the formula for the F-statistics is given as

$$F=\dfrac{\text{between-group variability}}{\text{within-group variability}}\;.$$

The component between-group variability is calculated as

$$\text{between-group variability}=\dfrac{1}{K-1}\sum_{i=1}^K n_i(\bar{x}_i-\bar{x})^2\;,$$

where 
* $\bar{x}_i$ is the sample mean of group $i$.
* $n_i$ is the number of observations in the $i-$th group.
* $\bar{x}$ is the overall mean of the data.
* $K$ is the number of groups.

The component within-group variability is computed by the formula

$$\text{within-group variability}=\sum_{i=1}^K\sum_{j=1}^{n_i}\dfrac{(x_{ij}-\bar{x}_i)^2}{N-K}\;,$$

where
* $x_{ij}$ is the observation $j$ in group $i$.
* $N$ is the overall sample size.

## 2.3. $\chi^2$ Test

The $\chi^2$ distribution appears from the result of the sum of independent, standard normal random variables, i.e., $X_1^2 + X_2^2 + \cdots + X_k^2\sim\chi^2(k)$.

In this test, the test statistic is $\chi^2$ distributed under the null hypothesis. This test is used used to determine whether there is a statistically significant difference between the expected frequencies and the observed frequencies in one or more categories. For this reason, it can be applied to compare categorical variables. Also, the $\chi^2$ test can be used to test whether the variance of the population has a pre-determined value.

The hypothesis being tested for chi-square is
* Null: Variable A and Variable B are independent
* Alternate: Variable A and Variable B are not independent.

There are two types of $\chi^2$ tests:
1. Goodness of fit test, which determines if a sample matches the population.
   
   a. A small chi-square value means that data fits
   
   b. A high chi-square value means that data doesn’t fit.
2. A $\chi^2$ fit test for two independent variables is used to compare two variables in a contingency table to check if the data fits.

The formula used for calculating the statistic is

$$ \chi^2=\sum_{i=1}^n\dfrac{(O_i-E_i)^2}{E_i}\;,$$

where
* $O_i$ is the number of observations of type $i$
* $E_i$ is the expected count of type $i$

# 3. Errors

Because of the statistical nature of the sample, it is possible to infer the following errors

1. *Type I Error*: The null hypothesis is true but the decision based on the testing process is that the null hypothesis should be rejected
2. *Type II Error*: The null hypothesis is false but the testing process concludes that it should be accepted. 

The probability of a Type I error (denoted by $\alpha$) is also called the significance level of the test. The Type II error occurs if one does not reject the hypothesis $H_0$ because $X$ was not in the critical region $S_c$, even though the hypothesis was actually false and an alternative hypothesis was true. This error is formalized as,

$$P(X\notin S_c\|H_1)=\beta\;.$$

 The following table summarizes the two types of errors.

|                | H0 is True   | H0 is False   |
|----------------|--------------|---------------|
| **H0 is accepted** | Correct      | Type II Error |
| **H0 is rejected** | Type I Error | Correct       |

This connection with the alternative hypothesis $H_1$ provides us with a method to specify the critical region $S_c$. A test is clearly most reasonable if for a given significance level $\alpha$ the critical region is chosen such that the probability $\beta$ for an error of the second kind is a minimum. The critical region and therefore the test itself naturally depend on the alternative hypothesis under consideration.

# 4. Dealing with Non-normal Distributions

As the reader may have notice, all these tests assume that the population is normally distributed. When this is not case, it is necessary to normalize the data. To see more information on how to deal with non-normal distribution, please check the following link https://www.statisticshowto.com/probability-and-statistics/non-normal-distributions/

# 5. Further Reading

* [1] M. Bonamente, "Statistics and Analysis of Scientific Data", Springer, 2017
* [2] S. Brandt, "Data Analysis", Springer, 2014
* [3] L.-G. Johansson, "Philosophy of Science for Scientists", Springer 2016
