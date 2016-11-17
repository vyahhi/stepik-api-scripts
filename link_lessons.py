# Run with Python 3
# Script adds (by link) all lessons from course_from_id into the new single module to course_to_id.

import json
import requests

# 1. Get your keys at https://stepik.org/oauth2/applications/ (client type = confidential, authorization grant type = client credentials)
client_id = '...'
client_secret = '...'
course_from_id = 1
course_to_id = 1463

# 2. Get a token
api_host = 'https://stepik.org'
auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
resp = requests.post('{}/oauth2/token/'.format(api_host), data={'grant_type': 'client_credentials'}, auth=auth)
token = json.loads(resp.text)['access_token']

# 3. Define unils functions

def fetch_object(obj_class, obj_id):
	api_url = '{}/api/{}s/{}'.format(api_host, obj_class, obj_id)
	response = requests.get(api_url, headers={'Authorization': 'Bearer ' + token}).json()
	return response['{}s'.format(obj_class)][0]


def fetch_objects(obj_class, obj_ids):
	objs = []
	# Fetch objects by 30 items,
	# so we won't bump into HTTP request length limits
	step_size = 30
	for i in range(0, len(obj_ids), step_size):
		obj_ids_slice = obj_ids[i:i + step_size]
		api_url = '{}/api/{}s?{}'.format(api_host, obj_class, '&'.join('ids[]={}'.format(obj_id) for obj_id in obj_ids_slice))
		response = requests.get(api_url, headers={'Authorization': 'Bearer ' + token}).json()
		objs += response['{}s'.format(obj_class)]
	return objs


# 3. Call API (https://stepik.org/api/docs/) using this token.

# Get Course FROM
course_from = fetch_object('course', course_from_id)
print('Course FROM:', course_from['id'], course_from['title'])

# Get list of lessons of Course FROM
section_ids = course_from['sections']
sections = fetch_objects('section', section_ids)

unit_ids = [unit for section in sections for unit in section['units']]
units = fetch_objects('unit', unit_ids)

lesson_ids = [unit['lesson'] for unit in units]
print('Lessons:', lesson_ids)

# lessons = fetch_objects('lesson', lesson_ids)
# for lesson in lessons:
# 	print('  Lesson:', lesson['id'], lesson['title'])

# Get Course TO
course_to = fetch_object('course', course_to_id)
print('Course TO:', course_to['id'], course_to['title'])

# Add new module (section) to Course TO
api_url = 'https://stepik.org/api/sections'
data = {
	'section': {
		'title': course_from['title'],
		'course': course_to_id,
		'position': len(course_to['sections']) + 1
	}
}
r = requests.post(api_url, headers={'Authorization': 'Bearer '+ token}, json=data)
section = r.json()['sections'][0]
print(' New module:', section['id'], section['title'])

# Link lesson to this new section (it is called unit)
for position, lesson_id in enumerate(lesson_ids):
	api_url = 'https://stepik.org/api/units'
	data = {
		'unit': {
			'section': section['id'],
			'lesson': lesson_id,
			'position': position + 1
		}
	}
	r = requests.post(api_url, headers={'Authorization': 'Bearer '+ token}, json=data)
	unit = r.json()['units'][0]
	print('  Lesson:', unit['lesson'])

###

# Your course is ready
print('Ready. Check https://stepik.org/course/{}'.format(course_to['id']))

###