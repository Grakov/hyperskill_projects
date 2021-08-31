import argparse
import requests

from bs4 import BeautifulSoup

languages = {
    'arabic': {
        'dir': 'rtl arabic'
    },
    'german': {
        'dir': 'ltr'
    },
    'english': {
        'dir': 'ltr'
    },
    'spanish': {
        'dir': 'ltr'
    },
    'french': {
        'dir': 'ltr'
    },
    'hebrew': {
        'dir': 'rtl'
    },
    'japanese': {
        'dir': 'ltr'
    },
    'dutch': {
        'dir': 'ltr'
    },
    'polish': {
        'dir': 'ltr'
    },
    'portuguese': {
        'dir': 'ltr'
    },
    'romanian': {
        'dir': 'ltr'
    },
    'russian': {
        'dir': 'ltr'
    },
    'turkish': {
        'dir': 'ltr'
    }
}


def get_lang_id(name):
    if name == 'all':
        return -1

    index = 0
    for lang in languages:
        if lang['full'] == name:
            return index
        index += 1


def custom_print(value, name, ext=".txt", sep=" ", end="\n", encoding="utf-8", rewrite=False):
    filename = name + ext
    if rewrite:
        file = open(filename, 'w', encoding=encoding)
        file.close()
        return

    with open(filename, 'a', encoding=encoding) as file:
        if isinstance(value, list):
            file.write(sep.join(value) + end)
        else:
            file.write(value + end)

    if isinstance(value, list):
        print(*value, sep=sep, end=end)
    else:
        print(value, end=end)


def make_request(lang_from, lang_to, word):
    base_url = f'https://context.reverso.net/translation/{lang_from}-{lang_to}/{word}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0'
    }
    r = requests.get(base_url, headers=headers)

    if r.status_code == 404:
        raise Exception(f"Sorry, unable to find {word}")

    return BeautifulSoup(r.content, 'html.parser')


def parse_examples(soup, lang, is_from=True, limit=5):
    target = 'src' if is_from else 'trg'
    example_content = soup.find('section', {'id': 'examples-content'})
    return [el.text.strip() for el in
            example_content.find_all('div', {'class': f"{target} {languages[lang]['dir']}"}, limit=limit)]


def parse_translations(soup, limit=5):
    return [el.text.strip() for el in
            soup.find('div', {'id': 'translations-content'}).find_all('a', {'class': 'translation'}, limit=limit)]


def translate(lang_from, lang_to, word, limit=5):
    soup = make_request(lang_from, lang_to, word)

    custom_print(f"{lang_to.capitalize()} Translations:", word)

    translations = parse_translations(soup, limit=limit)
    custom_print(translations, word, sep="\n")
    custom_print('', word)

    custom_print(f"{lang_to.capitalize()} Examples:", word)
    examples_from = parse_examples(soup, lang_from, limit=limit, is_from=True)
    examples_to = parse_examples(soup, lang_to, limit=limit, is_from=False)

    for i in range(len(examples_from)):
        custom_print(examples_from[i], word)
        custom_print(examples_to[i], word)
        custom_print('', word)

    custom_print('', word)


# begin
parser = argparse.ArgumentParser(description="Word translator")
parser.add_argument("lang_from", help="Lang to translate from")
parser.add_argument("lang_to", help="Lang to translate to (all for every language)")
parser.add_argument("word", help="Word to translate")
args = parser.parse_args()

lang_from = args.lang_from.lower()
lang_to = args.lang_to.lower()
word = args.word

custom_print('', word, rewrite=True)

try:
    if lang_from not in languages:
        raise Exception(f"Sorry, the program doesn't support {lang_from}")
    if lang_to not in languages and lang_to != 'all':
        raise Exception(f"Sorry, the program doesn't support {lang_to}")

    if lang_to == 'all':
        for lang in languages.keys():
            if lang != lang_from:
                translate(lang_from, lang, word, limit=1)
    else:
        translate(lang_from, lang_to, word)

except requests.exceptions.RequestException:
    custom_print("Something wrong with your internet connection", word)
except Exception as e:
    custom_print(str(e), word)
