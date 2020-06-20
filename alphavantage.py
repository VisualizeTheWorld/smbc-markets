# Query alphavantage for stock market info
import random

import requests

# Returns a tuple of (human-readable name, human-readable description)
def get_stock_move(av_key):
    hr_name = 'IBM'
    mr_name = 'IBM'

    change = query_change(mr_name,av_key)
    if change is None: return None

    return (hr_name,'moves %f points' % change)

# Returns change as percent
def query_change(symbol,av_key):
    r = requests.get('https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=%s&apikey=%s' % (symbol,av_key))
 
    if r.status_code != 200: return [] # TODO : should be an exception

    movement = r.json()
    movement = movement['Global Quote']['10. change percent']
    movement = float(movement.replace('%',''))
    return movement
