import sys
import json
import requests
from openpyxl import load_workbook

course_id = 291

# USER: get your keys at https://stepik.org/oauth2/applications/ (client type = confidential, authorization grant type = client credentials)
client_id = '...'
client_secret = '...'

hostname = 'https://sb.stepic.org' # without trailing slash 

# Get a token
auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
resp = requests.post('{}/oauth2/token/'.format(hostname), data={'grant_type': 'client_credentials'}, auth=auth)
token = json.loads(resp.text)['access_token']

# Add new module (section) to the end of course
api_url = '{}/api/courses/{}'.format(hostname, course_id)
r = requests.get(api_url, headers={'Authorization': 'Bearer '+ token})
sections = r.json()['courses'][0]['sections']

for section_id in sections:
  api_url = '{}/api/sections/{}'.format(hostname, section_id)
  r = requests.get(api_url, headers={'Authorization': 'Bearer '+ token})
  units = r.json()['sections'][0]['units']
  for unit_id in units:
    api_url = '{}/api/units/{}'.format(hostname, unit_id)
    r = requests.get(api_url, headers={'Authorization': 'Bearer '+ token})
    lesson_id = r.json()['units'][0]['lesson']
    print('Lesson:', lesson_id, '...')
    api_url = '{}/api/lessons/{}'.format(hostname, lesson_id)
    r = requests.get(api_url, headers={'Authorization': 'Bearer '+ token})
    lesson = r.json()['lessons'][0]
    lesson['tags'].append(1)
    data = { 'lesson': lesson }
    r = requests.put(api_url, headers={'Authorization': 'Bearer '+ token}, json=data)
    print('  ...', r)

