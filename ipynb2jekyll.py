#!/usr/bin/env python

import sys
import json
from datetime import datetime as dt

header = '''---
layout: post
title:  "%s"
date:   %s
---
'''

nb = json.load(open('/dev/stdin'))

print header % (sys.argv[1], dt.strftime(dt.now(), '%Y-%m-%d %H:%M:%S'))
# Make MathJax work
print '<script type="text/javascript" src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS_HTML-full" charset="utf-8"></script>'
print '''<script type="text/javascript">
MathJax.Hub.Config({
  tex2jax: {
    inlineMath: [['$','$'], ['\\(','\\)']],
    processEscapes: true
  }
});
</script>'''

for cell in nb['cells']:
    if cell['cell_type'] == 'markdown':
        for m in cell['source']:
            print '\n%s' % m
    elif cell['cell_type'] == 'code':
        print '\n\n{% highlight python %}'
        for code in cell['source']:
            sys.stdout.write(code)
        print '\n{% endhighlight %}\n'
        for o in cell['outputs']:
            if 'data' in o:
                for mime,data in o['data'].iteritems():
                    if mime == 'image/png':
                        sys.stdout.write('<img alt="Embedded Image" src="data:image/png;base64,%s"/>\n' % ''.join([x.strip() for x in data]))
                    elif mime == 'text/plain':
                        for o in data:
                            print '\n%s' % o


