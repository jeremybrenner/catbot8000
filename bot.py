import tweepy 
import secrets as s
import os
import random

# Handle OAuth instance and requests
auth = tweepy.OAuthHandler(s.consumer_key, s.consumer_secret)
auth.set_access_token(s.access_token, s.access_secret)

# Build twitter API instance
api = tweepy.API(auth)

# Create class that inherits from tweepy StreamListener
class BotStreamer(tweepy.StreamListener):

	# Listen for on_status event
	def on_status(self, status):
		username = status.user.screen_name
		status_id = status.id

		print(username)
		print(status_id)

		# Extract media from tweets without having to parse all text 
		if 'media' in status.entities:
			for image in status.entities['media']:
				tweet_image(image['media_url'], username, status_id)

		cat_pic = random.choice([x for x in os.listdir("cats")
        	if os.path.isfile(os.path.join("cats", x))])

# Listen to @catbot8000 for events
myStreamListener = BotStreamer()
stream = tweepy.Stream(auth, myStreamListener)
stream.filter(track=['@catbot8000'])

