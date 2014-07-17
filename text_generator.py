import difflib

version1 = ["first", "second", "third"]
version2 = ["first", "replaced second", "third"]

d = difflib.Differ()
# creates a diff object
diff = d.compare(version1, version2)
# adds enter between each line of diff info
connect_diff = '\n'.join(diff)
print connect_diff
# makes array of strings of each line
split_diff = connect_diff.split('\n')
print split_diff

# to generate second text from diffs
additions = []
deletions = []

for item in split_diff:
	diff_sign = item[0]
	if diff_sign == '-':
		deletions.append(item[2:])
	elif diff_sign == '+':
		additions.append(item[2:])

print deletions
print additions