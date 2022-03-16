import subprocess
import argparse, os, csv, json
import time
import pprint
from defines import getCreds, makeApiCall, makeApiPost

"""
https://developers.facebook.com/docs/instagram-api/guides/content-publishing
https://developers.facebook.com/docs/instagram-api/reference/ig-user/media#creating
"""

def get_quota(params):
    url = params['endpoint_base'] + params['instagram_account_id'] + "/content_publishing_limit"
    endpoint_params = {}
    endpoint_params['access_token'] = params['access_token']
    endpoint_params['fields'] = 'quota_usage,config'
    resp = makeApiCall(url, endpoint_params, params['debug'])
    return resp['json_data']['data'][0]['quota_usage']


def create_container(params, post):
    url = params['endpoint_base'] + params['instagram_account_id'] + "/media"
    endpoint_params = {}
    endpoint_params['access_token'] = params['access_token']
    endpoint_params['image_url'] = post['image_url']
    endpoint_params['caption'] = post['caption']
    if 'location_id' in post:
        endpoint_params['location_id'] = post['location_id']
    resp = makeApiPost(url, endpoint_params, params['debug'])
    return resp


def publish_container(params, container_id):
    url = params['endpoint_base'] + params['instagram_account_id'] + "/media_publish"
    endpoint_params = {}
    endpoint_params['access_token'] = params['access_token']
    endpoint_params['creation_id'] = container_id
    resp = makeApiPost(url, endpoint_params, params['debug'])
    return resp


def main():
    params = getCreds()
    params['debug'] = 'yes'
    print(get_quota(params))

    post = {
        'image_url': 'https://raw.githubusercontent.com/is-attic/P0/a1b49ee1169c3cad642cd5838597a24a556efbbd/A_04226__20220220_100213__1.jpg',
        'caption': 'test__0123 #scenery #native'
    }
    
    resp = create_container(params, post)
    id = resp['json_data']['id']
    resp2 = publish_container(params, id)



if __name__ == '__main__':
    main()
