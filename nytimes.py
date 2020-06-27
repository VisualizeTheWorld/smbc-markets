# Fetches headlines from the NY Times
import datetime
import random

import requests

# Returns number of seconds since given timestamp
def time_since_stamp(ts_iso8601):
    then_ts = datetime.datetime.fromisoformat(ts_iso8601)
    now_ts = datetime.datetime.now(datetime.timezone.utc)
    return (now_ts - then_ts).total_seconds()

# Returns a random NY Times headline
def get_headline(nyt_key):
    section = random.choice(['business','climate','new york','science','sports','u.s.','world'])
    headlines = get_recent_headlines('all',section,nyt_key)

    if len(headlines) > 0: return random.choice(headlines)
    return None

def get_recent_headlines(source,section,key):
    r = requests.get("https://api.nytimes.com/svc/news/v3/content/%s/%s.json?api-key=%s" % (source, section, key))

    if r.status_code != 200: return [] # TODO : should be an exception

    headlines = r.json()
    headlines = parse_headlines(headlines)
    
    return headlines

def parse_headlines(headlines,max_age=60*60*24):
    headlines = headlines['results']
    good_headlines = []

    for headline in headlines:
        # Remove old headlines
        time_since = time_since_stamp(headline['published_date'])
        if time_since > max_age: continue

        # Clean up headline
        headline = headline['title'].strip()

        # Remove headlines that probably won't fit
        if is_bad_headline(headline): continue

        # Done
        good_headlines.append(headline)

    return good_headlines

# Some heuristics to find headlines that won't make grammatical sense in this
# sort of generator.
bad_phrases = ['here\'s what you need to know',
               'what to know about',
               ':',
               '@',
               ]
bad_prefixes = ['what',
                'when',
                'how',
                ]
def is_bad_headline(headline):
    lc_headline = headline.lower()
    if not len(headline): return True

    # Remove questions
    if headline[-1] == '?': return True

    # Remove bad prefixes
    for prefix in bad_prefixes:
        if lc_headline.startswith(prefix): return True

    # Search for bad phrases
    for phrase in bad_phrases:
        if phrase in lc_headline: return True

    return False

