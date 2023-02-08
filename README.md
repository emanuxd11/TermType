# TermType
Terminal based typing game written in Python!


### What I've added so far:

- **Text highlighting** - The section of text you've already typed is shown in white, while the rest is dimmed.
- **Cursor** - When you type, the current character is highlighted in either white, in case the previous character was input correctly, or red, in case the previous character was wrong.
- **Multiple texts** - Upon starting, the game, a random text will be picked for you to type. These were shamelessly stolen from [TypeRacer's text database](https://data.typeracer.com/pit/texts). I also plan on updating this in the future (see next section).
- **Typing stats** - When you finish typing a text, you'll get feedback on your typing speed and accuracy.
- **Timer** - Above the text, there is a timer. However, this isn't perfect (see next section).


### What I plan on adding in future updates:

- **ncurses support** - Currently I am not using ncurses, I plan on changing this in the future.
- **Backspace support** - In the current state, when you mistype a character, the cursor just blocks, not allowing you to type further. However, this feels a bit awkward because, naturally, your first instict would be to backspace, deleting the few characters you typed before realizing the mistake, and retype the wrong section. I plan on fixing this by adding a backspace feature that would give you the option to continue typing or fix your typo.
- **Better timer** - The timer only updates when you insert a new character and the whole screen updates at once. Obviously, this isn't ideal and I plan on making it so that the timer updates independently from the text.
- **Better visualization** - As opppose to the text being presented in a single, terminal-wide, line, there would be a word limit per line, I believe that it would look nicer this way.
- **Different visualization modes** - Ideally, I'd like to add at least another visualization option where, instead of seeing the text all at once with the typed section highlighted in a different shade, you'd be shown only the current word, one at a time.
- **Keyboard visualizer** - On the bottom of the screen you'd be able to see your keyboard, and the keys being highlighted as you type. This would have support for different keyboard standards (QWERTY, AZERTY, etc...).
- **More text support** - While the program already supports an indefinite amount of texts, these all have to be added manually, and are stored in a plain .txt file. I also plan on updating this to make it more practical.
- **Type anything** - Feature that would allow you to type your own text, from a file you provided.

