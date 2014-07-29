# FOR GENERATE_DIFFS
import difflib
import operator
import json

# FOR APPLY_DIFFS
import nltk
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

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

    # # for each hunk, pull line numbers for hunks and append relevant diff lines to a list
    diffs = []

    for hunk in diff_hunks_array:
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

        # parsing lines of diffs for commands by looping through each line
        # if there is a command, adding a dictionary of that command
        # and appending that dictionary to a list of commands

        i = before_start - 1
        j = after_start - 1

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
                    print "Whitespace is bullshit."

            # increment j
            elif line[0] == '+':
                print "Addition detected."
                # increments beforehand because line number is actually (j + 1)
                j += 1

                diff_dict = {'after_line': j, 'before_line': i, 'cmd': '+', 'text': line[1:]}
                diffs.append(diff_dict)

    # conversion of diffs into json object (list of dictionaries) to be stored in database
    diffs = json.dumps(diffs)
    return diffs

def test_diff_gen_seed():
    print "\n\nSeeding empty token, then adding tokens."
    text1 = [""]
    text2 = ["This is a cat.", "This is another cat."]

    expected_result = [{"before_line": 1, "cmd": "+", "after_line": 1, "text": "This is a cat."}, {"before_line": 1, "cmd": "+", "after_line": 2, "text": "This is another cat."}]
    expected_result = json.dumps(expected_result)

    result = generate_diffs(text1, text2)

    if expected_result != result:
        print "Nope, test failed."
        print "Expected: ", str(expected_result)
        print "Output: ", str(result)
    else:
        print "Cool, test passed. Good job, you!"

def test_diff_gen_subtract():
    print "\n\nSubtracting tokens."
    text1 = ["This is a cat.", "This is another cat."]
    text2 = ["This is a cat."]

    expected_result = [{"before_line": 2, "cmd": "-", "after_line": 1, "text": None}]
    expected_result = json.dumps(expected_result)

    result = generate_diffs(text1, text2)

    if expected_result != result:
        print "Nope, test failed."
        print "Expected: ", str(expected_result)
        print "Output: ", str(result)
    else:
        print "Cool, test passed. Good job, you!"

def test_diff_gen_addition():
    print "\n\nAdding tokens."
    text1 = ["This is a cat."]
    text2 = ["This is a cat.", "I am a cat."]

    expected_result = [{"before_line": 1, "cmd": "+", "after_line": 2, "text": "I am a cat."}]
    expected_result = json.dumps(expected_result)

    result = generate_diffs(text1, text2)

    if expected_result != result:
        print "Nope, test failed."
        print "Expected: ", str(expected_result)
        print "Output: ", str(result)
    else:
        print "Cool, test passed. Good job, you!"

def test_diff_gen_switch_token():
    print "\n\nSwitching tokens."
    text1 = ["This is a cat.", "I am a cat."]
    text2 = ["This is a cat.", "I am not a cat."]

    expected_result = [{"before_line": 2, "cmd": "-", "after_line": 1, "text": None}, {"before_line": 2, "cmd": "+", "after_line": 2, "text": "I am not a cat."}]
    expected_result = json.dumps(expected_result)

    result = generate_diffs(text1, text2)

    if expected_result != result:
        print "Nope, test failed."
        print "Expected: ", str(expected_result)
        print "Output: ", str(result)
    else:
        print "Cool, test passed. Good job, you!"

def test_diff_gen_alternate():
    print "\n\nSwapping several tokens."
    text1 = ["I have a cat.", "Her name is Mana.", "My other cat's name is Jiji.", "Jiji sheds a lot.", "Jiji is also fat."]
    text2 = ["Her name is Mana.", "Not the test, my cat.", "Jiji sheds a lot.", "She's my cat."]

    expected_result = [{"before_line": 1, "cmd": "-", "after_line": 0, "text": None}, {"before_line": 3, "cmd": "-", "after_line": 1, "text": None}, {"before_line": 3, "cmd": "+", "after_line": 2, "text": "Not the test, my cat."}, {"before_line": 5, "cmd": "-", "after_line": 3, "text": None}, {"before_line": 5, "cmd": "+", "after_line": 4, "text": "She's my cat."}]
    expected_result = json.dumps(expected_result)

    result = generate_diffs(text1, text2)

    if expected_result != result:
        print "Nope, test failed."
        print "Expected: ", str(expected_result)
        print "Output: ", str(result)
    else:
        print "Cool, test passed. Good job, you!"

def test_diff_gen_delete_first():
    print "\n\nSubtracting the first from several tokens."
    text1 = ["Mana likes to meow.", "Meow.", "Meow.", "Meow meow meow meow meow."]
    text2 = ["Meow.", "Meow.", "Meow meow meow meow meow."]

    expected_result = [{"before_line": 1, "cmd": "-", "after_line": 0, "text": None}]
    expected_result = json.dumps(expected_result)

    result = generate_diffs(text1, text2)

    if expected_result != result:
        print "Nope, test failed."
        print "Expected: ", str(expected_result)
        print "Output: ", str(result)
    else:
        print "Cool, test passed. Good job, you!"

