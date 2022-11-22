###### CODE TO AUTHENTICATE THE TWITTER ACCOUNT #####
#auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET, callback = 'oob')
#auth.secure = True
#auth_url = auth.get_authorization_url()

#print ('Please authorize: ' + auth_url)

#verifier = input('PIN: ').strip()

#auth.get_access_token(verifier)

#print ("ACCESS_KEY = " + auth.access_token)
#print ("ACCESS_SECRET = " +  auth.access_token_secret)

import tweepy
from dotenv import load_dotenv
import os
import time
import random

#--------------------------------------------------------------------------------------------------
#LOADING KEYS AND AUTHENTICATION IN THE API

load_dotenv('.env') #Loading the enviroment where the keys are

CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
USER_KEY = os.getenv('USER_KEY')
USER_SECRET = os.getenv('USER_SECRET')

client = tweepy.Client( #Authenticate in the API 2.0
    consumer_key=CONSUMER_KEY, consumer_secret= CONSUMER_SECRET,
    access_token=USER_KEY, access_token_secret=USER_SECRET
)

auth = tweepy.OAuth1UserHandler( #Authenticate in the API 1.1
   CONSUMER_KEY, CONSUMER_SECRET,
   USER_KEY, USER_SECRET
)
api = tweepy.API(auth)

#--------------------------------------------------------------------------------------------------

bot_id = 1591113204331061248
start_id = 1

while True: 
    response = client.get_users_mentions(bot_id, expansions = ['in_reply_to_user_id', 'referenced_tweets.id'], \
               since_id = start_id, user_auth=True)
    if response.data != None:
        for tweet in response.data:
            ids = open('ids.txt').read().splitlines()
            try:
                if ('@HowManyBot expose' in tweet.text) and (str(tweet.id) not in ids): #Works as a function to replay to mentions
                    target_user = client.get_user(id = tweet.in_reply_to_user_id, user_auth=True)
                    
                    user_ID = target_user.data.id
                    user_name = target_user.data.username

                    print("The tweet is: " + tweet.text)

                    user_info = api.get_user(user_id = user_ID) 
                    user_likes = user_info.favourites_count #Get total likes of user given

                    rand_num = random.randint(0, user_likes)

                    message = ".@" + user_name + " es tan follawaifus que le ha dado me gusta a " \
                              + str(rand_num) + " monas chinas!"
                    print("The answer is: " + message)

                    client.create_tweet(
                        in_reply_to_tweet_id = tweet.id,
                        text = message
                    )

                    #Save the ID in ids.txt
                    f = open("ids.txt", 'a')
                    f.write(str(tweet.id) + "\n")
                    f.close()
                    
                    print("Se ha enviado la respuesta y guardado la ID.\n")
                
                    start_id = tweet.id

#--------------------------------------------------------------------------------------------------
                
                if ('@HowManyBot download' in tweet.text) and (str(tweet.id) not in ids): #Works as a function to download videos when mentioned
                    target_tweet = api.get_status(id=response.includes['tweets'][0].id, 
                                   tweet_mode='extended')
                    
                    target_media = target_tweet.extended_entities['media'][0]

                    media_type = target_media['video_info']['variants'][1]['content_type'] #Index [1] stores the mp4 video

                    if media_type == 'video/mp4': #Only download videos

                        print("The tweet is: " + tweet.text)

                        media_url = target_media['video_info']['variants'][1]['url']
                        print("The video link is: " + media_url)

                        message = "Aquí tienes el enlace! Solo tienes que pulsarlo y" \
                                  " hacer clic derecho, luego pulsar la opción 'Guardar video como...'.\n" \
                                  + media_url

                        client.create_tweet(
                            in_reply_to_tweet_id = tweet.id,
                            text = message
                        )
                        
                        #Save the ID in ids.txt
                        f = open("ids.txt", 'a')
                        f.write(str(tweet.id) + "\n")
                        f.close()
                        
                        print("Se ha enviado el link del video y guardado la ID.\n")
                        
                        start_id = tweet.id
            
#--------------------------------------------------------------------------------------------------

                else:   #Just in case the tweet don't match any command
                    message = "No te he entendido. ¿Seguro que estás usando el comando correcto?"

                    client.create_tweet(
                        in_reply_to_tweet_id = tweet.id,
                        text = message
                        )
                        
                    #Save the ID in ids.txt
                    f = open("ids.txt", 'a')
                    f.write(str(tweet.id) + "\n")
                    f.close()

            except:
                pass

    time.sleep(10)