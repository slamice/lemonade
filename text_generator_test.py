import difflib
import operator
import nltk.data
import json

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

def tokenize(text):
    return tokenizer.tokenize(text)

def generate_diffs_json(text1, text2):
    # creates diff generator
    diff = difflib.unified_diff(text1, text2)

    # conversion to array string
    diff_array = []
    for line in diff:
        diff_array.append(line)
    diff_str = '\n'.join(diff_array)

    # splitting into array of diff hunk
    # diff_hunks_array[0] is garbage formatting from unified_diff
    # each item after is a set of diffs for a hunk of diffs
    diff_hunks_array = diff_str.split('\n@@ ')
    diff_hunks_array = diff_hunks_array[1:]

    # for each hunk, pull line numbers for chunks and append relevant diff lines to a list
    diffs = []

    for hunk in diff_hunks_array:
        hunk_pieces = hunk.split('\n')
        # hunk_pieces[0] has line numbers
        # hunk_pieces[1] has an empty line
        # hunk_pieces[2:] are lines of diffs

        beginning_lines = hunk_pieces[0].split(' ')[0]
        # if one line of diff, beginning_lines[1:] is where the diffs begin
        if ',' not in beginning_lines:
            begin = beginning_lines[1:]
        # if more than one line of diff, there is a , so have to split and take first #
        else:
            begin = beginning_lines.split(',')[0][1:]
        differences = hunk_pieces[2:]

        # parsing lines of diffs for commands by looping through each line
        # and if there is a command, adding a dictionary of that command
        # and appending that dictionary to a list of commands
        line_num = int(begin) - 1
        for line in differences:
            diff_dict = {}
            if line[0] == ' ':
                line_num += 1
            while line[0] == '-' or line[0] == '+':
                if line[0] == '-':
                    line_num += 1
                    diff_dict = {'line': line_num, 'cmd': '-', 'text': None}
                    diffs.append(diff_dict)
                    break
                elif line[0] == '+':
                    diff_dict = {'line': line_num, 'cmd': '+', 'text': line[1:]}
                    diffs.append(diff_dict)
                    break

    # making sure + comes before - so that it doesn't skip lines before it's supposed to
    diffs = sorted(diffs, key=operator.itemgetter('line','cmd'))
    diffs = json.dumps(diffs)

    print diffs
    return diffs
    # this returns list of dicts with line nums, +/-, and text if cmd is +
    # eventually this will be put into the database

def apply_diffs(text1, diffs):
    diffs = json.loads(diffs)
    new_text = []

    i = 0
    # while there are still lines in the original text to loop through
    while i < (len(text1)):
        while len(diffs) > 0 and ((i + 1) == diffs[0].get("line") or diffs[0].get("line") == 0):
            current = diffs.pop(0)
            if current.get("cmd") == '-':
                i += 1
            elif current.get("cmd") == '+':
                new_text.append(current.get("text"))
        if 0 <= i and i < len(text1):
            new_text.append(text1[i])
            i += 1
    print ' '.join(new_text)

def main():
    # ""
    # "Alphabet soup. Banana. Hello. No."
    # "Banana. California. Arkansas. No."
    text1 = ""
    text2 = "Hi. Text. Alphabet soup. Banana. Hello. No."
    text1 = tokenize(text1)
    text2 = tokenize(text2)
    diffs = generate_diffs_json(text1, text2)
    apply_diffs(text1, diffs)

if __name__ == "__main__":
    main()