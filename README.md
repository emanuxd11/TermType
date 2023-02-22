# TermType
TUI single player clone of [TypeRacer](https://play.typeracer.com/) written in Python!


# Main priority as of now
- **Refactoring** - As this started as a simple "let's see if it works" kind of
  project, the code, despite being not even 200 lines, has become a mess.
  Therefore, my main priority as of now is to refactor it, making it more
  extensible so that I can start working on the next features.

# Added/planned features

### What I've added so far:

- **Text highlighting** - The section of text you've already typed is shown in white, while the rest is dimmed.
- **Cursor** - When you type, the current character is highlighted in either white, in case the previous character was input correctly, or red, in case the previous character was wrong.
- **Keyboard visualizer** - Below the text you can see a map of the keyboard with each key press being highlighted with either green for correct or red for wrong.
- **Typing stats** - When you finish typing a text, you'll get feedback on your typing speed and accuracy.
- **Timer** - Above the text, there is a timer. However, this isn't perfect (see next section).
- **Backspace** - Allows you to backspace to fix typos. You'll be allowed to type a few more characters up to a limit. When you reach the limit, your only option will be to backspace and fix your mistake, just like in [TypeRacer](https://play.typeracer.com/). *Please note* that this feature still has a few bugs.
- **More text support** - Using a web scraper I built based off [this idea](),
  you can download all the texts used in the original game directly from [TypeRacer's text database](https://data.typeracer.com/pit/texts).



### What I plan on adding in future updates:

- **Better text retrieval** - Since I have gathered all the data, not only on
  the texts themselves, but also on genre an author, it would be a waste not to
  also display these informations. I intend to make a Text class for this
  purpose.
- **ncurses** - Currently I am not using ncurses, I plan on changing this in the future.
- **Better timer** - The timer only updates when you insert a new character and the whole screen updates at once. Obviously, this isn't ideal and I plan on making it so that the timer updates independently from the text.
- **Better visualization** - As opppose to the text being presented in a single, terminal-wide, line, there would be a word limit per line, I believe that it would look nicer this way.
- **Different visualization modes** - Ideally, I'd like to add at least another visualization option where, instead of seeing the text all at once with the typed section highlighted in a different shade, you'd be shown only the current word, one at a time.
- **Type anything** - Feature that would allow you to type your own text, from a file you provided.



# License
MIT License 
