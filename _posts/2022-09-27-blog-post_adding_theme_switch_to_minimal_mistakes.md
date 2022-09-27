---
title: 'Adding a Dark/Light Theme Switcher to Minimal Mistakes'
date: 2022-09-27
permalink: posts/2022/09/27/blog-post_adding_theme_switch_to_minimal_mistakes
tags: 
  - webdev
  - Jerkyll
  - github
categories:
  - coding
---

This is how I found out how to add a switcher to toggle between light and dark modes of minimal mistakes theme.

I followed the instructions posted by sohamsaha99 in [this Github thread](https://github.com/mmistakes/minimal-mistakes/discussions/2033) and copied here:

1. Edit `_config.yml`: There are going to be two themes. The first one is declared as usual. And for the second one, we create a new entry caled minimal_mistakes_skin2. So, add the following lines:
   
```yml
minimal_mistakes_skin: "default"
minimal_mistakes_skin2: "dark"
```

2. Create a file in your project directory in the location `assets/css/theme2.scss` and insert the following lines in the file:

```scss
---
# Only the main Sass file needs front matter (the dashes are enough)
---

@charset "utf-8";

@import "minimal-mistakes/skins/{{ site.minimal_mistakes_skin2 | default: 'default' }}"; // skin
@import "minimal-mistakes"; // main partials
```

3. Modify the following line in file `_includes/head.html` from:
   
```html
<link rel="stylesheet" href="{{ '/assets/css/main.css' | relative_url }}">
```
to

```html
<link rel="stylesheet" href="{{ '/assets/css/main.css' | relative_url }}" id="theme_source">
```
and just after that line, add the code:
```html
{% if site.minimal_mistakes_skin2 %}
  <link rel="stylesheet alternate" href="{{ '/assets/css/theme2.css' | relative_url }}" id="theme_source_2">
  <script>
    let theme = sessionStorage.getItem('theme');
    if(theme === "dark")
    {
      sessionStorage.setItem('theme', 'dark');
      node1 = document.getElementById('theme_source');
      node2 = document.getElementById('theme_source_2');
      node1.setAttribute('rel', 'stylesheet alternate'); 
      node2.setAttribute('rel', 'stylesheet');
    }
    else
    {
      sessionStorage.setItem('theme', 'light');
    }
  </script>
{% endif %}
```

The names `light` and `dark` are generics of `skin1` and `skin2`. These strings have nothing to do with the actual skin names.

4. Add an icon next to navigation. In `_includes/masterhead.html` find  `{ % if site.search == true % }` and above that add:
   
```html
{% if site.minimal_mistakes_skin2 %}
  <i class="fas fa-fw fa-sun" aria-hidden="true" onclick="node1=document.getElementById('theme_source');node2=document.getElementById('theme_source_2');if(node1.getAttribute('rel')=='stylesheet'){node1.setAttribute('rel', 'stylesheet alternate'); node2.setAttribute('rel', 'stylesheet');sessionStorage.setItem('theme', 'dark');}else{node2.setAttribute('rel', 'stylesheet alternate'); node1.setAttribute('rel', 'stylesheet');sessionStorage.setItem('theme', 'light');} return false;"></i>
{% endif %}
```