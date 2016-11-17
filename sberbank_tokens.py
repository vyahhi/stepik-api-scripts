import json
import requests
import dateutil.parser

def solve():
    return 'TOP SECRET'

def check(reply):
    if reply == 'TOP SECRET':
        return 1, ';)'

    feedback = """
Вам следует посмотреть следующие уроки:
Статистика: https://sb.stepic.org/invitation/.../
Финансы банка: https://sb.stepic.org/invitation/.../
    """.strip()

    lesson_id = 16953
    user_id = int(reply)

    # Enter parameters below:
    # 1. Get your keys at https://sb.stepic.org/oauth2/applications/
    # (client type = confidential, authorization grant type = client credentials)
    client_id = "..."
    client_secret = "..."
    api_host = 'https://sb.stepic.org'

    # 2. Get a token
    auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
    response = requests.post('{}/oauth2/token/'.format(api_host),
                             data={'grant_type': 'client_credentials'},
                             auth=auth)
    token = response.json().get('access_token', None)
    if not token:
        return 0, 'ERROR: Unable to authorize with provided credentials'

    # 3. Utility functions
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


    # 4. Do the job

    lesson = fetch_object('lesson', lesson_id)
    steps = lesson['steps']
    steps = steps[1:-1] # all steps except of 1st and last

    oks = 0

    for step_id in steps:
        submissions = []
        page = 1
        while True:
            api_url = '{}/api/submissions?user={}&step={}&page={}'.format(api_host, user_id, step_id, page)
            response = requests.get(api_url, headers={'Authorization': 'Bearer ' + token}).json()
            submissions.extend(response['submissions'])
            if not response['meta']['has_next']:
                break
            page += 1
        submissions = [(dateutil.parser.parse(submission['time']), submission['status']) for submission in submissions]
        submissions.sort()
        if submissions and submissions[0][1] == 'correct':
            oks += 1

    if oks * 2 < len(steps):
        return 1, feedback
    else:
        return 1

print(check('2770917'))