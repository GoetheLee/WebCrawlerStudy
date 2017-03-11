# -*- coding: utf-8 -*-

from collections import Counter
import urllib
import random
import webbrowser

from konlpy.tag import Twitter
from konlpy.tag import Hannanum
from lxml import html
import pytagcloud # requires Korean font support

r = lambda: random.randint(0,255)
color = lambda: (r(), r(), r())

def get_tags(text, ntags=50, multiplier=10):
    spliter = Twitter()
    nouns = spliter.nouns(text)

#    h = Hannanum()
#    nouns = h.nouns(text)
    count = Counter(nouns)
    return [{ 'color': color(), 'tag': n, 'size': c*multiplier }\
                for n, c in count.most_common(ntags)]

def draw_cloud(tags, filename, fontname='Noto Sans CJK', size=(800, 600)):
    pytagcloud.create_tag_image(tags, filename, fontname=fontname, size=size)
    webbrowser.open(filename)


# bill_num = '1904882'
input = open('output_cleand.txt', 'r')
text = input.read()
# get_bill_text(bill_num)
# print(text)
tags = get_tags(text)
# print(tags)
open_output_file=open('out.txt', 'w')
open_output_file.write('%s\n'%tags)
open_output_file.close()
cloudfile = 'cloud.png'
draw_cloud(tags, cloudfile)


