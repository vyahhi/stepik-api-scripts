import sys
import json
import requests
from openpyxl import load_workbook

if len(sys.argv) < 3:
  print('Usage: python3 {} filename.xlsx course_id'.format(sys.argv[0]))
  exit()

filename = sys.argv[1]
course_id = sys.argv[2]

# USER: get your keys at https://stepik.org/oauth2/applications/ (client type = confidential, authorization grant type = client credentials)
client_id = '...'
client_secret = '...'

hostname = 'https://sb.stepic.org' # without trailing slash 

# Get a token
auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
resp = requests.post('{}/oauth2/token/'.format(hostname), data={'grant_type': 'client_credentials'}, auth=auth)
token = json.loads(resp.text)['access_token']

# Parse XLSX file
wb = load_workbook(filename=filename)
sheet = wb.worksheets[0]

# Add new module (section) to the end of course
api_url = '{}/api/courses/{}'.format(hostname, course_id)
r = requests.get(api_url, headers={'Authorization': 'Bearer '+ token})
sections = r.json()['courses'][0]['sections']
section_position = len(sections) + 1

api_url = '{}/api/sections'.format(hostname)
data = {
  'section': {
    'title': sheet.title,
    'course': course_id,
    'position': section_position
  }
}
r = requests.post(api_url, headers={'Authorization': 'Bearer '+ token}, json=data)
section_id = r.json()['sections'][0]['id']
print('Section ID:', section_id)

# Read XLSX file line by line

unit_position = 1

for line in sheet:

  # PARSE XLSX LINE
  # USER: change it if you have different xlsx structure
  title, number, question, difficulty, correct, wrong1, wrong2, wrong3 = line[:8]
  if not isinstance(number.value, int):
    continue
  # END OF PARSE XLSX LINE

  lesson_title = title.value + ' ' + str(number.value)
  print(lesson_title)
  
  # Create a new lesson
  api_url = '{}/api/lessons'.format(hostname)
  data = {
    'lesson': {
      'title': lesson_title,
      'is_public': False
    }
  }
  r = requests.post(api_url, headers={'Authorization': 'Bearer '+ token}, json=data)
  lesson_id = r.json()['lessons'][0]['id']
  print('Lesson ID:', lesson_id)

  # Add new multiple (single) choice step to this lesson

  api_url = '{}/api/step-sources'.format(hostname)
  data = {
    'stepSource': {
      'block': {
        'name': 'choice',
        'text': str(question.value),
        'source': {
          'options': [
            {'is_correct': True, 'text': str(correct.value), 'feedback': ''},
            {'is_correct': False, 'text': str(wrong1.value), 'feedback': ''},
            {'is_correct': False, 'text': str(wrong2.value), 'feedback': ''},
            {'is_correct': False, 'text': str(wrong3.value), 'feedback': ''},

          ],
          'is_always_correct': False,
          'is_html_enabled': True,
          'sample_size': 4,
          'is_multiple_choice': False,
          'preserve_order': False,
          'is_options_feedback': False
        }
      },
      'lesson': lesson_id,
      'position': 1,
      'cost': 1
    }
  }
  r = requests.post(api_url, headers={'Authorization': 'Bearer '+ token}, json=data)
  step_id = r.json()['step-sources'][0]['id']
  print('Step ID:', step_id)

  # Add new lesson to the new section (it is called unit)
  api_url = '{}/api/units'.format(hostname)
  data = {
    'unit': {
      'section': section_id,
      'lesson': lesson_id,
      'position': unit_position
    }
  }
  unit_position += 1
  r = requests.post(api_url, headers={'Authorization': 'Bearer '+ token}, json=data)
  unit_id = r.json()['units'][0]['id']
  print('Unit ID:', unit_id)

# Your course is ready
print('--> DONE. Check {}/course/{}'.format(hostname, course_id))


