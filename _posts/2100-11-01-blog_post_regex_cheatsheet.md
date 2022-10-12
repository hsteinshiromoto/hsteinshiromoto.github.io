My favourite regex patterns

Get all content between two words:

Suppose we have two paragraphs as such

Start: Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Sodales ut eu sem integer vitae justo eget magna. Tincidunt praesent semper feugiat nibh sed pulvinar proin gravida. Praesent semper feugiat nibh sed. Mi proin sed libero enim sed faucibus turpis. Tortor pretium viverra suspendisse potenti nullam ac. Porttitor massa id neque aliquam vestibulum morbi blandit cursus. Ridiculus mus mauris vitae ultricies leo integer malesuada. Facilisi cras fermentum odio eu feugiat pretium nibh. Commodo quis imperdiet massa tincidunt nunc. Fringilla phasellus faucibus scelerisque eleifend donec pretium vulputate sapien nec. Gravida cum sociis natoque penatibus. Vitae congue mauris rhoncus aenean vel elit scelerisque mauris. Nisl vel pretium lectus quam. Mattis aliquam faucibus purus in massa tempor. Luctus accumsan tortor posuere ac ut consequat semper. Nam at lectus urna duis. Vulputate odio ut enim blandit volutpat maecenas volutpat blandit.

Malesuada fames ac turpis egestas integer eget. Cras semper auctor neque vitae tempus. Sed adipiscing diam donec adipiscing tristique risus nec. Adipiscing tristique risus nec feugiat in fermentum. Diam quam nulla porttitor massa. Vestibulum rhoncus est pellentesque elit ullamcorper. Orci porta non pulvinar neque. Cras tincidunt lobortis feugiat vivamus. Felis eget nunc lobortis mattis aliquam faucibus. Volutpat diam ut venenatis tellus in. Nibh nisl condimentum id venenatis a condimentum vitae. end

and we want to select everything between the keywods `start` and `end`. We can use the following pattern

`(?<=Start)((.|\n)*)(?=end)`

## References:

* [1] www.regexr.com