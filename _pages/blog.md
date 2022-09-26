---
layout: archive
permalink: /blog/
title: "Blog"
author_profile: true
redirect_from:
- /critical_point/
- /blog/
---
Welcome to my blog. Here, I post texts about topics of my interest. The posts are dynamic: they might be modified in the
future.

{% for post in site.posts %}
    {% include archive-single.html %}
{% endfor %}
