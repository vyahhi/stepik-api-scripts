#!/usr/bin/python3
import sys

usage = 'Usage: python3 {} course-ID-structure.csv < course-ID-submissions.csv > course-ID-submissions-with-lesson.csv'.format(sys.argv[0])

if len(sys.argv) < 2:
	print(usage)
	exit()

try:
	stepids = {}
	with open(sys.argv[1]) as structure:
		for line in structure:
			line = line.split(',')
			stepids[line[5]] = line

	for line in sys.stdin:
		line = line.strip().split(',')
		line = [stepids[line[1]][3]] + line
		print(','.join(line))
except:
	print(usage)