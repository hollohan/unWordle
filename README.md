# unWordle
...is an assistant for solving Wordle puzzles.

When prompted, input the word you have tried followed by the result from Wordle.  The result must be a string of 5 characters.  Valid characters are **x**, **p**, and **-**, for exact, potential, and no match.  **unWordle** will provide a list of valid words to use based on the input provided.  The process repeats and the list of options becomes refined.

Setting **auto=True** will allow you to test a strategy.  The strategy is based on elimination and the three initial guesses.  The default words (below) were chosen because they contain letters which are likely to occur in other five letter words.  They can be edited within the **word_provider** method.

- myope
- tunic
- lards
