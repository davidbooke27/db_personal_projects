import requests
import json
import pandas as pd
import time
import requests_cache
from tqdm import tqdm
from IPython.core.display import clear_output

requests_cache.install_cache()


def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


def lastfm_get(payload):
    # define headers and URL
    headers = {'user-agent': 'davidbooke27'}
    url = 'https://ws.audioscrobbler.com/2.0/'

    # Add API key and format to the payload
    payload['api_key'] = '9e1aed6b5e20d2cae8eab8ada94a9c7a'
    payload['format'] = 'json'

    response = requests.get(url, headers=headers, params=payload)
    return response


responses = []

page = 1
total_pages = 100  # this is just a dummy number so the loop starts

while page <= total_pages:
    payload = {
        'method': 'chart.gettopartists',
        'limit': 500,
        'page': page
    }

    # print some output so we can see the status
    # print("Requesting page {}/{}".format(page, total_pages))
    # clear the output to make things neater
    # clear_output(wait=True)

    # make the API call
    response = lastfm_get(payload)

    # if we get an error, print the response and halt the loop
    if response.status_code != 200:
        print(response.text)
        break

    # extract pagination info
    page = int(response.json()['artists']['@attr']['page'])
    # total_pages = int(response.json()['artists']['@attr']['totalPages'])

    # append response
    responses.append(response)

    # if it's not a cached result, sleep
    if not getattr(response, 'from_cache', False):
        time.sleep(0.25)

    # increment the page number
    page += 1

frames = [pd.DataFrame(r.json()['artists']['artist']) for r in responses]
artists_df = pd.concat(frames)
artists_df = artists_df.drop('image', axis=1)
artists_df = artists_df.drop_duplicates().reset_index(drop=True)


def lookup_tags(artist):
    response = lastfm_get({
        'method': 'artist.getTopTags',
        'artist':  artist
    })

    # if there's an error, just return nothing
    if response.status_code != 200:
        return None

    # extract the top three tags and turn them into a string
    tags = [t['name'] for t in response.json()['toptags']['tag'][:3]]
    tags_str = ', '.join(tags)

    # rate limiting
    if not getattr(response, 'from_cache', False):
        time.sleep(0.25)
    return tags_str

tqdm.pandas()
artists_df['tags'] = artists_df['name'].progress_apply(lookup_tags)
