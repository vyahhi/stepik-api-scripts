# Run with Python 3
import csv
import json
import requests
import datetime

## DATA STARTS

course_ids = [217, 83, 73, 76, 524, 7, 187, 157, 67, 125, 401, 497, 129, 75, 150]

user_emails = """
first@email.com
second@email.org
""".strip().splitlines()

print(user_emails)

### DATA ENDS
# Enter parameters below:
# 1. Get your keys at https://stepic.org/oauth2/applications/ (client type = confidential,
# authorization grant type = client credentials)
client_id = '...'
client_secret = '...'
api_host = 'https://stepic.org'

# 2. Get a token
auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
resp = requests.post('https://stepic.org/oauth2/token/',
                     data={'grant_type': 'client_credentials'},
                     auth=auth
                     )
token = resp.json().get('access_token')
if not token:
    raise RuntimeWarning('Client id/secret is probably incorrect')


# 3. Call API (https://stepic.org/api/docs/) using this token.
def fetch_object(obj_class, obj_id):
    api_url = '{}/api/{}s/{}'.format(api_host, obj_class, obj_id)
    response = requests.get(api_url,
                            headers={'Authorization': 'Bearer ' + token}).json()
    return response['{}s'.format(obj_class)][0]


def fetch_objects(obj_class, obj_ids):
    objs = []
    # Fetch objects by 30 items,
    # so we won't bump into HTTP request length limits
    step_size = 30
    for i in range(0, len(obj_ids), step_size):
        obj_ids_slice = obj_ids[i:i + step_size]
        api_url = '{}/api/{}s?{}'.format(api_host, obj_class,
                                         '&'.join('ids[]={}'.format(obj_id)
                                                  for obj_id in obj_ids_slice))
        response = requests.get(api_url,
                                headers={'Authorization': 'Bearer ' + token}
                                ).json()
        objs += response['{}s'.format(obj_class)]
    return objs

today = datetime.datetime.now().date().isoformat()
csv_file = open('mts-{}.csv'.format(today), 'w')
csv_writer = csv.writer(csv_file)

# COURSE NAMES:

header = ['email']

for course_id in course_ids:
    course = fetch_object('course', course_id)
    header.append('{} {}'.format(course['id'], course['title']))

csv_writer.writerow(header)

# MAX COST FOR EACH COURSE:

row = ['MAX']

for course_id in course_ids:
    api_url = '{}/api/progresses/{}-{}'.format(api_host, 78, course_id)
    response = requests.get(api_url, headers={'Authorization': 'Bearer ' + token}).json()
    progress = response['progresses'][0]
    row.append(progress['cost'])

csv_writer.writerow(row)

# STUDENTS SCORE FOR EACH STUDENT AND COURSE:

for user_email in user_emails:
    row = [user_email]
    for course_id in course_ids:
        api_url = '{}/api/course-grades?course={}&search={}'.format(api_host, course_id, user_email)
        response = requests.get(api_url, headers={'Authorization': 'Bearer ' + token}).json()
        if not response['course-grades']:
            row.append('-')
        else:
            course_grade = response['course-grades'][0]
            row.append(course_grade['score'])
    csv_writer.writerow(row)

csv_file.close()

