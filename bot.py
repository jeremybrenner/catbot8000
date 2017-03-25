import tweepy 
import secrets as s
import os
import random
import requests
from io import BytesIO
from PIL import Image
from PIL import ImageChops

# Handle OAuth instance and requests
auth = tweepy.OAuthHandler(s.consumer_key, s.consumer_secret)
auth.set_access_token(s.access_token, s.access_secret)

# Build twitter API instance
api = tweepy.API(auth)

# Method which stores image and fetches random cat picture
def tweet_image(url, username, status_id):

	# Temp file to hold imaage from bot request
	post_temp = 'posted.png'

	# Pic a random cat image from assets
	cat_root_path = "./cats/"
	cat_pic = random.choice([x for x in os.listdir(cat_root_path)])
	cat_path = cat_root_path + cat_pic


	# Build request object
	request = requests.get(url, stream=True)
	if request.status_code == 200:

		# Read data from request and return PIL.Image.Image object 
		i = Image.open(BytesIO(request.content))
		i.save(post_temp)

		catify(post_temp,cat_path)

		api.update_with_media('result.png', status='@{0}'.format(username), in_reply_to_status_id=status_id)

	else: print("Unable to download image from bot request")

def catify(post_img,cat_img):

	print('\n=== Attempting to merge images ===')
	print('* Post => ' + post_img)
	print('* Cat => ' + cat_img)
	print('\n')

	# Open the post picture, and cat image
	post = Image.open(post_img)
	cat = Image.open(cat_img)


	post_size = post.size
	cat_size = cat.size

	# Resize and convert cat image to match post
	cat = cat.convert('RGBA')
	cat = cat.resize(post_size)

	pic_data = cat.load()

	width, height = cat.size

	# Make cat picture into a transparent layer and save it
	for y in xrange(height):
		for x in xrange(width):
			pic_data[x, y] = (pic_data[x, y][0], pic_data[x, y][1], pic_data[x, y][2], 100)

	cat.save('rdy_cat.png', 'PNG')

	transp_cat = Image.open('rdy_cat.png')

	# Create a composite which overlays cat onto original post
	post.paste(transp_cat, (0,0), transp_cat)
	post.save('result.png')

# Create class that inherits from tweepy StreamListener
class BotStreamer(tweepy.StreamListener):

	# Listen for on_status event
	def on_status(self, status):

		username = status.user.screen_name
		status_id = status.id

		print('\n === Incoming post to @catpicbot8000 ===')
		print('* Username => ' + username)
		print('* Status =>')
		print(status)
		print('\n')

		# Extract media from tweets without having to parse all text 
		if 'media' in status.entities:
			for image in status.entities['media']:
				tweet_image(image['media_url'], username, status_id)

# Listen to @catbot8000 for events
myStreamListener = BotStreamer()
stream = tweepy.Stream(auth, myStreamListener)
stream.filter(track=['@catpicbot8000'])



# 		img = Image.open('./cats/cat1.jpg')
# img2 = Image.open('./cats/cat2.jpg')

# img = img.convert("RGBA")
# img = img.resize(img2.size)

# pixdata = img.load()

# width, height = img2.size

# for y in xrange(height):
#     for x in xrange(width):
#         pixdata[x, y] = (pixdata[x, y][0], pixdata[x, y][1], pixdata[x, y][2], 50)

# img.save("test.png", "PNG")
