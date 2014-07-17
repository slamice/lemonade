import difflib
import re

string1 = "Here is a ton of stuff that is the same. Here is a ton of stuff that is the same. Here is a ton of stuff that is the same. Here is a ton of stuff that is the same. Here is a ton of stuff that is the same. Here is a ton of stuff that is the same. Here is a ton of stuff that is the same. Here is a ton of stuff that is the same. Here is a ton of stuff that is the same. Here is a ton of stuff that is the same. Here is a ton of stuff that is the same. This part is different."
string2 = "Here is a ton of stuff that is the same. Here is a ton of stuff that is the same. Here is a ton of stuff that is the same. Here is a ton of stuff that is the same. Here is a ton of stuff that is the same. Here is a ton of stuff that is the same. Here is a ton of stuff that is the same. Here is a ton of stuff that is the same. Here is a ton of stuff that is the same. Here is a ton of stuff that is the same. Here is a ton of stuff that is the same. Different part is here. Aloha."

array1 = string1.split('. ')
array2 = string2.split('. ')

context_diff = difflib.context_diff(array1, array2)
# context_diff would be stored in the db

# context_diff_array = []

for line in context_diff:
	# context_diff_array.append(line)
	# print line
	search = re.match("\*{3} .* \*{4}", line)
	print search
	# context _diff_array[3] has the line number of changes






# for each difference:
# 	array1[line in which it is different] = the new text
# print '.'.join(array1)