import tweepy, re, random, requests
from config import Config
from books import Reference, Bible

# Twitter Keys and Tokens
CONSUMER_KEY = Config.CONSUMER_KEY
CONSUMER_SECRET = Config.CONSUMER_SECRET
ACCESS_KEY = Config.ACCESS_KEY
ACCESS_SECRET = Config.ACCESS_SECRET

# Bible Keys and URL
API_KEY = Config.BIBLE_API
API_URL = Config.API_URL

# Authentication

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

# Random Proverb

rand_book = random.choice(Bible.Books)
print(rand_book)
chapter = random.randrange(0, int(Reference.Book_Dict[rand_book]))
print(chapter)
verse = random.randrange(0, 119)
print(verse)

# chapter = random.randrange(1, len(CHAPTER_LENGTHS))

verse = '%s %s:%s' % (rand_book, chapter, verse)
verse2 = 'John 3:16 - 17'

params = {
        'q': verse,
        'indent-poetry': False,
        'include-headings': False,
        'include-footnotes': False,
        'include-verse-numbers': False,
        'include-short-copyright': False,
        'include-passage-references': False
    }

headers = {
    'Authorization': 'Token %s' % API_KEY
}

data = requests.get(API_URL, params=params, headers=headers).json()
text = re.sub('\s+', ' ', data['passages'][0]).strip()

canon = data['canonical']

update = f'"{text}"\n – {canon}'
# update = '%s – %s' % (text, data['canonical'])

# user = api.get_user('CN_Mbhalati')
# timeline = api.user_timeline('CN_Mbhalati')


print(update)

#api.update_status(update)





print('Success!')
