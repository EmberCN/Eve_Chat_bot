import tweepy, re, random, requests
from config import Config
from books import Reference, Bible, Chapters, Psalm_Chapters, Random_Gos

# Twitter Keys and Tokens
CONSUMER_KEY = Config.CONSUMER_KEY
CONSUMER_SECRET = Config.CONSUMER_SECRET
ACCESS_KEY = Config.ACCESS_KEY
ACCESS_SECRET = Config.ACCESS_SECRET

# Bible Keys and URL
API_KEY = Config.BIBLE_API
API_URL = Config.API_URL


# Calls Scripture
def call(verse):
    params = {
        'q': verse,
        'indent-poetry': True,
        'include-headings': False,
        'include-footnotes': False,
        'include-verse-numbers': True,
        'include-short-copyright': False,
        'include-passage-references': False
    }

    headers = {
        'Authorization': 'Token %s' % (API_KEY)
    }
    data = requests.get(API_URL, params=params, headers=headers).json()
    text = re.sub('\s+', ' ', data['passages'][0]).strip()

    canon = data['canonical']
    scripture = update = f'"{text}"\n – {canon}'
    # Rendering below
    text = re.sub('\s+', ' ', data['passages'][0]).strip()
    render = '"%s" – %s' % (text, data['canonical'])
    print(scripture)

# Random Scripture generator
def pick(script):
    rand_book = random.choice(Bible.Books)
    print(rand_book)
    chapter = random.randrange(0, int(Reference.Book_Dict[rand_book]))
    print(chapter)
    verse = random.randrange(0, 119)
    print(verse)
    verse = '%s %s:%s' % (rand_book, chapter, verse)
    return call(verse)

#return random proverb
def Rand_Prov():
    chapter = random.randrange(1, len(Chapters.Lengths))
    verse = random.randint(1, Chapters.Lengths[chapter])
    verse =  "Proverbs %s:%s" % (chapter, verse)
    return call(verse)

#return random psalm
def Rand_Psa():
    chapter = random.randrange(1, len(Psalm_Chapters.Lengths))
    verse = random.randint(1, Psalm_Chapters.Lengths[chapter])
    verse =  "Psalm %s:%s" % (chapter, verse)
    return call(verse)

# Returns Random verse from one of the Gospels
def Rand_Gos():
        rand_book = random.choice(Random_Gos.Gospels)
        chapter = random.randrange(0, int(Reference.Book_Dict[rand_book]))
        verse = random.randrange(0, 80)
        verse = '%s %s:%s' % (rand_book, chapter, verse)
        return call(verse)

input('')
print('Hey! What scripture do you want?')
scripture = input(': ')
scripture = scripture.lower()
if 'random' and 'proverb' in scripture:
    Rand_Prov()
elif 'random' and 'psalm' in scripture:
    Rand_Psa()
elif 'random' and 'gospel' in scripture:
    Rand_Gos()
else:
    try: 
        call(scripture)
    except:
        print("Sorry about that. I couldn't get what you were looking for, go ahead and try again.")
        print("Just give me the scripture you're looking for and I'll find it!")

