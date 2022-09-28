---
title: "My Quick Reference Guide For A Few Natural Language Processing Techniques"
date: 2020-07-02
layout: posts
permalink: /posts/2020/07/02/my_quick_reference_guide_for_a_few_natural_language_processing_techniques
tags:
  - Natural Language Processing
  - Machine Learning
---
Natural language processing (NLP) is a field of study dedicated to
analyze of natural languages. In particular, using statistics and
algorithms.

This blog post provides a quick reference guide on what, when and how
each of the methods can be used.

- [Regular Expressions (RegEx)](#regular-expressions-regex)
  - [What it is](#what-it-is)
  - [When to use it](#when-to-use-it)
  - [How to use it](#how-to-use-it)
- [Word Tokenization](#word-tokenization)
  - [What it is](#what-it-is-1)
  - [When to use it](#when-to-use-it-1)
  - [How to use it](#how-to-use-it-1)
- [Bag of Words](#bag-of-words)
  - [What it is](#what-it-is-2)
  - [When to use it](#when-to-use-it-2)
  - [How to use it](#how-to-use-it-2)
- [Word as Vectors](#word-as-vectors)
  - [What it is](#what-it-is-3)
  - [When to use it](#when-to-use-it-3)
  - [How to use it](#how-to-use-it-3)
- [Tf-idf](#tf-idf)
  - [What it is](#what-it-is-4)
  - [When to use it](#when-to-use-it-4)
  - [How to use it](#how-to-use-it-4)
- [Name Entity Recognition](#name-entity-recognition)
  - [What it is](#what-it-is-5)
  - [When to use it](#when-to-use-it-5)
  - [How to use it](#how-to-use-it-5)
- [References](#references)

# Regular Expressions (RegEx)

## What it is

Regular expressions are strings with a special syntax, and for which
present a regular pattern that describes them.

## When to use it

RegEx is a powerful technique to be used with programming languages such
as C, Python, Java and others.

It consists of verifying if a specific pattern exists in the string
under consideration.

In many cases, using RegEx may create problems instead of solve it, as
the definition of the patterns to the searched for are not easy to
understand at first.

I have found a website that provides a sandbox to test for RegEx in
\[1\].

## How to use it

Python's regex module comes with the default installation. To add to
your script just write\
`import re`

The methods that I frequently use are

* `split(pattern, string)`: split a string
* `findall(pattern, string)`: find all patterns in the string
* `search(pattern, string)`: search for the pattern
* `match(pattern, string)`: match the entire string based on the pattern

# Word Tokenization

## What it is

Tokenization is process of transform a string or text into tokens
(smaller pieces).

## When to use it

Tokenization is useful to remove unwanted part of a text, separate
punctuation and processing hashtags in social media. For example,
tokenization can be used to separate the content of a text into
sentences.

## How to use it

Python has a module for word tokenization called nltk. The functions
that tokenize words and sentences are imported as follows.\
`from nltk.tokenize import word_tokenize, sent_tokenize`\
\
These functions can be used as\
`word_tokenize(string)`\
or\
`sent_tokenize(string)`

# Bag of Words

## What it is

Bag words is a method to obtain a set of words in a string (or text).

## When to use it

This methodology provides a way to count the how many times a specific
word appears in a text or a string.

## How to use it

A bag of words can be created with the tokenize functions as shown in
the section below.

# Word as Vectors

## What it is

A word vector is a multidimensional representation of a word. This
representation allows to analyze distance between words, according to an
appropriate metric.

These vectors are built using a model that has been trained over a
myriad of texts.

## When to use it

Word vectors can be used to understand relationships between words. For
instance, the vectors (man, woman) and (king, queen) are similar,
according to the metric obtained from the model.

## How to use it

The module `gensim` for Python allows the construction of the word
vectors. Gensim creates a corpus by transforming the tokens into ids
associated to the number of documents used.

# Tf-idf

## What it is

Term Frequency -- Inverse Document Frequency (tf-idf) is a measurement
of the number of occurrences of a specific token in a document
normalized by the number of documents that contain this token.
Mathematically, this is expressed as

$$ w_{i,j}=tf_{i.j}\log\left(\dfrac{N}{df_i}\right)\;, $$

where

* $w_{i,j}$ is the weight for the token $i$ in document $j$
* $tf_{i,j}$ is the number of occurrences of token $i$ in document $j$
* $df_i$ is the number of documents that contain token $i$
* $N$ is total number of documents

## When to use it

Tf-idf is useful to analyze the distribution of a token across multiple
documents.

## How to use it

The Python module Gensim provides a tf-idf model as follows\
`from gensim.models.tfidfmodel import TfidfModel `\
The tf idf class is instantiate using the corpus built with gensim:\
`tfidf = TfidfModel(corpus) `

# Name Entity Recognition

## What it is

It is the process of identifying tokens present in the text under
consideration as people, places, organizations, dates, states etc.

## When to use it

It is employed when tokens need to be identified into categories.

## How to use it

The modules `nltk` and (`Di`)`SpaCy` from Python allow the
identification of the tokens into categories.

# References

\[1\] <http://www.pyregex.com/>
