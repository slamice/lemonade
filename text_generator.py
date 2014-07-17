import difflib
import re
import nltk.data

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

def tokenize_text(string):
    return tokenizer.tokenize(string)

def grab_diffs_array(array1, array2):
    context_diff = difflib.context_diff(array1, array2)
    context_diff_array = []
    for line in context_diff:
        context_diff_array.append(line)
    context_diff_str = '\n'.join(context_diff_array)

    array = context_diff_str.split('***************')
    return array

def grab_before_hunk(context_diff):
    before_hunk = re.search(r'\*{3} \d*,\d* \*{4}\n\n(.*\n)*?(?=-{3} \d*,\d* -{4})', context_diff)
    before_hunk = before_hunk.group()
    return before_hunk

def grab_after_hunk(context_diff):
    after_hunk = re.search(r'\-{3} \d*,\d* \-{4}\n\n(.*\n)*?.*(?=(\*{15})|$)', context_diff)
    after_hunk = after_hunk.group()
    return after_hunk

def grab_line_nums(before_hunk):
    before_hunk = before_hunk.split('\n')
    start_line = re.search(r'\d*(?=,)', before_hunk[0])
    start_line = int(start_line.group())

    end_line = re.search(r'\d*(?= \*{3})', before_hunk[0])
    end_line = int(end_line.group())
    return (start_line, end_line)

def generate_new_hunk(after_hunk):
    after_hunk = after_hunk.split('\n')
    after_hunk = after_hunk[2:]
    new_hunk = []
    for line in after_hunk:
        new_hunk.append(line[2:])
    return new_hunk

def replace_text(line_nums, before_array, new_hunk):
    replace_from_num = line_nums[0] - 1
    replace_to_num = line_nums[1]
    before_array[replace_from_num:replace_to_num] = new_hunk
    return ' '.join(before_array)

def main():
    string1 = """Animal. Blue. Cat. Dog. Elephant. Green. Frog. 1. 1. 1. 1. 1. 1. 1. 1. 1. Zoo."""
    string2 = """Animalia. Blue. Cork. Dork. Meow. Frog. 1. 1. 1. 1. 1. 1. 1. 1. 1. Meow."""
    str_array1 = tokenize_text(string1)
    str_array2 = tokenize_text(string2)
    context_diffs = grab_diffs_array(str_array1, str_array2)
    generated_text = ""

    for context_diff in context_diffs[1:]:
        before_hunk = grab_before_hunk(context_diff)
        line_nums = grab_line_nums(before_hunk)
        after_hunk = grab_after_hunk(context_diff)
        new_hunk = generate_new_hunk(after_hunk)
        generated_text = replace_text(line_nums, str_array1, new_hunk)

    print generated_text


if __name__ == "__main__":
    main()