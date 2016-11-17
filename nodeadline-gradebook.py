import csv
import sys
from collections import defaultdict

structure = open(sys.argv[1])
submissions = open(sys.argv[2])
learners = open(sys.argv[3])

steps = []

for line in structure:
	# course_id,module_id,module_position,lesson_id,lesson_position,step_id,step_position,step_type
	line = line.strip().split(',')
	try:
		module_position = int(line[2])
		lesson_position = int(line[4])
		step_position =  int(line[6])
		step_type = line[7]
		if step_type in ['text', 'video']:
			continue
	except:
		continue
	steps.append((module_position, lesson_position, step_position, line))

steps.sort()

users = defaultdict(dict)

for line in submissions:
	# submission_id,step_id,user_id,attempt_time,submission_time,status	
	line = line.strip().split(',')
	try:
		step_id = int(line[1])
		user_id = int(line[2])
	except:
		continue
	status = True if line[5] == 'correct' else False
	if step_id not in  users[user_id]:
		 users[user_id][step_id] = False
	users[user_id][step_id] |= status

csv_writer = csv.writer(sys.stdout)
row = ['user_id','user_name']
for _, _, _, sline in steps:
	lesson_id = sline[3]
	step_position = sline[6]
	row.append('https://sb.stepic.org/lesson/{}/step/{}'.format(lesson_id, step_position))

row.append('total')
csv_writer.writerow(row)

for line in learners:
	# stepic_id,last_name,first_name,email,last_login,sberbank_id
	line = line.strip().split(',')
	try:
		user_id = int(line[0])
		full_name = '{} {}'.format(line[2], line[1])
	except:
		continue
	row = [user_id, full_name]
	total = 0
	for _, _, _, sline in steps:
		step_id = int(sline[5])
		ok = int(users[user_id].get(step_id, False))
		row.append(ok)
		total += ok
	row.append(total)
	csv_writer.writerow(row)

