# The main program
import json
import random
import twitter
import alphavantage, nytimes

def get_api_keys():
    keys = {}
    with open('api-keys.json','r') as f:
        keys = json.load(f)
    return keys

def get_hashtags():
    hashtags = {}
    with open('hashtags.json','r') as f:
        hashtags = json.load(f)
    return hashtags

def construct_tweet(api_keys, hashtag_list, n_retries=3, max_tweet_len=280):
    # Headline
    for i in range(n_retries):
        headline = nytimes.get_headline(api_keys['nytimes'])
        if headline is not None: break
    if headline is None: return None
    
    # Get stock, movement, and stock types
    for i in range(n_retries):
        stonk = alphavantage.get_stock_move(api_keys['alphavantage'])
        if stonk is not None: break
    if stonk is None: return None
    stonk, sentiment, hashtag_groups = stonk

    # Construct base tweet
    tweet = '%s %s After %s' % (stonk, sentiment, headline)
    tweet_len = len(tweet)
    if tweet_len > max_tweet_len:
        tweet = tweet[:max_tweet_len - 3] + '...'
        return tweet

    # Hashtag the tweet for better discoverability
    # TODO : we can pack these in tighter
    hashtags = []
    hashtag_options = []
    for hg in hashtag_groups:
        hashtag_options += hashtag_list[hg]
    while True:
        hashtag = random.choice(hashtag_options)
        if hashtag in hashtags: continue
        hashtag = ' #%s' % hashtag
        if tweet_len + len(hashtag) > max_tweet_len: break
        hashtags.append(hashtag)
        tweet_len += len(hashtag)

    # Last tag pushed it over the edge
    hashtags = hashtags[:-1]

    # Construct final tweet
    return '%s%s' % (tweet,''.join(hashtags))

def send_tweet(tweet,twitter_keys):
    oauth = twitter.OAuth(twitter_keys['auth'],twitter_keys['auth-secret'],
            twitter_keys['consumer'],twitter_keys['consumer-secret'])
    T = twitter.Twitter(auth=oauth)

    T.statuses.update(status=tweet)

if __name__ == '__main__':
    # Get 
    api_keys = get_api_keys()
    hashtag_list = get_hashtags()

    # Build tweet
    tweet = construct_tweet(api_keys,hashtag_list,n_retries=3)

    # Send tweet
    send_tweet(tweet,api_keys['twitter'])
