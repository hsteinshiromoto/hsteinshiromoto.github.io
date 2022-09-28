---
title: "A Digression on the Cantor Set"
date: 2021-01-21
layout: posts
permalink: posts/2021/01/21/a_digression_on_the_cantor_set
categories: 
  - mathematics
---

The Cantor set is a special type of set in mathematics. In this blog post, I will use it as an illustration of how my mind works, when I learning a new topic.

- [1. Mathematics](#1-mathematics)
  - [1.1. Definition](#11-definition)
  - [1.2. Properties](#12-properties)
- [2. A Model of How We Learn](#2-a-model-of-how-we-learn)
- [3. References](#3-references)

Cantor sets are used as a counterexample in fields such as set theory, and general topology.

![4](https://upload.wikimedia.org/wikipedia/commons/5/56/Cantor_set_in_seven_iterations.svg)

This set is obtained by interatively removing the middle third of a line segment: starting from the interval $[0, 1]$, remove the middle third $(1/3, 2/3)$. Now, for the second iteration, remove the middle thirds of the remaining sections: $(1/9, 2/9)$ and $(7/9, 8/9)$.

# 1. Mathematics

## 1.1. Definition

Let $C_0$ be the interval $[0,1]$ of the real numbers. For every $n\in\mathbb{N}_{>0}$, define the set

$$C_n=\dfrac{C_{n-1}}{3}\cup\left(\dfrac{2}{3}+\dfrac{C_{n-1}}{3}\right)\;.$$

The Cantor set is given by the intersection

$$C=\bigcap_{n=1}^\infty C_n\;.$$

## 1.2. Properties

The Cantor set has be following properties:
1. It is a [closed set](https://mathworld.wolfram.com/ClosedSet.html) consisting only of [boundary points](https://mathworld.wolfram.com/BoundaryPoint.html)
2. It is uncountable [2]
3. Have 0 or positive Lebesgue measure [2]
4. It is disconnected, [perfect](https://encyclopediaofmath.org/wiki/Perfect_set), compact metric space up to a homeomorphism [2]
5. It is self similar [3]

# 2. A Model of How We Learn

When we learn about a new topic, the first thing that we usually understand is the big picture. 

![The big picture](https://github.com/hsteinshiromoto/blog/raw/master/posts/2021-01-21-blog_post_a_digression_on_the_cantor_set/Cantor_set_in_one_iteration.svg)

It looks simple and easy to understand, until we start to scrutinize it and find gaps that we do not understand.

![](https://github.com/hsteinshiromoto/blog/raw/master/posts/2021-01-21-blog_post_a_digression_on_the_cantor_set/Cantor_set_in_two_iterations.svg)

As I start to investigate what we know to fill in the missing parts, we find even more gaps.

![](https://github.com/hsteinshiromoto/blog/raw/master/posts/2021-01-21-blog_post_a_digression_on_the_cantor_set/Cantor_set_in_three_iterations.svg)

This process goes on and on... as illustrated in the Cantor set below

![4](https://upload.wikimedia.org/wikipedia/commons/5/56/Cantor_set_in_seven_iterations.svg)

At the end, we realize that the pieces that remain provide enough information  to understand what we are investigating and that we learned an uncountable amount of information.

Now, the process of understanding the big picture in detail goes from bottom to top. At this point, our knowledge and understanding of the topic allows us to connect the two subjects that we could not at the beginning, filling the missing gap.

# 3. References

[1] Barile, Margherita and Weisstein, Eric W. "Cantor Set." From MathWorld--A Wolfram Web Resource. [https://mathworld.wolfram.com/CantorSet.html](https://mathworld.wolfram.com/CantorSet.html)

[2] Cantor Set. Brilliant.org. Retrieved 14:49, January 21, 2021, from [https://brilliant.org/wiki/cantor-set/](https://brilliant.org/wiki/cantor-set/)

[3] G.-T. Deng, X.-G. He and Z.-X. Wen, "Self-similar structure on intersections of triadicCantor sets", J. Math. Anal. Appl. 337 (2008) 617–631, 2007

[4] 127 "rect", . Cantor ternary set, in seven iterations. Retrieved September 21st, 2021, from [https://commons.wikimedia.org/wiki/File:Cantor_set_in_seven_iterations.svg](https://commons.wikimedia.org/wiki/File:Cantor_set_in_seven_iterations.svg)