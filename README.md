# Lemonade

Lemonade is a version control system for translations and gives translators a clean space to keep track of their progress for their projects. Inspired by Git, Lemonade is a backend-focused project that detects minor changes in text and stores them as a series of differences between a current and previous version, which are used to regenerate text from different points in time. Storing as diffs reduces redundancy in data and optimizes database storage.

Lemonade is a Python application built on Flask and a SQLite database. Python modules used include: difflib, NLTK, unittest, and JSON, and the frontend uses HTML5, CSS3/Sass, Bourbon, and JavaScript/jQuery.

## How do I make it go?
1. Download/clone the Lemonade repo on Github.
2. In shell, cd into the root of your new lemonade directory. 
3. Set up your virtual environment. In shell, input:
```shell
virtualenv env
source env/bin/activate
```
4. Run ```./run.sh```.
5. Congratulations, Lemonade is now running on localhost:5000!

## How does it actually go?
