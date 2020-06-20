# The main program
import alphavantage, nytimes

def get_api_keys():
    keys = {}
    with open('api-keys.txt','r') as f:
        keys = [line.split(' ') for line in f.read().split('\n')]
    keys = { l[0] : l[1] for l in keys if len(l) == 2 }
    return keys

def construct_headline(api_keys, n_retries=3):
    for i in range(n_retries):
        headline = nytimes.get_headline(api_keys['nytimes'])
        if headline is not None: break
    if headline is None: return None
    
    for i in range(n_retries):
        stonk = alphavantage.get_stock_move(api_keys['alphavantage'])
        if stonk is not None: break
    if stonk is None: return None
    stonk, sentiment = stonk

    return '%s %s After %s' % (stonk, sentiment, headline)

if __name__ == '__main__':
    api_keys = get_api_keys()
    headline = construct_headline(api_keys,n_retries=3)
    print(headline)
