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
	#print x,y
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

def plot_colors2(hist, centroids):
	# initialize the bar chart representing the relative frequency
	# of each of the colors
	#print x,y
	bar = np.zeros((100, 300, 3), dtype = "uint8")
	startX = 0
 
	# loop over the percentage of each cluster and the color of
	# each cluster
	for (percent, color) in zip(hist, centroids):
		# plot the relative percentage of each cluster
		endX = startX + (percent * 300)
		cv2.rectangle(bar, (int(startX), 0), (int(endX), 100),
			color.astype("uint8").tolist(), -1)
		startX = endX
	
	# return the bar chart
	return bar

def saveCorpusColors(i,hist,centers):
	barimg = plot_colors2(hist,centers)
   	bx,by,bc = barimg.shape
   	outfilename = str(i) + "_colors.png"
   	cv2.imwrite(outfilename,barimg)

def get_colors(hist, centroids):
	# loop over the percentage of each cluster and the color of
	# each cluster
	colors = list()
	for (percent, color) in zip(hist, centroids):
		rgb = color.astype("uint8").tolist()
		#print rgb
		colors.append(rgb)

	return colors

def load_corpus_images(dirname,outdirname):
	'''load corpus from Directory'''
	colormemory = list()
	print dirname

	for i,filename in enumerate(glob.glob("./" + str(dirname) + "/*")):
		ori_img = cv2.imread(filename)
		fname = filename.split("/")
		#ori_img = cv2.cvtColor(ori_img,cv2.COLOR_BGR2RGB)
		ox,oy,oc = ori_img.shape
		#decrease processing time
		img = cv2.resize(ori_img, (0,0), fx=0.1, fy=0.1) 
		img = img.reshape((img.shape[0]*img.shape[1],3))
		#img = cv2.sort(img, cv2.SORT_ASCENDING)
		clusters = KMeans(n_clusters = 3)# random.randrange(3, 8, 1))
		clusters.fit(img)
		hist = centroid_histogram(clusters)
		colors = get_colors(hist,clusters.cluster_centers_)
		saveCorpusColors("./" + outdirname + "/" + fname[2],hist,clusters.cluster_centers_)
		colormemory.append(colors)
		#print colors

	saveColorMemory(dirname,outdirname,colormemory)
	loadColorMemory(dirname,outdirname)
	return colormemory

def saveColorMemory(dirname,outdirname,colormem):
#lines = fo.readlines()
	fo = open("./" + outdirname + "/" +dirname +".dat","w")

	for color in colormem:
		fo.write(str(color) + "\n") 

	fo.close()
	print "Memory Saved"

def loadColorMemory(dirname,outdirname):
	fo = open("./" + outdirname + "/" +dirname +".dat","r")
	lines = fo.readlines()
	for l in lines:
		l = eval(l)
		print l
	print "Memory Loaded"
	return lines



#Keys
IMGUR_CLIENT_ID = '01daaea9535f153'
IMGUR_CLIENT_SECRET = '7ee8195bc0a759716a3aefd0898312c0d24c3e95'
T_CONSUMER_KEY = 'AOP8tSfCUVGnPvP5XhuQ0YM4a'#keep the quotes, replace this with your consumer key
T_CONSUMER_SECRET = 'AnoqbRjZq66qaf3ko5QnbCVFswizY5TRYnBwVqfP3MoMqe5no2'#keep the quotes, replace this with your consumer secret key
T_ACCESS_KEY = '4870995742-SbLewErytfpuulbm42NCYJUW92ldWarsLwgkZB0'#keep the quotes, replace this with your access token
T_ACCESS_SECRET = 'QJmMsF5Qf4WjCqi4MNN7tIDhA8mPF555oTImQW19b6ivu'#keep the quotes, replace this with your access token secret
NUM_CLUSTERS = 5
CHOOSE = 1 #How many items to grab
SUBREDDITS = ["imaginarylandscapes","Art","Creatures_of_earth","Pics","earthporn","EyeCandy","watchmen","LandscapePhotography","GraphicDesign","cinemagraphs","aww"]
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
					"Insidious","Irksome", "Jocular", "Beautiful", "Mendacious", "Redolent", "Zealous"]
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

load_corpus_images("corpus","loadedCorpusData")

exit()


run = True
while (run):
	images = imgur.get_subreddit_gallery(SUBREDDITS[random.randrange(0,len(SUBREDDITS))], sort='time', window='top', limit=CHOOSE)
	names = list()
	links = list()
	for i,im in enumerate(images):
		name = "image" + str(i)
		names.append(name)
		links.append(im.link)
		im.download("./downloads",name)

	for i,n in enumerate(names):
		for filename in glob.glob("./downloads/*"):
	   		if str(n) in str(filename):
	   			ori_img = cv2.imread(filename)
	   			#img = cv2.cvtColor(ori_img,cv2.COLOR_BGR2HSV)
	   			ox,oy,oc = ori_img.shape
	   			#decrease processing time
	   			img = cv2.resize(ori_img, (0,0), fx=0.1, fy=0.1) 
	   			img = img.reshape((img.shape[0]*img.shape[1],3))
	   			#img = cv2.sort(img, cv2.SORT_ASCENDING)
	   			clusters = KMeans(n_clusters = 3)#random.randrange(3, 8, 1))
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
	   			message = str(links[i]) + " " + MESSAGES_FOUR[random.randrange(0,len(MESSAGES_FOUR))] + " #UmbalaBot"
	   			api.update_with_media(outfilename,message)


	for filename in glob.glob("*"):
		#Clean up Directory
		if str(".jpg") in str(filename.lower()):
				os.remove(filename)
		if str(".png") in str(filename.lower()):
				os.remove(filename)
		if str(".gif") in str(filename.lower()):
				os.remove(filename)

	time.sleep(300)#Every Five Minutes



 

 

