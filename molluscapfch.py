import csv, requests, json, shutil

#lists to keep track of the book titles and links
book_info_links = []
complete_titles = []


#open the CSV file
with open('names.csv', 'rU') as links_list:

	#ask the csv module to parse the file for us
	books = csv.reader(links_list)
	#this line stuff skips the first line of the CSV
	line=0
	#this for loop pulls all the page item numbers and titles from the CSV
	for row in books:
		if line > 0:
			line =line+1
			url = row[0]
			url = url[40:]
			title = row [2]
			#this if statement tells it to only pull the title if it's not in the titles list already, so there are no repeat titles
			if title not in complete_titles:
			
		
				book_info_links.append(url)
		
				complete_titles.append(title)
		else:
			line+=1
# 		print('done printing pageID')	
# 	print(complete_titles)	

#this uses the page id from our list to then search for the itemID		
for pageID in book_info_links:
#Ask for a search for all the page ID's from the titles -asks for it in json format to be more readable
	#print('requesting page ID...', pageID)
	payload = {'op': 'GetPageMetadata', 'pageid': pageID ,'apikey':'YourAPIKeyHERE', 'format': 'json' }
#The metadata returned by this method includes Title Identifier, Title URL, Full Title, Part Number, 
#Part Name, Publisher Place, Publisher Name, Publication Date, complete author data, Item Identifier, Item URL, 
#Volume, Contributor, and collection data. For more information about these data elements, 
#see the "Data Elements" section of this documentation.
	r = requests.get('http://www.biodiversitylibrary.org/api2/httpquery.ashx?', params = payload)
	
	
	try:
		pageMetadata = json.loads(r.text)
	except:
		print('could not continue', pageID)
		continue
	

	
	ItemID = pageMetadata['Result']['ItemID']
	
	
	
	payload = {'op': 'GetItemPages', 'itemid': ItemID ,'apikey':'YourAPIKeyHERE', 'format': 'json' }
	f = requests.get('http://www.biodiversitylibrary.org/api2/httpquery.ashx?', params = payload)
	
	try:
		itemPages = json.loads(f.text)
	except:
		print('could not continue', ItemID)
		continue
	
# 	print(itemPages)
	
	#itemPages= all the pages of a book contating word 'mullusca'
	# a_page= going page by page within each book
	for a_page in itemPages['Result']:
		#Result= list of dictionaries, each dicationary is a book's metadata 
		#page_type_name= 
		for page_type_name in a_page['PageTypes']:
			#this pulls all the pagetypenames that say illustration
			if 'Illustration' in page_type_name['PageTypeName']:
				#Then it prints out all of the image urls for the illustration pages
				print(a_page['FullSizeImageUrl'])
				#the below code then downloads all of the images to a file on your computer
				response = requests.get(a_page['FullSizeImageUrl'], stream=True)
				with open('images/' + str(a_page['PageID']) + '.jpeg', 'wb') as ill_file:
					shutil.copyfileobj(response.raw, ill_file)
				del response
				
				
			
