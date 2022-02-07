from bs4 import BeautifulSoup as bs
import requests
import json
from string import ascii_lowercase as alphabet


def getWords():

    # query data
    r = requests.get('https://wordfind.com/length/5-letter-words/')
    print('\twordfind.com queried...')

    # parse data
    soup = bs(r.text, 'html.parser')
    # return class #dl
    f = soup.find_all(class_='dl')
    # iterate and store
    words = []
    for thing in f:
        words.append(thing.get_text()[:5])

    print(f'\t{len(words)} words gathered...')
    # write to file
    with open('words.json', 'w') as file:
        json.dump(words, file)

    print('\tdata has been written to words.json...')
    return words


# answer question: what is the most common letter in a word?
# doubles don't count, either a letter occurrs in the word or not
def getStats():
    results = {}
    # initializez results
    for letter in alphabet: results[letter] = 0
    # count letter occurrences
    for word in wordlist:
        for letter in alphabet:
            if letter in word:
                results[letter] += 1

    print(f'\tletters counted...')
    # convert results to list and sort
    s = [(x, results[x]) for x in results]
    s = sorted(s, key=lambda x: x[1])[::-1]

    # write results to file
    with open('stats.json', 'w') as file:
        json.dump(s, file)
    print(f'\tstats written to file...')
    return s


# get words containing the top (j-i) letters
def get_top_words(i,j, wordlist, stats):
    matches = []
    for word in wordlist:
        match = True
        for letter in stats[i:j]:
            if letter[0] not in word:
                match = False
                break
        if match: matches.append(word)
    print(f'\t{len(matches)} matches found...')

    with open(f'topWords_{i}_{j}.json', 'w') as file:
        json.dump(matches, file)
    print(f'\tmatches written to file...')
    return matches


if __name__=='__main__':
    wordlist = getWords()
    stats = getStats()
    print(stats)
    print(len(stats))
    # top word (arose, until)
    t = get_top_words(0,5, wordlist, stats)
    n = get_top_words(5,10, wordlist, stats)
    m = get_top_words(10,15, wordlist, stats)
    print(t)
    print(n)
    print(m)