# import the necessary packages
import tweepy, time, sys
import pyimgur
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
import argparse
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

def plot_colors(hist, centroids):
	# initialize the bar chart representing the relative frequency
	# of each of the colors
	bar = np.zeros((50, 300, 3), dtype = "uint8")
	startX = 0
 
	# loop over the percentage of each cluster and the color of
	# each cluster
	for (percent, color) in zip(hist, centroids):
		# plot the relative percentage of each cluster
		endX = startX + (percent * 300)
		cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
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

#Twitter Auth
auth = tweepy.OAuthHandler(T_CONSUMER_KEY, T_CONSUMER_SECRET)
auth.set_access_token(T_ACCESS_KEY, T_ACCESS_SECRET)
api = tweepy.API(auth)

#Imgur
imgur = pyimgur.Imgur(IMGUR_CLIENT_ID)
#image = imgur.get_image('S1jmapR')
#print image.title # Cat Ying & Yang
#print image.link# http://imgur.com/S1jmapR.jpg
#image.download()
images = imgur.get_gallery(section='hot', sort='viral', window='day', show_viral=True, limit=1)
#images = imgur.get_subreddit_gallery('CineShots', sort='time', window='top', limit=1)

names = list()
for i,im in enumerate(images):
	name = "image" + str(i)
	names.append(name)
	#im.download("./","image"+str(i))

for n in names:
	for filename in glob.glob("*"):
   		if str(n) in str(filename):
   			img = cv2.imread(filename)
   			img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
   			img = img.reshape((img.shape[0]*img.shape[1],3))
   			clusters = KMeans(n_clusters = NUM_CLUSTERS)
   			clusters.fit(img)
   			hist = centroid_histogram(clusters)
   			colors = get_colors(hist,clusters.cluster_centers_)
   			barimg = plot_colors(hist,clusters.cluster_centers_)
   			cv2.imwrite("colors.png",barimg)
   			#Update Status with color info
   			api.update_status(str(filename) + " " + str(colors))


 

 

