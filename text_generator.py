import difflib
import re
import nltk.data

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

def tokenize_text(string):
    return tokenizer.tokenize(string)

def grab_diff_info_str(array1, array2):
    context_diff = difflib.context_diff(array1, array2)
    context_diff_array = []
    for line in context_diff:
        context_diff_array.append(line)
    context_diff_str = '\n'.join(context_diff_array)
    return context_diff_str

def grab_before_hunk(context_diff):
    before_hunk = re.search(r'\*{3} \d*,\d* \*{4}\n\n(.*\n)*?(?=-{3} \d*,\d* -{4})', context_diff)
    before_hunk = before_hunk.group()
    return before_hunk

def grab_after_hunk(context_diff):
    after_hunk = re.search(r'\-{3} \d*,\d* \-{4}\n\n(.*\n)*?.*(?=(\*{15})|$)', context_diff)
    after_hunk = after_hunk.group()
    return after_hunk

def grab_before_start_line_num(before_hunk):
    before_hunk = before_hunk.split('\n')
    start_line = re.search(r'\d*(?=,)', before_hunk[0])
    start_line = int(start_line.group())
    return start_line

def grab_before_end_line_num(before_hunk):
    before_hunk = before_hunk.split('\n')
    end_line = re.search(r'\d*(?= \*{3})', before_hunk[0])
    end_line = int(end_line.group())
    return end_line

def generate_new_hunk(after_hunk):
    after_hunk = after_hunk.split('\n')
    after_hunk = after_hunk[2:]
    new_hunk = []
    for line in after_hunk:
        new_hunk.append(line[2:])
    return new_hunk

def replace_text(before_num1, before_num2, before_array, new_hunk):
    replace_from_num = before_num1 - 1
    replace_to_num = before_num2
    before_array[replace_from_num:replace_to_num] = new_hunk
    return ' '.join(before_array)

def main():
    string1 = """Animal. Blue. Cat. Dog. Elephant. Green. Frog. Zoo."""
    string2 = """Animalia. Blue. Cork. Dork. Meow. Frog. Zoo."""
    str_array1 = tokenize_text(string1)
    str_array2 = tokenize_text(string2)
    context_diff = grab_diff_info_str(str_array1, str_array2)

    # need to account for multiple hunks
    before_hunk = grab_before_hunk(context_diff)
    before_num1 = grab_before_start_line_num(before_hunk)
    before_num2 = grab_before_end_line_num(before_hunk)
    # maybe turn the num1 and num2 in to a tuple instead
    after_hunk = grab_after_hunk(context_diff)
    new_hunk = generate_new_hunk(after_hunk)
    print replace_text(before_num1, before_num2, str_array1, new_hunk)

    # print context_diff

if __name__ == "__main__":
    main()