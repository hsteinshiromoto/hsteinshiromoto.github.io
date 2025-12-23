---
permalink: /
layout: single
title: "About me"
author_profile: true
redirect_from:
- /about/
- /home/
- /index/
---

Hi!

Welcome to my webpage.

I am also passionate about making a local impact, moving our society towards a more fair ideal. That means
learning about and working to increase social good. During my PhD, I was an active leader in my department at Université
Grenoble Alpes, advocating for graduate students through inclusion efforts. I am especially proud of the PhD students
association during the years 2012-2013, where I learned management skills that have positively impacted almost every
aspect of my life.

When I’m not doing those things, I am probably baking bread or walking my dog. Before moving to Australia, I lived in
Europe (Italy, France, and The Netherlands), and Brazil.

## Latest Posts

{% for post in site.posts limit:3 %}
  {% include archive-single.html type=entries_layout %}
{% endfor %}