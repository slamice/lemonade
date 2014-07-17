import difflib

text1_lines = ["This is some example text.", "This is a sentence.", "Hello."]
text2_lines = ["This is some example text.", "Boo.", "Hello."]

d = difflib.Differ()
# creates a diff object
diff = d.compare(text1_lines, text2_lines)
# adds enter between each line of diff info
connect_diff = '\n'.join(diff)
print connect_diff
# makes array of strings of each line
split_diff = connect_diff.split('\n')
print split_diff

# to generate second text from diffs
second_text_array = []

for item in split_diff:
	diff_sign = item[0]
	if diff_sign == '-':
		pass
	elif diff_sign == '+':
		print item[2:]
		second_text_array.append(item[2:])
	else:
		print item[2:]
		second_text_array.append(item[2:])

print ' '.join(second_text_array)