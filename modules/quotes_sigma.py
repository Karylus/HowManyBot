import random

def get_quote():
    with open('./data/sigmaQuotes.txt', 'r') as f:
        read = f.read()
        array = read.split('\n')
        quote = random.choice(array)
    
    return quote

print(get_quote())
