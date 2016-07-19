#coding=utf-8
import sys
import os
import urllib
import urllib2

testline = "\xe5\x9b\x9b\xe5\xb7\x9d\xe8\x8f\x9c\xe9\xa6\x86"
print testline.decode('utf-8')

url="http://127.0.0.1:5000/restaurant/JSON/"
response = urllib2.urlopen(url)
content = response.read()
print content
