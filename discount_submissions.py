##########
# You can run it as:
# python3 discount_submissions.py < course-198-submissions.csv > course-198-discounted-submissions.csv
##########

import fileinput
from collections import defaultdict

d = defaultdict(int) # (step_id, user_id) --> number of submissions 
ok = defaultdict(bool) # (step_id, user_id) --> correct

for line in fileinput.input():
	submission_id, step_id, user_id, attempt_time, submission_time, status = line.strip().split(',')
	key = step_id, user_id
	if not ok[key]:
		d[key] += 1
		if status == 'correct':
			ok[key] = True


print('step_id,user_id,div')

for key, value in d.items():
	print('{},{},{}'.format(key[0], key[1], 1/value))