def test_diff_gen_add_first():
    print "\n\nAdding one token in the beginning of a list of several tokens."
    text1 = ["Mana likes to meow.", "Meow.", "Meow.", "Meow meow meow meow meow."]
    text2 = ["Meow meow meow meow.", "Mana likes to meow.", "Meow.", "Meow.", "Meow meow meow meow meow."]

    expected_result = [{"before_line": 0, "cmd": "+", "after_line": 1, "text": "Meow meow meow meow."}]
    expected_result = json.dumps(expected_result)

    result = generate_diffs(text1, text2)

    if expected_result != result:
        print "Nope, test failed."
        print "Expected: ", str(expected_result)
        print "Output: ", str(result)
    else:
        print "Cool, test passed. Good job, you!"

# ------------------------------------------#
#                                           #
#    apply_diffs takes a string and json    #
#  object of diffs and creates new string   #
#                                           #
# ------------------------------------------#

# ** Currently, it takes a string and json object of diffs,
# ** but maybe it should take a list of tokens, and output tokens,
# ** and when text is needed as a string, i.e. displayed on editor,
# ** it can be joined into a string in the controller.

# def apply_diffs(text, diffs):
#     print "APPLYING DIFFS..."
#     new_tokens = []
#     diffs = json.loads(diffs)
#     tokens = tokenizer.tokenize(text)

#     i = 0
#     diff_index = 0
#     # while there are still lines in the original text to loop through
#     while i < (len(tokens)):
#         # while 1. there are still diffs, and 2.1 the line number matches to a diff line number or 2.2. the diff line number is 0
#         while diff_index < len(diffs) and ((i + 1) == diffs[diff_index].get("line") or diffs[diff_index].get("line") == 0):
#             # current is a dictionary with diff instructions
#             current = diffs[diff_index]
#             # -: skip a line without copying
#             if current.get("cmd") == '-':
#                 i += 1
#                 diff_index += 1
#                 print "\nSkipped line."
#                 print "New text is..."
#                 print new_tokens
#             # +: copy a line from original text
#             elif current.get("cmd") == '+':
#                 new_tokens.append(current.get("text"))
#                 diff_index += 1
#                 print "\nAppended new text."
#                 print "New text is..."
#                 print new_tokens
#         # if we are still on a line within the original text and there are no diffs for that line, copy existing text
#         if 0 <= i and i < len(tokens):
#             if tokens[i] == "":
#                 print "\nWhitespace is stupid."
#             else:
#                 new_tokens.append(tokens[i])
#                 print "\nAppended existing text."
#                 print "New text is..."
#                 print new_tokens
#             i += 1
#         print "Moving onto next line.\n"
#     print "Finished looping. Returning new tokens..."
#     print new_tokens
#     return new_tokens
#     # returns a list of tokens

# def test_apply_seed():
#     print "\n\nTake an empty string and add text."

#     text = ""
#     diffs = json.dumps([{"text": "Meow meow meow meow.", "line": 0, "cmd": "+"}, {"text": "Meow mama cat.", "line": 0, "cmd": "+"}])

#     expected_result = ["Meow meow meow meow.", "Meow mama cat."]
#     result = apply_diffs(text, diffs)

#     if expected_result != result:
#         print "Nope, test failed."
#         print "Expected: ", expected_result
#         print "Output: ", result
#     else:
#         print "Cool, test passed. Good job, you!"

# def test_apply_subtract():
#     print "\n\nSubtract a token."

#     text = "Meow meow meow meow. Too many meows."
#     diffs = json.dumps([{"text": None, "line": 2, "cmd": "-"}])

#     expected_result = ["Meow meow meow meow."]
#     result = apply_diffs(text, diffs)

#     if expected_result != result:
#         print "Nope, test failed."
#         print "Expected: ", expected_result
#         print "Output: ", result
#     else:
#         print "Cool, test passed. Good job, you!"

# def test_apply_addition():
#     print "\n\nAdd a token."

#     text = "Meow meow meow meow."
#     diffs = json.dumps([{"text": "Not enough meows.", "line": 1, "cmd": "+"}])

#     expected_result = ["Meow meow meow meow.", "Not enough meows."]
#     result = apply_diffs(text, diffs)

#     if expected_result != result:
#         print "Nope, test failed."
#         print "Expected: ", expected_result
#         print "Output: ", result
#     else:
#         print "Cool, test passed. Good job, you!"

def main():
    test_diff_gen_seed()
    test_diff_gen_subtract()
    test_diff_gen_addition()
    test_diff_gen_switch_token()
    test_diff_gen_alternate()
    test_diff_gen_delete_first()
    test_diff_gen_add_first()

    # print "---------------------------------------"

    # test_apply_seed()
    # test_apply_subtract()
    # test_apply_addition()

    # before_tokens = ["A", "B", "C", "G", "H", "I", "X", "Y", "Z"]
    # after_tokens = ["A", "B", "C", "D", "E", "F", "X", "Z"]
    # generate_diffs(before_tokens, after_tokens)

if __name__ == "__main__":
    main()