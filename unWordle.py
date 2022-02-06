import json

word_list = []
letters_exact = []
letters_partial = []
letters_not = []
stats = {}

def load_wordlist():
    global word_list
    # write data to file
    with open('words.json', 'r') as file:
        word_list = json.load(file)

def load_stats():
    global stats
    # write results to file
    s = 0
    with open('stats.json', 'r') as file:
        s = json.load(file)
    for thing in s: stats[thing[0]] = thing[1]

def find_next_try(letter_at=[], letters_contained=[], letters_not=[]):

    exact_matches  = []
    # find words with exact matches
    for word in word_list:
        matches = [True if word[letter[1]] == letter[0] else False for letter in letter_at]
        if all(matches): exact_matches.append(word)
    # find words with partial matches
    partial_matches = []
    for word in exact_matches:
        matches = [True if letter in word else False for letter in letters_contained]
        if all(matches): partial_matches.append(word)
    # find words without letters_not
    noneless_matches = []
    for word in partial_matches:
        matches = [True if letter not in word else False for letter in letters_not]
        if all(matches): noneless_matches.append(word)
    print(f'noneless_matches=')
    return noneless_matches

def decode_result(guess, result):
    for i in range(len(result)):
        if result[i] == 'x': letters_exact.append( (guess[i], i) )
        elif result[i] == 'p': letters_partial.append(guess[i])
        elif result[i] == '-': letters_not.append(guess[i])
        else: return 0
    return 1

def calc_word_weight(w):
    weight = 0
    for thing in set(w):
        weight += stats[thing]
    return weight

if __name__=='__main__':
    
    # load word_list from file
    load_wordlist()
    # load letter stats
    load_stats()

    #start = input('starting word: ')
    while True:
        # input 5 letter word
        print('\nTurn')
        print('----')
        guess = input('enter guess: ')
        # confirm 5 chars input
        if len(guess) != 5 or any([c.isnumeric() for c in guess]): continue

        while True:
            # input encoded result
            enc_result = input('(x=exact,p=partial,-=none) result: ')
            # confirm 5 xp- chars input
            if len(enc_result) != 5 or not all([c in 'xp-' for c in enc_result]): continue
            elif enc_result == 'xxxxx':
                print('\n' + '-'*20)
                print(f'{guess} :)')
                print('-'*20)
                exit()
            else: break
        decode_result(guess, enc_result)

        print(f'\nSummary')
        print(f'-------')
        print(f'{letters_exact=}')
        print(f'{letters_partial=}')
        print(f'{letters_not=}')


        p = find_next_try(letters_exact, letters_partial, letters_not)
        p = [[x, calc_word_weight(x)] for x in p]
        p = sorted(p, key=lambda x: x[1])[::-1]
        print('\nPossible Answers')
        print('-------- -------')
        for thing in p[:5]: print(thing)
        print(f'and {len(p) - 5} more')
        



