# Query alphavantage for stock market info
import datetime
import random

import requests

# Returns change as percent
def query_change_global_quote(symbol,av_key):
    r = requests.get('https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=%s&apikey=%s' % (symbol,av_key))
 
    if r.status_code != 200: return [] # TODO : should be an exception

    movement = r.json()
    movement = movement['Global Quote']['10. change percent']
    movement = float(movement.replace('%',''))
    return movement

def query_change_cryptocurrency(symbol,av_key):
    r = requests.get('https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&market=USD&symbol=%s&apikey=%s' % (symbol,av_key))
 
    if r.status_code != 200: return [] # TODO : should be an exception

    movement = r.json()
    movement = movement['Time Series (Digital Currency Daily)']
    today = datetime.date.today().isoformat()
    if today not in movement: return None
    movement = movement[today]
    open_price = float(movement['4a. close (USD)'])
    close_price = float(movement['1a. open (USD)'])
    movement = 100.0 * (close_price - open_price) / open_price
    return movement

symbols_index = {'S&P 500' : (query_change_global_quote,'SPY',['generic','stock']),
                 'Dow Jones' : (query_change_global_quote,'DIA',['generic','stock']),
                 }
symbols_meme =  {'Tesla' : (query_change_global_quote,'TSLA',['generic','stock','tesla','tesla']),
           
                 'Bitcoin' : (query_change_cryptocurrency,'BTC',['generic','cryptocurrency','bitcoin']),
                'Ethereum' : (query_change_cryptocurrency,'ETH',['generic','cryptocurrency','ethereum']),
                }
symbols_stock = {'Microsoft' : (query_change_global_quote, 'MSFT',['generic','stock','tech']),
                 'Google'    : (query_change_global_quote, 'GOOG',['generic','stock','tech']),
                 'Amazon'    : (query_change_global_quote, 'AMZN',['generic','stock','tech']),
                 'Facebook'  : (query_change_global_quote, 'FB',['generic','stock','tech']),
                 'Apple'     : (query_change_global_quote, 'AAPL',['generic','stock','tech']),
                 'Netflix'   : (query_change_global_quote, 'NFLX',['generic','stock','tech']),
                }

# Returns a tuple of (human-readable name, human-readable description, groups of hashtags to use)
def get_stock_move(av_key):
    symbols = random.choice([symbols_index,symbols_index,symbols_stock,symbols_meme])
    hr_name = random.choice(list(symbols.keys()))
    query_change,mr_name,tag_groups = symbols[hr_name]
 
    change = query_change(mr_name,av_key)
    if change is None: return None

    return (hr_name,exaggerate_change(change),tag_groups)

def exaggerate_change(change):
    word = 'Holds Steady'
    if change > 5.0:
        word = random.choice(['Soars'])
    elif change > 0.1:
        word = random.choice(['Rises','Ticks Higher','Rallies'])
    elif change < -5.0:
        word = random.choice(['Plummets','Craters','Tanks'])
    elif change < -0.1:
        word = random.choice(['Drops','Falls'])
    return word
