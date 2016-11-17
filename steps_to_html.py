# Run with Python 3
import json
import requests
import itertools

# parameters here:

# 1. Get your keys at https://stepic.org/oauth2/applications/ (client type = confidential,
# authorization grant type = client credentials)
client_id = "..."
client_secret = "..."
api_host = 'https://stepic.org'
course_ids = [569, 647, 648, 677, 678]


# 2. Get a token
auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
resp = requests.post('https://stepic.org/oauth2/token/',
                     data={'grant_type': 'client_credentials'},
                     auth=auth
                     )
token = json.loads(resp.text)['access_token']

# 3. Call API (https://stepic.org/api/docs/) using this token.

def fetch_object(api_host, obj_class, obj_id):
	api_url = '{}/api/{}s/{}'.format(api_host, obj_class, obj_id)
	response = json.loads(requests.get(api_url, headers={'Authorization': 'Bearer '+ token}).text)
	obj = response['{}s'.format(obj_class)][0]
	return obj

def fetch_objects(api_host, obj_class, obj_ids):
	api_url = '{}/api/{}s?{}'.format(api_host, obj_class, '&'.join('ids[]={}'.format(obj_id) for obj_id in obj_ids))
	response = json.loads(requests.get(api_url, headers={'Authorization': 'Bearer '+ token}).text)
	objs = response['{}s'.format(obj_class)]
	return objs

for course_id in course_ids:
	course = fetch_object(api_host, 'course', course_id)

	sections = fetch_objects(api_host, 'section', course['sections'])

	unit_ids = [unit for section in sections for unit in section['units']]
	units = fetch_objects(api_host, 'unit', unit_ids)

	lesson_ids = [unit['lesson'] for unit in units]
	lessons = fetch_objects(api_host, 'lesson', lesson_ids)

	step_ids = [step for lesson in lessons for step in lesson['steps']]
	steps = fetch_objects(api_host, 'step', step_ids)

	f = open('course{}.html'.format(course_id), 'w')

	for step in steps:
		text = step['block']['text']
		url = '<a href="https://stepic.org/lesson/{}/step/{}">{}</a>'.format(step['lesson'], step['position'], step['id'])
		f.write('<h1>{}</h1>'.format(url))
		f.write(text)
		f.write('<hr>')

	f.close()