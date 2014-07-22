import difflib
import nltk.data

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

def tokenize(text):
    return tokenizer.tokenize(text)

def diff(text1, text2):
    diff = difflib.unified_diff(text1, text2)

    diff_array = []
    for line in diff:
        diff_array.append(line)
    diff_str = '\n'.join(diff_array)
    diff_hunks_array = diff_str.split('\n@@ ')
    diff_hunks_array = diff_hunks_array[1:]

    diffs = []
    for hunk in diff_hunks_array:
        hunk_pieces = hunk.split('\n')
        if len(hunk_pieces[0]) > 8:
            begin, end = hunk_pieces[0].split(' ')[0][1:].split(',')
            differences = hunk_pieces[2:]
        elif len(hunk_pieces[0]) <= 8:
            begin = hunk_pieces[0][1]
            end = hunk_pieces[0][4]
            differences = hunk_pieces[2:]

        line_num = int(begin) - 1
        for line in differences:
            if line[0] == ' ':
                line_num += 1
            while line[0] == '-' or line[0] == '+':
                if line[0] == '-':
                    line_num += 1
                    diffs.append((line_num, '-', None))
                    break
                elif line[0] == '+':
                    diffs.append((line_num, line[0], line[1:]))
                    break
    diffs = sorted(diffs)
    return diffs
    # this returns a list of tuples: (line number, command, args)

def apply_diffs(text1, diffs):
    new_text = []

    i = 0
    while i < (len(text1)):
        while len(diffs) > 0 and (i + 1) == diffs[0][0]:
            current = diffs.pop(0)
            if current[1] == '-':
                i += 1
            elif current[1] == '+':
                new_text.append(current[2])
        if 0 <= i and i < len(text1):
            new_text.append(text1[i])
            i += 1
    return ' '.join(new_text)

if __name__ == "__main__":
    text1 = "Here's a sentence. b. c. d. e. f."
    text2 = "Here's a sentence. b. c. d. zip. f. zop. zoop."
    text1 = tokenize(text1)
    text2 = tokenize(text2)
    diffs = diff(text1, text2)
    print apply_diffs(text1, diffs)