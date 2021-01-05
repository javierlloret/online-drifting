from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
import random

#Point of departure
initial_sites = ["http://www.publico.es"  , "http://www.youtube.com"  ]

#Path to geckodriver
browser = webdriver.Firefox(executable_path='./geckodriver')
#browser = webdriver.Chrome(executable_path='./chromedriver')

#If allow_internal_links = True, we will navigate randomly without trying to reach a different website
allow_internal_links = False

#If True we will take snapshots of the websites that we have visited
saving_images = True

#If True the browser will scroll down
scroll = True

#If True we will take a second snapshot of the website
save_two_images_when_scrolling = True

#Set to True for debugging
verbose = False

#internal variables
sites = initial_sites
allow_temp_internal_links = allow_internal_links
tempsites = []
counter=1
url = ""
stem = ""
counter_locked = 0

#Infinite loop
while True:
	if verbose:
		print "sites len="+str(len(sites))+"\n"

	#Pick random destination from the current list of urls
	randomIndex = random.randint(0,len(sites)-1)
	url = sites[randomIndex]
	print url

	#get the domain of the url
	index = url.find("//")
	if index != -1: #// found
		stem =  url[(index+2):len(url)]

	indexWWW = stem.find("www.")
	if indexWWW != -1: #www. found
		stem =  stem[indexWWW+4:len(stem)]
		indexDots = stem.find(".")
		if indexDots > -1: #remove the .whatever
			stem =  stem[0:indexDots]
	else: #www. Not found
		indexDots = stem.find(".")
		if indexDots > -1:
			stem =  stem[0:indexDots]
			indexDots = stem.find(".")
			if indexDots > -1:
				stem =  stem[0:indexDots]

	if verbose:
		print "domain="+stem
	try:
		#go there
		browser.get(url)

		#take snapshop
		if saving_images:
			time.sleep(0.5)
			browser.save_screenshot("screenshots/i_have_been_places_"+str(counter)+".jpg")
			counter=counter+1

		#scroll down
		if scroll:
			scheight = 9.9
			time.sleep(0.5)
			while scheight > .1:
				browser.execute_script("window.scrollTo(0, document.body.scrollHeight/%s);" % scheight)
				scheight -= .1

			#second snapshop?
			if saving_images and save_two_images_when_scrolling:
				browser.save_screenshot("screenshots/i_have_been_places_"+str(counter)+".jpg")
				counter=counter+1

		#store all the links
		elems = browser.find_elements_by_xpath("//a[@href]")

		#store the links in the list of potential destinations
		if verbose:
			print "elems len="+str(len(elems))
		if len(elems) > 0:
			tempsites = []
			for elem in elems:
				href = elem.get_attribute("href")
				if href.find("http") > -1:
					if allow_internal_links:
						tempsites.append(href)
					elif allow_temp_internal_links:
						tempsites.append(href)
					elif stem not in href and "icloud" not in href and "mailto:" not in href and url not in href:
						tempsites.append(href)

		allow_temp_internal_links=False
		if verbose:
			print "tempsites len="+str(len(tempsites))
		if len(tempsites) > 0:
			sites = []
			sites = tempsites
			counter_locked=0
		else:
			counter_locked = counter_locked+1
			if counter_locked > 1:
				sites=initial_sites
				counter_locked=0
				if allow_internal_links == False:
					allow_temp_internal_links = True
					print "internal search"
	except Exception as e:
		print "Exception!"
		print type(e)
		print e

#close the web browser
browser.close()
