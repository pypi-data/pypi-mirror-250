# std imports
import random
from datetime import datetime
import argparse

# 3rd party
import requests

# local
# 3rd-party
from bs4 import BeautifulSoup
# local imports
from blessed import Terminal


parser = argparse.ArgumentParser(
    description='Print articles from various sources.')
parser.add_argument('-a', type=int, default=5,
                    help='Number of articles to print from each source.')
args = parser.parse_args()


def embolden(phrase):
    # bold some phrases
    return phrase.isdigit() or phrase[:1].isupper()


def make_bold(term, text):
    # embolden text
    return ' '.join(term.bold(phrase) if embolden(phrase) else phrase
                    for phrase in text.split(' '))


def whitespace_only(term, line):
    # return only left-hand whitespace of `line'.
    return line[:term.length(line) - term.length(line.lstrip())]


def find_articles(soup, url):
    if 'text.npr.org' in url:
        return (a_link for section in soup.find_all('div', class_='topic-container') for a_link in section.find_all('a'))
    return (a_link for section in soup.find_all('section') for a_link in section.find_all('a'))


def main():
    term = Terminal()
    print(f"Current date and time: {datetime.now()}\n")
    urls = ['https://lite.cnn.com',
            'https://legiblenews.com', 'https://text.npr.org']
    for url in urls:
        print(f"Articles from {term.link(url,url)}:")
        soup = BeautifulSoup(requests.get(
            url, timeout=10).content, 'html.parser')
        textwrap_kwargs = {
            'width': term.width - (term.width // 4),
            'initial_indent': ' ' * (term.width // 6) + '* ',
            'subsequent_indent': (' ' * (term.width // 6)) + ' ' * 2,
        }
        article_count = 0
        for a_href in find_articles(soup, url):
            if article_count >= args.a:
                break
            url_id = random.randrange(0, 1 << 24)
            for line in term.wrap(make_bold(term, a_href.text), **textwrap_kwargs):
                print(whitespace_only(term, line), end='')
                print(term.link(url + a_href.get('href'), line.lstrip(), url_id))
            article_count += 1

    print(f"\nWeather from {term.link('https://wttr.in','wttr.in')}:")
    weather_response = requests.get(
        'http://wttr.in/?format=%C+%t+%w', timeout=10)
    print(weather_response.text)


if __name__ == '__main__':
    main()
