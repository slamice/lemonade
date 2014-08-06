# Lemonade ![run mana, run!](https://raw.githubusercontent.com/lalalalinna/lemonade/master/static/imgs/mana-run-small.gif)

Lemonade is a version control system for translations and gives translators a clean space to keep track of their progress for their projects. Inspired by Git, Lemonade is a backend-focused project that detects minor changes in text and stores them as a series of differences between a current and previous version, which are used to regenerate text from different points in time. Storing as diffs reduces redundancy in data and optimizes database storage.

Lemonade is a Python application built on Flask and a SQLite database. Python modules used include: difflib, NLTK, unittest, and JSON. The frontend is built on HTML5, CSS3/Sass, Bourbon, and JavaScript/jQuery/jQuery UI.


## How do I make it go?

1. Download/clone the Lemonade repo on Github.
2. In shell, cd into the root of your new lemonade directory. 
3. Set up your virtual environment. In shell, input:
```shell
virtualenv env
source env/bin/activate
```
4. Run ```./setup.sh```.
5. Congratulations, Lemonade is now running on localhost:5000!

After setup, simply run ```./setup.sh``` to open Lemonade.

## How do I use it?

You studious polygot, you. Let's say you have a short-medium length translation to complete for school or work. As long as your text is in Unicode, you can create a project and input your source text.

The text editor allows you to view your source text and current translation side-by-side. As you work on your translation, be sure to save your progress, also known as a commit, with a message to remind yourself of your work thus far.

You can revert to previous versions of your text in the commits page or switch into another project, both options accessible in the sidebar.

In case of emergency, you can summon Mana the black cat with the cat button next to the save button.

## How does it actually go?

Magic and lemonade.

There are 4 key features in Lemonade, implemented through the backend: saving a commit, constructing text from a commit, generating diffs, and applying diffs. These are all found in ```generators.py```.

1. Saving a commit

