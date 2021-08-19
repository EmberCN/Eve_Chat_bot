from flask import Flask, request
import re, random, requests
from config import Config
from twilio.twiml.messaging_response import MessagingResponse
from books import Reference, Bible, Chapters, Psalm_Chapters, Random_Gos

app = Flask(__name__)
# Bible Keys and URL
API_KEY = Config.BIBLE_API
API_URL = Config.API_URL

@app.route('/chat_bot', methods=['POST'])
def bot():
    resp = MessagingResponse()
    msg = resp.message()
    incoming_msg = request.values.get('Body', '').lower()
    responded = False

    # Introduces Eve and gives instructions
    if 'hi' in incoming_msg:
        msg.body('''Hey! My name is Eve!

I'm a bible bot and here's how you can interact with me:
- Reply *'random proverb'* to get a random scripture from *Proverbs.*
- Reply *'random psalm'* to get a random scripture from  *Psalms.*
- Reply *'random gospel'* to get a random scripture from one of the *Gospels (Matthew, Mark, Luke, and John).*
- Or just send me a verse and I'll give you the scripture you asked for (e.g. John 3:16 or Jhn 3:16)

- Or Or just say *'hi'* and you'll get this list of options again!

So. How can I help? 😊''')
        responded = True
    
    #Returns random Proverb
    elif 'random' and 'proverb' in incoming_msg:
        chapter = random.randrange(1, len(Chapters.Lengths))
        verse = random.randint(1, Chapters.Lengths[chapter])
        verse =  "Proverbs %s:%s" % (chapter, verse)

        params = {
        'q': verse,
        'indent-poetry': True,
        'include-headings': False,
        'include-footnotes': False,
        'include-verse-numbers': False,
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

        msg.body(scripture)
        responded = True 

    #Returns random Psalm
    elif 'random' and 'psalm' in incoming_msg:
        chapter = random.randrange(1, len(Psalm_Chapters.Lengths))
        verse = random.randint(1, Psalm_Chapters.Lengths[chapter])
        verse =  "Psalm %s:%s" % (chapter, verse)

        params = {
        'q': verse,
        'indent-poetry': True,
        'include-headings': False,
        'include-footnotes': False,
        'include-verse-numbers': False,
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

        msg.body(scripture)
        responded = True 
    
    # Returns Random verse from one of the Gospels  
    elif 'random' and 'gospel' in incoming_msg:
        rand_book = random.choice(Random_Gos.Gospels)
        chapter = random.randrange(0, int(Reference.Book_Dict[rand_book]))
        verse = random.randrange(0, 80)
        verse = '%s %s:%s' % (rand_book, chapter, verse)

        params = {
        'q': verse,
        'indent-poetry': True,
        'include-headings': False,
        'include-footnotes': False,
        'include-verse-numbers': False,
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

        msg.body(scripture)
        responded = True 

    # Returns requested scripture
    else:
        try: 
            verse = incoming_msg
            params = {
            'q': verse,
            'indent-poetry': True,
            'include-headings': False,
            'include-footnotes': False,
            'include-verse-numbers': False,
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

            msg.body(scripture)
            responded = True 
        # Tells user to try again
        except:
            msg.body('''Sorry about that. 
I couldn't get what you were looking for. Go ahead and try again!
And if you're looking for a scripture, just type in the book and verse you want and I'll get it back to you!(e.g. Jeremiah 29:11 or Jer 29:11)''')
   
    responded = True  
    return str(resp)  

if __name__ == '__main__':
    app.run()