"""
Naughty way to get the data.
"""
import facebook as fb
import json
import requests as r

# global variables
token = ""
graph = fb.GraphAPI(access_token=token, version='2.7')
data = graph.get_object(id='me', fields='posts')
me = data['posts']

def get_likes(id):
    total_likes = 0
    likers = []

    try:
        nav = graph.get_object(id=id, fields='reactions')['reactions']
    except:
        return 0, likers
    
    while True:
        total_likes += len(nav['data'])
        likers += [x['name'] for x in nav['data']]

        if 'next' in nav['paging']:
            nav = json.loads(
                    r.get(nav['paging']['next']).text)
        else:
            break
    return total_likes, likers

with open('data.csv', 'w') as datafile:
    while True:
        for post in me['data']:
            if 'message' in post:
                message = post['message']
            elif 'story' in post:
                message = post['story']
            else:
                message = post['id']

            q_likes, likers = get_likes(post['id'])

            datafile.write('%s;"%s";%d;%s\n' % \
                    (post['created_time'], message.replace('"', "'"), q_likes, 
                        likers.__str__())
                    )

        if 'next' in me['paging']:
            me = json.loads(r.get(me['paging']['next']).text)
        else:
            break

