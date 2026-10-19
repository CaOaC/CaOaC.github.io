---
layout: archive
title: "CV"
permalink: /cv/
author_profile: true
redirect_from:
  - /resume
---

{% include base_path %}

Education
======
* Ph.D. in Chemical Physics, University of Science and Technology of China, 2018–2024 (Advisor: Zhonghuai Hou)
* B.S. in Chemical Physics, University of Science and Technology of China, 2014–2018

Work experience
======
* Aug. 2023–Feb. 2024: Visiting scholar
  * Rice University, Center for Theoretical Biological Physics
  * Advisor: Peter G. Wolynes
  
* Aug. 2024–present: Postdoctoral researcher
  * Rice University, Center for Theoretical Biological Physics
  * Advisor: Peter G. Wolynes

Publications
======
  <ul>{% for post in site.publications reversed %}
    {% include archive-single-cv.html %}
  {% endfor %}</ul>
  
Talks
======
  <ul>{% for post in site.talks reversed %}
    {% include archive-single-talk-cv.html  %}
  {% endfor %}</ul>
  
{% if site.teaching.size > 0 %}
Teaching
======
  <ul>{% for post in site.teaching reversed %}
    {% include archive-single-cv.html %}
  {% endfor %}</ul>
{% endif %}
