# Regex Cheatsheet

In this post, I compile a cheatsheet of the main regexes that I use in my projects.

Digital communication relies heavily on regular expressions to make it work. These are sequences of characters that specify a search pattern in the text. It is usually these types of patterns that are used by string-searching algorithms when they are attempting to "find" and/or "replace" strings or when they are attempting to validate input. Regular expression techniques are developed in theoretical computer science and formal language theory.

It is common to use regular expressions and other text processing utilities, for example `sed` and `AWK`, to search and replace in text processors, as well as in lexical analysis and in text processing. The majority of general-purpose programming languages support regex capabilities either natively or with the aid of libraries. Examples of such languages include Python, C, C++, Java, and JavaScript.

An example of a regular expression is to locate a word spelled two different ways in a text editor, the regular expression `seriali[sz]e` matches both "serialise" and "serialize".

## Table of Contents

- [Regex Cheatsheet](#regex-cheatsheet)
  - [Table of Contents](#table-of-contents)
  - [Character Classes](#character-classes)
  - [Python's regex module](#pythons-regex-module)
    - [`re.findall`](#refindall)
    - [`re.finditer`](#refinditer)
    - [`re.search`](#research)
    - [`re.split`](#resplit)
    - [`re.sub`](#resub)
    - [`re.compile`](#recompile)
    - [`re.escape`](#reescape)
    - [Flags](#flags)
  - [Cookbook](#cookbook)
    - [Select everything between the keywods `start` and `end`](#select-everything-between-the-keywods-start-and-end)
    - [Select email addresses](#select-email-addresses)
  - [References:](#references)

## Character Classes

All characters used in digital communication can be categorized the classes shown in the table below.

| Character Class 	| Same as 	                            | Meaning                        |
| ----------------- | ------------------------------------- | ------------------------------ |
| `[[:alnum:]]` 	  | `[0-9A-Za-z]` 	                      | Letters and digits             |
| `[[:alpha:]]` 	  | `[A-Za-z]` 	                          | Letters                        |
| `[[:ascii:]]` 	  | `[\x00-\x7F]` 	                      | ASCII codes 0-127              |
| `[[:blank:]]` 	  | `[\t ] `	                            | Space or tab only              |
| `[[:cntrl:]]` 	  | `[\x00-\x1F\x7F]` 	                  | Control characters             |
| `[[:digit:]]` 	  | `[0-9]` 	                            | Decimal digits                 |
| `[[:graph:]]` 	  | `[[:alnum:][:punct:]] `	              | Visible characters (not space) |
| `[[:lower:]]` 	  | `[a-z]` 	                            | Lowercase letters              |
| `[[:print:]]` 	  | `[ -~] == [ [:graph:]] `              | Visible characters             |
| `[[:punct:]]`     | ``[!"#$%&’()*+,-./:;<=>?@[]^_`{\|}~]``| Visible punctuation characters |
| `[[:space:]]` 	  | `[\t\n\v\f\r ] `	                    | Whitespace                     |
| `[[:upper:]]` 	  | `[A-Z]` 	                            | Uppercase letters              |
| `[[:word:]]` 	    | `[0-9A-Za-z_]` 	                      | Word characters                |
| `[[:xdigit:]]`    | `[0-9A-Fa-f]` 	                      | Hexadecimal digits             |
| `[[:<:]]` 	      | `[\b(?=\w)] `	                        | Start of word                  |
| `[[:>:]]` 	      | `[\b(?<=\w)] `	                      | End of word                    |

## Python's regex module

The regular expressions module can be imported using the command

```python
import re
```

It contains the following functions to be used.

### `re.findall`

Returns a list containing all matches:
```python
>>> re.findall(r'\bs?pare?\b', 'par spar apparent spare part pare')
['par', 'spar', 'spare', 'pare']
>>> re.findall(r'\b0*[1-9]\d{2,}\b', '0501 035 154 12 26 98234')
['0501', '154', '98234']
```

### `re.finditer` 

Returns an iterable of match objects (one for each match):
```python
>>> m_iter = re.finditer(r'[0-9]+', '45 349 651 593 4 204')
>>> [m[0] for m in m_iter if int(m[0]) < 350]
['45', '349', '4', '204']
```

### `re.search`
Returns a Match object if there is a match anywhere in the string:
```python
>>> sentence = 'This is a sample string'
>>> bool(re.search(r'this', sentence, flags=re.I))
True
>>> bool(re.search(r'xyz', sentence))
False
```

### `re.split`
Returns a list where the string has been split at each match:
```python
>>> re.split(r'\d+', 'Sample123string42with777numbers')
['Sample', 'string', 'with', 'numbers']
```

### `re.sub`
Replaces one or many matches with a string:
```python
>>> ip_lines = "catapults\nconcatenate\ncat"
>>> print(re.sub(r'^', r'* ', ip_lines, flags=re.M))
* catapults
* concatenate
* cat
```

Tip: You can also use string methods {: .notice--info} {: .text-justify}

### `re.compile`
Compiles a regular expression pattern for later use:
```python
>>> pet = re.compile(r'dog')
>>> type(pet)
<class '_sre.SRE_Pattern'>
>>> bool(pet.search('They bought a dog'))
True
>>> bool(pet.search('A cat crossed their path'))
False
```

### `re.escape`

### Flags

|code (short)|code (long)      |Description                                    |
|------------|-----------------|---------------------------------------------- |
| `re.I`     | `re.IGNORECASE` | Ignore case                                   |
| `re.M`     | `re.MULTILINE`  | Multiline                                     |
| `re.L`     | `re.LOCALE`     | Make `\w`, `\b`, `\s` locale dependent        |
| `re.S`     | `re.DOTALL`     | Dot matches all (including newline)           |
| `re.U`     | `re.UNICODE`    | Make `\w`, `\b`, `\d`, `\s` unicode dependent |
| `re.X`     | `re.VERBOSE`    | Readable style                                |

## Cookbook

Suppose we have two paragraphs as such

```python
paragraph = """

Start: 
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor 
incididunt ut labore et dolore magna aliqua. Sodales ut eu sem integer vitae 
justo eget magna. 

Tincidunt praesent semper feugiat nibh sed pulvinar proin 
gravida. Praesent semper feugiat nibh sed. Mi proin sed libero enim sed faucibus 
turpis. Tortor pretium viverra suspendisse potenti nullam ac. end
"""
```

### Select everything between the keywods `start` and `end`

```python
>>> result = re.search(r"(?<=Start:)((.|\n)*)(?=end)", paragraph).group()
>>> print(result)
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor 
incididunt ut labore et dolore magna aliqua. Sodales ut eu sem integer vitae 
justo eget magna. 

Tincidunt praesent semper feugiat nibh sed pulvinar proin 
gravida. Praesent semper feugiat nibh sed. Mi proin sed libero enim sed faucibus 
turpis. Tortor pretium viverra suspendisse potenti nullam ac.
```

### Select email addresses

Suppose we want to extract the emails contained in the following paragraph:
```python
paragraph = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor 
incididunt ut labore et dolore magna aliqua. Sodales ut eu sem integer vitae 
justo eget magna. John Silva Doe <john.silva_3.doe@email.com> 
Josh Tree Done 'jpsj_3@gmail.com'

Jane Doe <jane_doe4@email.com>

Malesuada fames ac turpis egestas integer eget. Cras semper auctor neque vitae 
tempus. Sed adipiscing diam donec adipiscing tristique risus nec. 
"""
```

```python
>>> result = re.findall(r"<?(\S+@[\w.-]+\.[a-zA-Z]{2,4}\b)", paragraph)
>>> result
['john.silva_3.doe@email.com', 'jpsj_3@gmail.com', 'jane_doe4@email.com']
```

## References:

* [1] https://www.regexr.com
* [2] https://quickref.me/regex
* [3] https://www.regex101.com