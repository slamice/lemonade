import json
import model
import difflib
import nltk

tokenizer = nltk.data.load("nltk:english.pickle")

# remade tokenizer
def tokenize(string):
    positions = tokenizer.span_tokenize(string)
    tokens = []
    for position in positions:
        start_pos = position[0]
        end_pos = position[1]
        token = string[start_pos:end_pos]
        tokens.append(token)
    return tokens

# takes in tokens, json object, returns tokens
def apply_diffs(tokens, diffs):
    print "APPLYING DIFFS..."
    new_tokens = []
    diffs = json.loads(diffs)

    i = 0
    j = 0
    diff_index = 0

    # while there are diffs remaining
    while diff_index < len(diffs):
        current = diffs[diff_index]

        # 1. cmd is +, j matches and increase j, diff_index
        if current.get("cmd") == "+" and current.get("after_line") == j + 1:
            add_token = current.get("text")
            new_tokens.append(add_token)

            print "\nAdded existing token."
            print add_token
            diff_index += 1
            j += 1

        # 2. cmd is -, i matches and increase i, diff_index
        elif current.get("cmd") == "-" and current.get("before_line") == i + 1:

            print "\nSkipped deleted line."
            diff_index += 1
            i += 1
        # 3. diffs exist, but none match so copy and increase both
        else:
            existing_token = tokens[i]
            new_tokens.append(existing_token)

            print "\nCopied existing token."
            print existing_token
            i += 1
            j += 1

    # copy remaining from tokens to output
    while i < len(tokens):
        remaining_token = tokens[i]
        if remaining_token == "":
            print "Ignoring empty token."
        else:
            new_tokens.append(remaining_token)
            print "\nCopied remaining tokens."
            print remaining_token
        i += 1

    print "\nReturning new tokens:"
    print new_tokens
    return new_tokens

def parse_hunk(hunk):
    hunk_pieces = hunk.split('\n')
    # hunk_pieces[0] has line numbers
    # hunk_pieces[1] has an empty line
    # hunk_pieces[2:] are lines of diffs

    before_lines = hunk_pieces[0].split(' ')[0]
    # -begin_line,end_line

    # if multi-line diffs
    if ',' in before_lines:
        before_start = before_lines.split(',')[0][1:]
        before_end = before_lines.split(',')[1][0:]
    # if single-line diffs
    else:
        before_start = before_lines[1:]
        before_end = before_lines[1:]

    after_lines = hunk_pieces[0].split(' ')[1]
    # +begin_line,end_line
    if ',' in after_lines:
        # print after_lines
        after_start = after_lines.split(',')[0][1:]
        after_end = after_lines.split(',')[1][0:]
    # if single-line diffs
    else:
        after_start = after_lines[1:]
        after_end = after_lines[1:]

    before_start = int(before_start)
    before_end = int(before_end)
    after_start = int(after_start)
    after_end = int(after_end)
    differences = hunk_pieces[2:]
    # this is a set of differences for one hunk
    # ex: [' A', ' B', ' C', '-G', '-H', '-I', '+D', '+E', '+F', ' X', '-Y', ' Z']

    hunk_dict = { 
        "before_start"  : before_start, 
        "before_end"    : before_end, 
        "after_start"   : after_start, 
        "after_end"     : after_end,
        "differences"   : differences
        }
    
    return hunk_dict

def parse_diff_lines(before_start, after_start, differences):
    # parsing lines of diffs for commands by looping through each line
    # if there is a command, adding a dictionary of that command
    # and appending that dictionary to a list of commands
    i = before_start - 1
    j = after_start - 1

    diffs = []

    for line in differences:
        print line
        diff_dict = {}

        # increment both i and j
        if line[0] == ' ':
            i += 1
            j += 1

        # increment i
        elif line[0] == '-':
            print "Deletion detected."
            # increments beforehand because line number is actually (i + 1)
            i += 1

            # text token being deleted
            if line[1:]:
                diff_dict = {'after_line': j, 'before_line': i, 'cmd': '-', 'text': None}
                diffs.append(diff_dict)
                
            # empty token being deleted
            else:
                print "Say no to whitespace."

        # increment j
        elif line[0] == '+':
            print "Addition detected."
            # increments beforehand because line number is actually (j + 1)
            j += 1

            diff_dict = {'after_line': j, 'before_line': i, 'cmd': '+', 'text': line[1:]}
            diffs.append(diff_dict)

    return diffs

# takes in tokens, returns json object
def generate_diffs(before_tokens, after_tokens):
    print "DIFFING TOKENS..."

    # creates diff generator, converts into str
    diff = difflib.unified_diff(before_tokens, after_tokens)
    diff_str = '\n'.join(diff)

    # splitting into array of diff hunk
    # diff_hunks_array[0] is garbage formatting from unified_diff
    # each item after is a set of diffs for a hunk of diffs
    diff_hunks_array = diff_str.split('\n@@ ')
    diff_hunks_array = diff_hunks_array[1:]

    # # for each hunk, pull line numbers for hunks and append relevant diff lines to a list
    diffs_list = []

    for hunk in diff_hunks_array:
        hunk_dict = parse_hunk(hunk)

        before_start = hunk_dict.get("before_start")
        before_end = hunk_dict.get("before_end")
        after_start = hunk_dict.get("after_start")
        after_end = hunk_dict.get("after_end")
        differences = hunk_dict.get("differences")

        diffs = parse_diff_lines(before_start, after_start, differences)
        diffs_list += diffs

    # conversion of diffs into json object (list of dictionaries) to be stored in database
    diffs_list = json.dumps(diffs_list)
    return diffs_list

# takes a commit_id, returns tokens
def construct_commit_id(commit_id):
    # takes a sequence of diffs and apply them sequentially to an initial empty token to produce a list of tokens
    tokens = [""]

    diffs_list = retrieve_diffs(commit_id)

    for diff_set in diffs_list:
        tokens = apply_diffs(tokens, diff_set)

    return tokens

# takes a commit_id, returns list of json objects
def retrieve_diffs(commit_id):
    # takes a commit_id, chases the parent_id, and returns a list of json objects (list of dicts)
    # each json object represents one set of diffs for a specific version/commit
    diffs_list = []
    commit = model.Commit.query_commit_by_id(commit_id)
    project_id = commit.project_id

    commits = model.Commit.query_commits_by_proj_id(project_id)
    commits_dict = {}

    for project_commit in commits:
        commits_dict[project_commit.id] = project_commit

    # all commits before initial commit
    while commit.parent_id != None:
        diffs_set = commit.diffs
        diffs_list.append(diffs_set)
        commit_id = commit.parent_id
        commit = commits_dict.get(commit_id)

    # very initial commit
    diffs_set = commit.diffs
    diffs_list.append(diffs_set)
    
    diffs_list = diffs_list[::-1]

    return diffs_list

def main():
    pass

if __name__ == "__main__":
    main()