#!/usr/bin/env python
# coding: utf-8

import sys
import os
from jinja2 import Environment, FileSystemLoader
import config
from bs4 import BeautifulSoup
import re

class Pages(object):
    """
    Page Generator
    """

    def __init__(self):
        self.curr_dir = os.path.dirname(os.path.abspath(__file__))
        self.env = Environment(loader=FileSystemLoader(
            os.path.join(self.curr_dir, '../templates')
        ))
        self.output_dir = os.path.join(self.curr_dir, '../public')

    def home(self):
        f_list = os.listdir(self.output_dir)
        archives = []
        for f0 in f_list:
            f = os.path.join(self.output_dir, f0)
            if os.path.isfile(f) and f.endswith('.html') and f0 != 'index.html':
                with open(f, 'r', encoding='utf-8') as post_f:
                    soup = BeautifulSoup(post_f.read(), 'lxml')
                    title = soup.find('h1').text.rstrip('¶')
                    date = soup.find('h1').find_next('p').text
                    url = f0
                    archives.append({'title': title, 'date': date, 'url': url})

        archives = sorted(archives, key=lambda x: x['date'], reverse=True)

        template = self.env.get_template('index.html')
        data = {'title': config.title,
                   'author': config.author, 'archives': archives}

        with open(os.path.join(self.output_dir, 'index.html'), 'w', encoding='utf-8') as home_f:
            home_html = template.render(data=data)
            analytics_code = open(os.path.join(self.output_dir, '../templates/analytics.html'),
                    'r', encoding='utf-8').read()
            home_html = home_html.replace('<head><meta charset="utf-8" />', \
                    '<head><meta charset="utf-8" />\n' + analytics_code)
            home_f.write(home_html)

    def comment(self):
        f_list = os.listdir(self.output_dir)
        comment_code = open(os.path.join(self.output_dir, '../templates/comments.html'),
                            'r', encoding='utf-8').read()
        analytics_code = open(os.path.join(self.output_dir, '../templates/analytics.html'),
                'r', encoding='utf-8').read()
        for f0 in f_list:
            filename = os.path.join(self.output_dir, f0)
            if os.path.isfile(filename) and filename.endswith('.html') and f0 != 'index.html':
                with open(filename, 'r+', encoding='utf-8') as f:
                    text = f.read()
                    soup = BeautifulSoup(text, 'lxml')
                    title = soup.find('h1').text.rstrip('¶')
                    text = re.sub('\<title\>.*?\<\/title\>', f'<title>{config.author} | {title}</title>', text)
                    text = text.replace('</body>', comment_code + '</body>')
                    text = text.replace('<head><meta charset="utf-8" />', \
                            '<head><meta charset="utf-8" />\n' + analytics_code)
                    f.seek(0)
                    f.write(text)
                    f.truncate()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} [home|comment]')
        sys.exit(-1)

    pages = Pages()

    if sys.argv[1] == 'home':
        pages.home()
    elif sys.argv[1] == 'comment':
        pages.comment()
    else:
        print(f'Usage: {sys.argv[0]} [home|comment]')
        sys.exit(-1)
