# FOR GENERATE_DIFFS
import difflib
import operator
import json

# ------------------------------------------#
#                                           #
#    generate_diffs takes 2 tokens lists    #
#  and outputs a json list of dictionaries  #
#                                           #
# ------------------------------------------#

def generate_diffs(before_tokens, after_tokens):
    print "DIFFING TOKENS..."

    # creates diff generator
    diff = difflib.unified_diff(before_tokens, after_tokens)

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
                if line[0] == '+':
                    diff_dict = {'line': line_num, 'cmd': '+', 'text': line[1:]}
                    diffs.append(diff_dict)
                    print "Detected addition."
                    break
                elif line[0] == '-':
                    line_num += 1

                    # if it's deleting empty token
                    if line[1:]:
                        diff_dict = {'line': line_num, 'cmd': '-', 'text': None}
                        diffs.append(diff_dict)
                        print "Detected deletion."
                        break
                    else:
                        print "Whitespace is bullshit."
                        break

    # making sure + comes before - so that it doesn't skip lines before it's supposed to
    diffs = sorted(diffs, key=operator.itemgetter('line','cmd'))
    diffs = json.dumps(diffs)

    return diffs

def test_diff_gen_seed():
    print "\n\nSeeding empty token, then adding tokens."
    text1 = [""]
    text2 = ["This is a cat.", "This is another cat."]

    expected_result = [{"text": "This is a cat.", "line": 1, "cmd": "+"}, {"text": "This is another cat.", "line": 1, "cmd": "+"}]
    expected_result = json.dumps(expected_result)

    result = generate_diffs(text1, text2)

    if expected_result != result:
        print "Nope, test failed."
        print "Expected: ", str(expected_result)
        print "Output: ", str(result)
    else:
        print "Cool."

def test_diff_gen_subtract():
    print "\n\nSubtracting tokens."
    text1 = ["This is a cat.", "This is another cat."]
    text2 = ["This is a cat."]

    expected_result = [{"text": None, "line": 2, "cmd": "-"}]
    expected_result = json.dumps(expected_result)

    result = generate_diffs(text1, text2)

    if expected_result != result:
        print "Nope, test failed."
        print "Expected: ", str(expected_result)
        print "Output: ", str(result)
    else:
        print "Cool."

def test_diff_gen_addition():
    print "\n\nAdding tokens."
    text1 = ["This is a cat."]
    text2 = ["This is a cat.", "I am a cat."]

    expected_result = [{"text": "I am a cat.", "line": 1, "cmd": "+"}]
    expected_result = json.dumps(expected_result)

    result = generate_diffs(text1, text2)

    if expected_result != result:
        print "Nope, test failed."
        print "Expected: ", str(expected_result)
        print "Output: ", str(result)
    else:
        print "Cool."

def test_diff_gen_switch_token():
    print "\n\nSwitching tokens."
    text1 = ["This is a cat.", "I am a cat."]
    text2 = ["This is a cat.", "I am not a cat."]

    expected_result = [{"text": "I am not a cat.", "line": 2, "cmd": "+"}, {"text": None, "line": 2, "cmd": "-"}]
    expected_result = json.dumps(expected_result)

    result = generate_diffs(text1, text2)

    if expected_result != result:
        print "Nope, test failed."
        print "Expected: ", str(expected_result)
        print "Output: ", str(result)
    else:
        print "Cool."

def test_diff_gen_alternate():
    print "\n\nSwapping several tokens."
    text1 = ["I have a cat.", "Her name is Mana.", "My other cat's name is Jiji.", "Jiji sheds a lot.", "Jiji is also fat."]
    text2 = ["Her name is Mana.", "Not the test, my cat.", "Jiji sheds a lot.", "She's my cat."]

    expected_result = [{"text": None, "line": 1, "cmd": "-"}, {"text": "Not the test, my cat.", "line": 3, "cmd": "+"}, {"text": None, "line": 3, "cmd": "-"}, {"text": "She's my cat.", "line": 5, "cmd": "+"}, {"text": None, "line": 5, "cmd": "-"}]
    expected_result = json.dumps(expected_result)

    result = generate_diffs(text1, text2)

    if expected_result != result:
        print "Nope, test failed."
        print "Expected: ", str(expected_result)
        print "Output: ", str(result)
    else:
        print "Cool."

def test_diff_gen_delete_first():
    print "\n\nSubtracting the first from several tokens."
    text1 = ["Mana likes to meow.", "Meow.", "Meow.", "Meow meow meow meow meow."]
    text2 = ["Meow.", "Meow.", "Meow meow meow meow meow."]

    expected_result = [{"text": None, "line": 1, "cmd": "-"}]
    expected_result = json.dumps(expected_result)

    result = generate_diffs(text1, text2)

    if expected_result != result:
        print "Nope, test failed."
        print "Expected: ", str(expected_result)
        print "Output: ", str(result)
    else:
        print "Cool."

def test_diff_gen_add_first():
    print "\n\nAdding one token in the beginning of a list of several tokens."
    text1 = ["Mana likes to meow.", "Meow.", "Meow.", "Meow meow meow meow meow."]
    text2 = ["Meow meow meow meow.", "Mana likes to meow.", "Meow.", "Meow.", "Meow meow meow meow meow."]

    expected_result = [{"text": "Meow meow meow meow.", "line": 0, "cmd": "+"}]
    expected_result = json.dumps(expected_result)

    result = generate_diffs(text1, text2)

    if expected_result != result:
        print "Nope, test failed."
        print "Expected: ", str(expected_result)
        print "Output: ", str(result)
    else:
        print "Cool."

# ------------------------------------------#
#                                           #
#  construct_text takes a string and json   #
#   object of diffs and creates new text    #
#                                           #
# ------------------------------------------#

# ** Currently, it takes a string and json object of diffs,
# ** but maybe it should take a list of tokens and output tokens
# ** and when text is needed as a string, i.e. displayed on editor,
# ** it can be joined into a string in the controller.



def main():
    test_diff_gen_seed()
    test_diff_gen_subtract()
    test_diff_gen_addition()
    test_diff_gen_switch_token()
    test_diff_gen_alternate()
    test_diff_gen_delete_first()
    test_diff_gen_add_first()

    print "---------------------------------------"



if __name__ == "__main__":
    main()