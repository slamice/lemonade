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

    diffs_list = []
    for hunk in diff_hunks_array:
        hunk_pieces = hunk.split('\n')
        begin, end = hunk_pieces[0].split(' ')[0][1:].split(',')
        # line_pos = (int(begin), int(end))
        # pulls line numbers
        differences = hunk_pieces[2:]

        diffs = []
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
        diffs_list.append(diffs)
    return diffs_list

def apply_diffs(text1, diffs):
    new_text = []
    text1 = text1.split()
    i = 0
    # i is equal to line number - 1
    while i < (len(text1)-1):
        new_text.append(text1[i])
        # something is going to change here where
        # it has to see whether there are diffs at that particular line
        while diffs:
            current = diffs.pop(0)
            if current[0] == '-':
                i += 1
            elif current[0] == '+':
                new_text.append(current[1:])
    return ' '.join(new_text)

if __name__ == "__main__":
    text1 = "1 2 3 4 5 6 7 a a a a a a a a a zebra"
    text2 = "1 3' 4' 6', 7' a a a a a a a a a zoo"
    diffs = diff(text1, text2)
    # apply_diffs(text1, diffs)