import difflib
import re
import nltk.data

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

string1 = """Hi. Hi. Hi. Hi. Hi. Hi. Hi. Hi. Hi. Hi. Hi. Hi. Hi. Hi. Aloha. Banana. Cream. Door. Elephant.

And a space."""
string2 = """Hi. Hi. Hi. Hi. Hi. Apple. Cream. Elephant. Ferengi.

And a space. Extra text."""

array1 = tokenizer.tokenize(string1)
array2 = tokenizer.tokenize(string2)

context_diff = difflib.context_diff(array1, array2)
# context_diff would be stored in the db

context_diff_array = []
for line in context_diff:
    context_diff_array.append(line)

context_diff_str = '\n'.join(context_diff_array)
# print context_diff_str
# turned context_diff into a string instead of an object

before_diff = re.search(r'\*{3} .* \*{4}\n\n(.*\n)*(?=(\-{3} .* \-{4}))', context_diff_str)
before_diff = before_diff.group()
print before_diff
# shows the before info (type: str)

after_diff = re.search(r'\-{3} .* \-{4}\n\n(.*\n)*((?=-{3})|.*)', context_diff_str)
after_diff = after_diff.group()
print after_diff
# shows the after info (type: str)

after_diff_array = after_diff.split('\n')
# after_diff_array[0]: has line # information
line_nums = after_diff_array[0]
# array_diff_array[3~]: have line differences

# have to subtract 1 for line numbers because the items are in an array
start_line = re.search(r'\d*(?=,)', line_nums)
start_line = int(start_line.group())
print start_line

end_line = re.search(r'\d*(?= -{3})', line_nums)
end_line = int(end_line.group())
print end_line

after_diff_info = after_diff_array[3:]
replacement_text_array = []
for line in after_diff_info:
    replacement_text_array.append(line[2:])

print array1[(start_line-1):(end_line)]