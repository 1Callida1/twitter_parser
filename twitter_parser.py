# Importing libraries
import requests, string, random, json, time
from requests.auth import HTTPProxyAuth
from dotenv import dotenv_values

def get_proxy():
    proxy_config = dotenv_values(".env")
    return HTTPProxyAuth(str(proxy_config['PROXY_LOGIN']), 
    str(proxy_config['PROXY_PASSWORD'])), {'http': f"{proxy_config['PROXY_TYPE']}://{proxy_config['PROXY_IP']}:{proxy_config['PROXY_PORT']}/"}

# HTTP headers required to send the request to Twitter
twitter_session_headers = {
	'Connection': 'keep-alive',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.62',
	'Accept': '*/*',
	'Referer': 'https://google.com/',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br'
}

# Func for returning the basic part of the request headers
# For the formation of a request to obtain information about the tweet
def get_params():
    return {
                "referrer":"tweet","rux_context":"HHwWlsC9zcrS9ZYpAAAA",
                "with_rux_injections":True,
                "includePromotedContent":True,
                "withCommunity":True,
                "withQuickPromoteEligibilityTweetFields":True,
                "withTweetQuoteCount":True,
                "withBirdwatchNotes":False,
                "withSuperFollowsUserFields":True,
                "withBirdwatchPivots":False,
                "withDownvotePerspective":False,
                "withReactionsMetadata":False,
                "withReactionsPerspective":False,
                "withSuperFollowsTweetFields":True,
                "withVoice":True,
                "withV2Timeline":False,
                "__fs_interactive_text":False,
                "__fs_dont_mention_me_view_api_enabled":False
            }

# Recursive function for getting links to commentators profiles
def get_comments(session, post_id, params, count_comments):
    auth, proxy = get_proxy()
    resp = session.get(f'https://twitter.com/i/api/graphql/s2RO46g9Rhw53GX2BEMfiA/TweetDetail?variables={params}', 
    headers=twitter_session_headers, proxies=proxy, auth=auth)

    resp = json.loads(resp.text)
    time.sleep(0.5)
    for comments in resp['data']['threaded_conversation_with_injections']['instructions'][0]['entries']:
        if count_comments == 3:
            break

        if comments['entryId'].startswith('conversationthread'):
            for tweet_results in comments['content']['items'][0]['item']['itemContent']:
                if 'tweet_results' in tweet_results:
                    print(f"Comment {count_comments+1} Link(https://twitter.com/" + 
                    f"{comments['content']['items'][0]['item']['itemContent']['tweet_results']['result']['core']['user_results']['result']['legacy']['screen_name']})")
                    count_comments+=1

        if comments['entryId'].startswith('cursor-showmorethreads-'):
            params = get_params()
            params['focalTweetId']=post_id
            params['cursor']=str(comments['content']['itemContent']['value'])
            get_comments(session, post_id, json.dumps(params), count_comments)

def main():
    session = requests.Session()
    auth, proxy = get_proxy()
    response = session.get('https://twitter.com/', headers=twitter_session_headers, proxies=proxy, auth=auth)

    time.sleep(0.5)

    twitter_session_headers['authorization'] = 'Bearer'
    + ' AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA'
    twitter_session_headers['content-type'] = 'application/x-www-form-urlencoded'

    response = session.post('https://api.twitter.com/1.1/guest/activate.json', 
    headers=twitter_session_headers, proxies=proxy, auth=auth)

    gt = json.loads(response.text)['guest_token']
    twitter_session_headers['x-guest-token'] = gt

    session.cookies['gt'] = gt
    session.cookies['ct0'] = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(32))

    data = json.dumps(
        {
            'userId':'44196397',
            'count':10,
            'withTweetQuoteCount':True,
            'includePromotedContent':True,
            'withQuickPromoteEligibilityTweetFields':True,
            'withSuperFollowsUserFields':True,
            'withBirdwatchPivots':False,
            'withDownvotePerspective':False,
            'withReactionsMetadata':False,
            'withReactionsPerspective':False,
            'withSuperFollowsTweetFields':True,
            'withVoice':True,
            'withV2Timeline':False,
            '__fs_interactive_text':False,
            '__fs_dont_mention_me_view_api_enabled':False
        })

    twitter_session_headers['content-type'] = 'application/json'
    twitter_session_headers['Referer'] = 'https://twitter.com/elonmusk'

    response = session.get(f'https://twitter.com/i/api/graphql/jFdWt4I2nKXWbke-306dfQ/UserTweets?variables={data}',
    headers=twitter_session_headers, proxies=proxy, auth=auth)
    response = json.loads(response.text)

    for i, post in enumerate(response['data']['user']['result']['timeline']['timeline']['instructions'][0]['entries']):
        if not post['entryId'].startswith('TopicsModule') and 'itemContent' in post['content']:
            print(f"Post {i+1} {post['content']['itemContent']['tweet_results']['result']['legacy']['full_text']}")
            data = get_params()
            data['focalTweetId'] = str(post['sortIndex'])
            get_comments(session, str(post['sortIndex']), json.dumps(data), 0)

if __name__ == "__main__": 
    main()