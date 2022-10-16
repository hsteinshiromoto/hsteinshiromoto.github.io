My favourite regex patterns

Get all content between two words:

Suppose we have two paragraphs as such

>📝 Start: Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Sodales ut eu sem integer vitae justo eget magna. Tincidunt praesent semper feugiat nibh sed pulvinar proin gravida. Praesent semper feugiat nibh sed. Mi proin sed libero enim sed faucibus turpis. Tortor pretium viverra suspendisse potenti nullam ac. Porttitor massa id neque aliquam vestibulum morbi blandit cursus. Ridiculus mus mauris vitae ultricies leo integer malesuada. Facilisi cras fermentum odio eu feugiat pretium nibh. Commodo quis imperdiet massa tincidunt nunc. Fringilla phasellus faucibus scelerisque eleifend donec pretium vulputate sapien nec. Gravida cum sociis natoque penatibus. Vitae congue mauris rhoncus aenean vel elit scelerisque mauris. Nisl vel pretium lectus quam. Mattis aliquam faucibus purus in massa tempor. Luctus accumsan tortor posuere ac ut consequat semper. Nam at lectus urna duis. Vulputate odio ut enim blandit volutpat maecenas volutpat blandit.
> >
> Malesuada fames ac turpis egestas integer eget. Cras semper auctor neque vitae tempus. Sed adipiscing diam donec adipiscing tristique risus nec. Adipiscing tristique risus nec feugiat in fermentum. Diam quam nulla porttitor massa. Vestibulum rhoncus est pellentesque elit ullamcorper. Orci porta non pulvinar neque. Cras tincidunt lobortis feugiat vivamus. Felis eget nunc lobortis mattis aliquam faucibus. Volutpat diam ut venenatis tellus in. Nibh nisl condimentum id venenatis a condimentum vitae. end
---

### Select everything between the keywods `start` and `end`

```python
(?<=Start)((.|\n)*)(?=end)
```

### Select everything between the keywods `start` and `end` including these

`Start((.|\n)*)end`

## Regex with Python

Import the regular expressions module

```python
import re
```

### Functions

Returns a list containing all matches:
```python
re.findall

>>> re.findall(r'\bs?pare?\b', 'par spar apparent spare part pare')
['par', 'spar', 'spare', 'pare']
>>> re.findall(r'\b0*[1-9]\d{2,}\b', '0501 035 154 12 26 98234')
['0501', '154', '98234']
```

Returns an iterable of match objects (one for each match):
```python
re.finditer

>>> m_iter = re.finditer(r'[0-9]+', '45 349 651 593 4 204')
>>> [m[0] for m in m_iter if int(m[0]) < 350]
['45', '349', '4', '204']
```

Returns a Match object if there is a match anywhere in the string:
```python
re.search 

>>> sentence = 'This is a sample string'
>>> bool(re.search(r'this', sentence, flags=re.I))
True
>>> bool(re.search(r'xyz', sentence))
False

```

Returns a list where the string has been split at each match:
```python
re.split

>>> re.split(r'\d+', 'Sample123string42with777numbers')
['Sample', 'string', 'with', 'numbers']
```

Replaces one or many matches with a string:
```python
re.sub

>>> ip_lines = "catapults\nconcatenate\ncat"
>>> print(re.sub(r'^', r'* ', ip_lines, flags=re.M))
* catapults
* concatenate
* cat
```

Compiles a regular expression pattern for later use:
```python
re.compile

>>> pet = re.compile(r'dog')
>>> type(pet)
<class '_sre.SRE_Pattern'>
>>> bool(pet.search('They bought a dog'))
True
>>> bool(pet.search('A cat crossed their path'))
False
```

Returns string with all non-alphanumerics backslashed:
```python
re.escape
```

### Tags

re.I 	re.IGNORECASE 	Ignore case
re.M 	re.MULTILINE 	Multiline
re.L 	re.LOCALE 	Make \w,\b,\s locale dependent
re.S 	re.DOTALL 	Dot matches all (including newline)
re.U 	re.UNICODE 	Make \w,\b,\d,\s unicode dependent
re.X 	re.VERBOSE 	Readable style

## References:

* [1] https://www.regexr.com
* [2] https://quickref.me/regex