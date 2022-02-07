import json
from random import choice

from sympy import solve_undetermined_coeffs

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

        # load wordlist from file
        # load letter stats
        self.load_wordlist(words_filename)
        self.load_stats(stats_filename)

    def load_wordlist(self, words_filename):
        # write data to file
        with open(words_filename, 'r') as file: #with open('words.json', 'r') as file:
            self.wordlist = json.load(file)

    def load_stats(self, stats_filename):
        # write results to file
        s = 0
        with open(stats_filename, 'r') as file: # with open('stats.json', 'r') as file:
            s = json.load(file)
        for thing in s: self.stats[thing[0]] = thing[1]

    def find_next_try(self):

        letter_at = self.letters_exact
        letters_contained = self.letters_partial
        letters_not = self.letters_not

        exact_matches  = []
        # find words with exact matches
        for word in self.wordlist:
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
        #print(f'noneless_matches=')

        matches_not_exact = []
        for word in noneless_matches:
            matches = [True if word[letter[1]] != letter[0] else False for letter in self.letters_not_exact]
            if all(matches): matches_not_exact.append(word)
        return matches_not_exact

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



if __name__=='__main__':

    print()
    game_counter = 0
    num_solved = 0
    turns = []
    auto = True

    while True:

        # create unWordle object
        unwdl = unWordle(
            words_filename = 'words.json',
            stats_filename = 'stats.json'
            )

        unwdl.answer = 'skill'
        answer = unwdl.word_provider()
        if game_counter > len(unwdl.wordlist): exit()
        turn_counter = 1
        next_game=False

        unwdl.answer = choice(unwdl.wordlist)
        print(f'{"-"*6} game# {game_counter} --- {unwdl.answer} {"-"*6}')
        while True:
            # input 5 letter word
            if not auto: print(f'\nTurn {turn_counter}')
            if not auto: print('----')
            if auto:
                guess = next(answer)
                #print(f'enter guess: {guess}')
            else: guess = input('enter guess: ')
            # confirm 5 chars input
            if len(guess) != 5 or any([c.isnumeric() for c in guess]): continue

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
                p = [[x, unwdl.calc_word_weight(x)] for x in p]
                p = sorted(p, key=lambda x: x[1])[::-1]
                print('\nPossible Answers')
                print('-------- -------')
                for thing in p[:5]: print(thing)
                print(f'and {len(p[:4])} more')
            turn_counter += 1

        print(f'\nrecorcd {num_solved/game_counter*100}%')
        print(f'avg turns: {sum(turns)/len(turns)}\n')
        if not auto: exit()