# import the necessary packages
import tweepy, time, sys, os
import pyimgur
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
import argparse
import random
import glob
import cv2

def centroid_histogram(clt):
	# grab the number of different clusters and create a histogram
	# based on the number of pixels assigned to each cluster
	numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
	(hist, _) = np.histogram(clt.labels_, bins = numLabels)
 
	# normalize the histogram, such that it sums to one
	hist = hist.astype("float")
	hist /= hist.sum()
 
	# return the histogram
	return hist

def plot_colors(hist, centroids,x,y):
	# initialize the bar chart representing the relative frequency
	# of each of the colors
	print x,y
	bar = np.zeros((y, x, 3), dtype = "uint8")
	startX = 0
 
	# loop over the percentage of each cluster and the color of
	# each cluster
	for (percent, color) in zip(hist, centroids):
		# plot the relative percentage of each cluster
		endX = startX + (percent * x)
		cv2.rectangle(bar, (int(startX), 0), (int(endX), y),
			color.astype("uint8").tolist(), -1)
		startX = endX
	
	# return the bar chart
	return bar

def get_colors(hist, centroids):
	# loop over the percentage of each cluster and the color of
	# each cluster
	colors = list()
	for (percent, color) in zip(hist, centroids):
		rgb = color.astype("uint8").tolist()
		print rgb
		colors.append(rgb)

	return colors

#Keys
NUM_CLUSTERS = 5
CHOOSE = 3 #How many items to grab
SUBREDDITS = ["Creatures_of_earth","Pics","earthporn","EyeCandy","watchmen","GraphicDesign"]
MESSAGES_ONE = ["I like this picture, " ,\
				"I love this image, ",\
				"This pic is beautiful, ",\
				"This is my favorite, ",\
				"This is Exquisite, "]
MESSAGES_TWO = ["The details are ",\
				"It's Quite ",\
				"Somewhat ",\
				"Refreshing and "]
MESSAGES_TWO_ADJ = ["Adroit","Adamant","Arcadian","Baleful","Comely","Contumacious", "Didactic",\
					"Efficacious","Effulgent","Equanimous","Fastidious","Fecund","Hubristic",\
					"Insidious","Irksome", "Jocular", "Limpid", "Mendacious", "Redolent", "Zealous"]
MESSAGES_THREE = [", let me tell you what my #favoritecolors in it are",\
					", I'll post my #favoritecolors next",\
					", do you want to know my #favoritecolors?"]

MESSAGES_FOUR = ["And these are my #favoritecolors.", "This makes a nice palatte. #favoritecolors",\
				 "I like this. #favoritecolors", "Very Quaint! #favoritecolors"]
#Twitter Auth
auth = tweepy.OAuthHandler(T_CONSUMER_KEY, T_CONSUMER_SECRET)
auth.set_access_token(T_ACCESS_KEY, T_ACCESS_SECRET)
api = tweepy.API(auth)

#Imgur
imgur = pyimgur.Imgur(IMGUR_CLIENT_ID)
#images = imgur.get_gallery(section='hot', sort='viral', window='day', show_viral=True, limit=CHOOSE)
#images = imgur.get_subreddit_gallery(SUBREDDITS[random.randrange(0,len(SUBREDDITS))], sort='time', window='top', limit=CHOOSE)

run = True
while (run):
	images = imgur.get_subreddit_gallery(SUBREDDITS[random.randrange(0,len(SUBREDDITS))], sort='time', window='top', limit=CHOOSE)
	names = list()
	links = list()
	for i,im in enumerate(images):
		name = "image" + str(i)
		names.append(name)
		links.append(im.link)
		im.download("./",name)

	for i,n in enumerate(names):
		for filename in glob.glob("*"):
	   		if str(n) in str(filename):
	   			ori_img = cv2.imread(filename)
	   			img = cv2.cvtColor(ori_img,cv2.COLOR_BGR2HSV)
	   			ox,oy,oc = ori_img.shape
	   			#decrease processing time
	   			img = cv2.resize(ori_img, (0,0), fx=0.1, fy=0.1) 
	   			img = img.reshape((img.shape[0]*img.shape[1],3))
	   			#img = cv2.sort(img, cv2.SORT_ASCENDING)
	   			clusters = KMeans(n_clusters = random.randrange(3, 8, 1))
	   			clusters.fit(img)
	   			hist = centroid_histogram(clusters)
	   			colors = get_colors(hist,clusters.cluster_centers_)
	   			barimg = plot_colors(hist,clusters.cluster_centers_,ox,oy)
	   			bx,by,bc = barimg.shape
	   			outfilename = "colors.png"
	   			cv2.imwrite(outfilename,barimg)
	   			#Update Status with color info
	   			#api.update_status(str(n) + " from imgur has " + str(NUM_CLUSTERS) + " main colors: " + str(colors))
	   			message = MESSAGES_ONE[random.randrange(0,len(MESSAGES_ONE))] +\
	   					  MESSAGES_TWO[random.randrange(0,len(MESSAGES_TWO))] +\
	   					  MESSAGES_TWO_ADJ[random.randrange(0,len(MESSAGES_TWO_ADJ))] +\
	   					  MESSAGES_THREE[random.randrange(0,len(MESSAGES_THREE))]
	   			api.update_with_media(filename,message)
	   			message = str(links[i]) + MESSAGES_FOUR[random.randrange(0,len(MESSAGES_FOUR))] + " #UmbalaBot"
	   			api.update_with_media(outfilename,message)


	for filename in glob.glob("*"):
		#Clean up Directory
		if str(".jpg") in str(filename.lower()):
				os.remove(filename)
		if str(".png") in str(filename.lower()):
				os.remove(filename)
		if str(".gif") in str(filename.lower()):
				os.remove(filename)



 

 

