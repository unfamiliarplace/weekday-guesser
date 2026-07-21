from datetime import date
from pathlib import Path
import random
import calendar

# Constants
CONFIG = {
    'DISTANCE': 3000,
    'ALLOW_BC':     0,
    'ALLOW_FUTURE': 0
}

# Weekdays are 0-based in Python
NUMS = '0123456'

# Or they can type some of the full name
NAMES = [
    'MONDAY',
    'TUESDAY',
    'WEDNESDAY',
    'THURSDAY',
    'FRIDAY',
    'SATURDAY',
    'SUNDAY',
]

# Single-letter abbreviations
SHORTS = 'MTWRFSD'

# Functions

def read_config():
    with open(Path(__file__).parent.resolve() / 'config.ini', 'r') as f:
       data = []
       for line in f.readlines():
           line = line.strip().split(';')[0]
           if line:
               data.append(int(line))

    CONFIG['DISTANCE'], CONFIG['ALLOW_BC'], CONFIG['ALLOW_FUTURE'] = data

def random_date() -> date:
    this_year = date.today().year
    
    min_year = this_year - CONFIG['DISTANCE']
    if min_year < 0 and not CONFIG['ALLOW_BC']:
        min_year = 0
    
    max_year = this_year + CONFIG['DISTANCE']
    if max_year > this_year and not CONFIG['ALLOW_FUTURE']:
        max_year = this_year

    y = random.randint(min_year, max_year)
    m = random.randint(1, 12)
    
    if m in [1, 3, 5, 7, 8, 10, 12]:
        d = random.randint(1, 31)
    elif m in [4, 6, 9, 11]:
        d = random.randint(1, 30)
    elif calendar.isleap(y):
        d = random.randint(1, 29)
    else:
        d = random.randint(1, 28)    

    return date(y, m, d)

def format_date(d: date) -> str:
    
    # No automatic zero-stripping cross-platform in datetime :/
    yr = d.strftime('%Y').lstrip('0')
    mo = d.strftime('%B')
    dy = d.strftime('%d').lstrip('0')

    era = ' BC' if d.year < 0 else ''

    return f'{mo} {dy}, {yr}{era}'

def is_valid_guess(s: str) -> bool:
    if len(s) < 1:
        return False
    
    if s.isdigit():
        return 0 <= int(s) <= 6

    else:
        return any(s.startswith(c) for c in SHORTS)

def parse_guess(s: str) -> str:
    """Just makes it easier to guess."""    

    if s.isdigit():
        pool = NUMS
    elif len(s) == 1:
        pool = SHORTS
    else:
        pool = NAMES
   
    for (i, name) in enumerate(pool):
        if name.startswith(s):
            return i

def play() -> bool:
    print()

    d = random_date()
    ans = d.weekday()

    print(format_date(d))
    guess = input('Guess: ').strip().upper()
    while not is_valid_guess(guess):
        print('Invalid guess...')
        guess = input('Guess: ').strip().upper()

    if parse_guess(guess) == ans:
        print('Yes!')
    else:
        print(f'No. It was a {NAMES[ans].title()}')
    
    print()

def run():
    read_config()

    print('Guess the weekday of a given date!')
    print('You can type in a full day, a partial day, or a single letter. (Thursday = R, Sunday = D)')

    choice = ''
    while choice.strip().upper() != 'Q':
        play()
        choice = input('Enter to play again or Q to quit: ')

if __name__ == '__main__':
    run()
