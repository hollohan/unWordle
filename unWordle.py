import json
from random import choice
from os import system
from string import ascii_lowercase as alphabet

clear_srcrn = lambda: system('cls')
ylw  = '\033[93m'
grn  = '\033[92m'
endc = '\033[0m'

class unWordle():
    def __init__(self, words_filename, stats_filename):
        self.wordlist = []
        self.letters_exact = []
        self.letters_partial = []
        self.letters_not = []
        self.letters_not_exact = []
        self.stats = {}
        self.answer = None

        # load wordlist / stats from file
        self.load_wordlist(words_filename)
        self.load_stats(stats_filename)

    def load_wordlist(self, words_filename):
        # write data to file
        with open(words_filename, 'r') as file:
            self.wordlist = json.load(file)

    def load_stats(self, stats_filename):
        # write results to file
        s = 0
        with open(stats_filename, 'r') as file:
            s = json.load(file)
        for thing in s: self.stats[thing[0]] = thing[1]

    
    def contains_letters_exact (self, word):
        matches = [True if word[letter[1]] == letter[0] else False for letter in self.letters_exact]
        if all(matches): return True    # all([]) == True
        return False

    def contains_letters_partial(self, word):
        matches = [True if letter in word else False for letter in self.letters_partial]
        if all(matches): return True
        return False

    def without_letters_not(self, word):
        matches = [True if letter not in word else False for letter in self.letters_not]
        if all(matches): return True
        return False

    def without_letters_notexact(self, word):
        matches = [True if word[letter[1]] != letter[0] else False for letter in self.letters_not_exact]
        if all(matches): return True
        return False

    def find_next_try(self):
        exact_matches  = []
        # find words with exact matches
        
        matches = [word for word in self.wordlist
            if self.contains_letters_exact(word)
            and self.contains_letters_partial(word)
            and self.without_letters_not(word)
            and self.without_letters_notexact(word)
            ]
        return matches

    def decode_result(self, guess, result):
        colorized_response = ''
        for i in range(len(result)):
            if result[i] == 'x':
                self.letters_exact.append( (guess[i], i) )
                self.letters_exact = list(set(self.letters_exact))
                colorized_response += f'{grn}{guess[i]}{endc} '
            elif result[i] == 'p':
                self.letters_partial.append(guess[i])
                self.letters_not_exact.append( (guess[i], i) )
                colorized_response += f'{ylw}{guess[i]}{endc} '
                self.letters_partial = list(set(self.letters_partial))
            elif result[i] == '-':
                if guess[i] in [x[0] for x in self.letters_exact + self.letters_not_exact]:
                    self.letters_not_exact.append((guess[i], i))
                else:
                    self.letters_not.append(guess[i])
                colorized_response += guess[i] + ' '
                self.letters_not = list(set(self.letters_not))
            else: return 0
        return colorized_response

    def calc_word_weight(self, w):
        weight = 0
        for thing in w:
            weight += self.stats[thing]
        return weight

    def response_provider(self, guess):
        response = ''
        for i in range(len(guess)):
            if guess[i] == self.answer[i]: response += 'x'
            elif guess[i] in self.answer: response += 'p'
            else: response += '-'
        return response

    def word_provider(self):
        ans_num = 0
        guessed = []
        while True:
            if ans_num == 0:    word='myope'
            elif ans_num == 1:  word='tunic'
            elif ans_num == 2:  word='lards'
            else:
                word=self.find_next_try()
                word = [w for w in word if w not in guessed]
                word = word[0]
                #print(f'{word=}')
                if word not in guessed:
                    guessed.append(word)
                else: continue

            #print(f'{len(word)=}')
            if not len(word): raise StopIteration
            yield word
            ans_num += 1

    def recalc_stats(self, words):
        results = {}
        # initializez results
        for letter in alphabet: results[letter] = 0
        # count letter occurrences
        for word in words:
            for letter in alphabet:
                if letter in word:
                    results[letter] += 1

        print(f'\tletters counted...')
        # convert results to list and sort
        s = [(x, results[x]) for x in results]
        s = sorted(s, key=lambda x: x[1])[::-1]
        for thing in s: self.stats[thing[0]] = thing[1]


if __name__=='__main__':

    print()
    game_counter = 0
    num_solved = 0
    turns = []
    auto = False

    while True:
        # create unWordle object
        unwdl = unWordle(
            words_filename = 'getData/words.json',
            stats_filename = 'getData/stats.json'
            )

        unwdl.answer = 'skill'
        answer = unwdl.word_provider()
        if game_counter > len(unwdl.wordlist): exit()
        turn_counter = 1
        next_game=False

        unwdl.answer = choice(unwdl.wordlist)
        if auto: print(f'{"-"*6} game# {game_counter} --- {unwdl.answer} {"-"*6}')
        while True:
            # input guess
            if not auto: print(f'\nTurn {turn_counter}')
            if not auto: print('----')
            if auto: guess = next(answer)
            else: guess = input('enter guess: ').lower()
            # confirm 5 chars input
            if len(guess) != 5 or any([not c.isalpha() for c in guess]): continue

            while True:
                # input encoded result
                if auto: enc_result = unwdl.response_provider(guess)
                else: enc_result = input('(x=exact,p=partial,-=none) result: ')
                #print(f'{enc_result=}')
                # confirm 5 xp- chars input
                if len(enc_result) != 5 or not all([c in 'xp-' for c in enc_result]): continue
                elif enc_result == 'xxxxx':
                    if not auto: print('\n' + '-'*20)
                    #print(f':)\t{grn}{" ".join(guess)}{endc}')
                    if not auto: print('-'*20)
                    next_game = True
                    game_counter += 1
                    #print(turns)
                    if turn_counter < 7:
                        num_solved += 1
                    turns.append(turn_counter)
                    break
                else: break

            cr = unwdl.decode_result(guess, enc_result)
            print(f'\t{cr}')

            if next_game: 
                next_game = False
                print()
                break

            #print(f'\nSummary')
            #print(f'-------')
            #print(f'{unwdl.letters_exact=}')
            #print(f'{unwdl.letters_partial=}')
            #print(f'{unwdl.letters_not=}')

            if not auto: 
                p = unwdl.find_next_try()
                unwdl.recalc_stats(p)
                p = [[x, unwdl.calc_word_weight(x)] for x in p]
                p = sorted(p, key=lambda x: x[1])[::-1]
                print('\nPossible Answers')
                print('-------- -------')
                for thing in p: print(thing)
            turn_counter += 1

        if auto: clear_srcrn()
        
        print(f'\nrecord {num_solved/game_counter*100}%')
        print(f'avg turns: {sum(turns)/len(turns)}\n')

        if not auto: break
    print(f'{grn}:){endc}')