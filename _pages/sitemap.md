---
layout: archive
title: "Sitemap"
permalink: /sitemap/
author_profile: true
---

{% include base_path %}

Browse the pages and academic work on this site. An [XML sitemap]({{ base_path }}/sitemap.xml) is also available.

<h2>Pages</h2>
<ul>
{% for post in site.pages %}
  {% if post.title and post.title != empty and post.sitemap != false %}
    <li><a href="{{ post.url | relative_url }}">{{ post.title }}</a></li>
  {% endif %}
{% endfor %}
</ul>

{% for collection in site.collections %}
  {% if collection.output and collection.label != 'posts' and collection.docs.size > 0 %}
    <h2>{{ collection.label | capitalize }}</h2>
    {% for post in collection.docs reversed %}
      {% include archive-single.html %}
    {% endfor %}
  {% endif %}
{% endfor %}
