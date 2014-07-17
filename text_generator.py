import difflib
import re
import nltk.data

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

string1 = "Here is a ton of stuff that is the same. Here is a ton of stuff that is the same. Here is a ton of stuff that is the same. Here is a ton of stuff that is the same. Here is a ton of stuff that is the same. Here is a ton of stuff that is the same. Here is a ton of stuff that is the same. Here is a ton of stuff that is the same. Here is a ton of stuff that is the same. Here is a ton of stuff that is the same. This part is different."
string2 = "Here is a ton of stuff that is the same. Here is a ton of stuff that is the same. Here is a ton of stuff that is the same. Here is a ton of stuff that is the same. Here is a ton of stuff that is the same? Here is a ton of stuff that is the same. Here is a ton of stuff that is the same. Here is a ton of stuff that is the same. Here is a ton of stuff that is the same. Different part is here. Aloha."

array1 = tokenizer.tokenize(string1)
array2 = tokenizer.tokenize(string2)

context_diff = difflib.context_diff(array1, array2)
# context_diff would be stored in the db

context_diff_array = []

for line in context_diff:
	context_diff_array.append(line)

context_diff_str = '\n'.join(context_diff_array)

before_pos = re.search(r'\*{3} .* \*{4}\n\n(  .*\n)*(! .*\n)*', context_diff_str)
before_diff = before_pos.group()
print before_diff

after_pos = re.search(r'\-{3} .* \-{4}\n\n(  .*\n)*(! .*(\n|))*', context_diff_str)
after_diff = after_pos.group()
print after_diff

before_array = before_diff.split('\n')
print before_array
# before_array[0]: *** begin_line#, end_line# ****
# before_array[1]: empty string/white space
# before_array[2]: this is line begin_line#
# eventually use lstrip somewhere?
# for line in before_array:
# 	if line[0] == '!':
# 		print "!"

# for each difference:
# 	array1[line in which it iss different] = the new text
# print '.'.join(array1)