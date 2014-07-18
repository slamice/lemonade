import difflib

def diff(text1, text2):
    text1 = text1.split()
    text2 = text2.split()
    diff = difflib.unified_diff(text1, text2)

    diff_array = []
    for line in diff:
        diff_array.append(line)
    diff_str = '\n'.join(diff_array)
    diff_hunks_array = diff_str.split('\n@@ ')
    diff_hunks_array = diff_hunks_array[1:]

    for hunk in diff_hunks_array:
        hunk_pieces = hunk.split('\n')
        begin, end = hunk_pieces[0].split(' ')[0][1:].split(',')
        line_pos = (int(begin), int(end))
        # pulls line numbers

        diffs = []
        for line in hunk_pieces[3:]:
            while line[0] == '-' or line[0] == '+':
                diffs.append(line)
                break
        return diffs

def apply_diffs(text1, diffs):
    new_text = []
    text1 = text1.split()
    i = 0
    while i < (len(text1)-1):
        new_text.append(text1[i])
        while diffs:
            current = diffs.pop(0)
            if current[0] == '-':
                i += 1
            elif current[0] == '+':
                new_text.append(current[1:])
    return ' '.join(new_text)

if __name__ == "__main__":
    text1 = "1 2 3 4 5 6 7"
    text2 = "1 3' 4' 6', 7'"
    diffs = diff(text1, text2)
    print apply_diffs(text1, diffs)