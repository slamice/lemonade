import json
import model
import nltk
import difflib
import operator
from sqlalchemy import desc

def generate_new_diffs(text, project_id):

    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    commit_id = model.session.query(model.Commit). \
        filter_by(project_id = project_id). \
        order_by(desc(model.Commit.id)). \
        first(). \
        id

    prev_text = construct_text_from_commit_id(commit_id)
    prev_tokens = tokenizer.tokenize(prev_text)
    new_tokens = tokenizer.tokenize(text)
    # old_tokens: array of sentences from browser
    # new_tokens: array of sentences constructed by parent_id

    diffs = diff_tokens_to_json(prev_tokens, new_tokens)
    return diffs

def diff_tokens_to_json(text1, text2):
    # creates diff generator
    diff = difflib.unified_diff(text1, text2)

    # conversion to array to string
    diff_array = []
    for line in diff:
        diff_array.append(line)
    diff_str = '\n'.join(diff_array)

    # splitting into array of diff hunk
    # diff_hunks_array[0] is garbage formatting from unified_diff
    # each item after is a set of diffs for a hunk of diffs
    diff_hunks_array = diff_str.split('\n@@ ')
    diff_hunks_array = diff_hunks_array[1:]

    # for each hunk, pull line numbers for hunks and append relevant diff lines to a list
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

    return diffs
    # this returns list of dicts with line nums, +/-, and text if cmd is +
    # eventually this will be put into the database

def apply_diffs(text, diffs):
    new_text = []

    i = 0
    diff_index = 0
    # while there are still lines in the original text to loop through
    while i < (len(text)):
        while diff_index < len(diffs) and ((i + 1) == diffs[diff_index].get("line") or diffs[diff_index].get("line") == 0):
            current = diffs[diff_index]
            if current.get("cmd") == '-':
                i += 1
                diff_index += 1
            elif current.get("cmd") == '+':
                new_text.append(current.get("text"))
                diff_index += 1
        if 0 <= i and i < len(text):
            new_text.append(text[i])
            i += 1
    return new_text

def construct_text_from_commit_id(commit_id):
    # fetch all commits for the project_id
    this_commit = model.session.query(model.Commit).filter_by(id = commit_id).one()
    project_id = this_commit.project_id
    commits = model.session.query(model.Commit).filter(model.Commit.id.between(0, commit_id)).filter_by(project_id = project_id).all()
    # grab a list of all the diffs for each commit previous until the null
    project_diffs = []
    for commit in commits:
        diffs = json.loads(commit.diffs)
        project_diffs.append(diffs)

    text = [""]
    # apply the diffs sequentially from initial to requested
    for diffs in project_diffs:
        text = apply_diffs(text, diffs)
    return ' '.join(text)

def main():
    # ""
    # "Alphabet soup. Banana. Hello. No."
    # "Banana. California. Arkansas. No."
    # "NO. NO. NO. Yes. Here's something completely different."
    construct_text_from_commit_id(1)
    text1 = "Ok. Cool. Very cool."
    print generate_new_diffs(text1, 1)

if __name__ == "__main__":
    main()