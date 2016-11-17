# Run with Python 3
import requests

# Enter parameters below:
# 1. Get your keys at https://stepik.org/oauth2/applications/
# (client type = confidential, authorization grant type = client credentials)
client_id = '...'
client_secret = '...'
api_host = 'https://stepik.org'
course_id = 568

# 2. Get a token
auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
response = requests.post('https://stepik.org/oauth2/token/',
                         data={'grant_type': 'client_credentials'},
                         auth=auth)
token = response.json().get('access_token', None)
if not token:
    print('Unable to authorize with provided credentials')
    exit(1)


# 3. Call API (https://stepik.org/api/docs/) using this token.
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

course = fetch_object('course', course_id)
tag = course['tags'][0]

print('Course', course)
print('Tag', tag)

print('user tag skill uncertainty')

learners = fetch_object('group', course['learners_group'])
for user in learners['users']:
    api_url = '{}/api/tag-progresses?user={}&tag={}'.format(api_host, user, tag)
    response = requests.get(api_url, headers={'Authorization': 'Bearer ' + token}).json()
    objects = response['tag-progresses']
    if len(objects):
        tag_progress = objects[0]
        skill = tag_progress['skill']
        uncertainty = tag_progress['uncertainty']
    else:
        skill = 'NaN'
        uncertainty = 'NaN'
    print(user, tag, skill, uncertainty)

