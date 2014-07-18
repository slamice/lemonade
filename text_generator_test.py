def diff(text1, text2):
    # this is dummy diff
    diffs = ["-2", "-3", "+3'", "-4", "+4'", "-5", "+6", "+7"]
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
    print ' '.join(new_text)

if __name__ == "__main__":
    text1 = "1 2 3 4 5"
    text2 = "1 3' 4' 6, 7"
    diffs = diff(text1, text2)
    apply_diffs(text1, diffs)