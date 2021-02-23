
#### To run the project: 

            "python3 main.py"

please note that everytime you run it, you are scraping again from scratch and the index is rebuilt.
You can test with scraping 1000 links, it will take less than a minute to get the final index, you can also change the number of concurrent requests in scraper.py line 78, it will run faster. You can ofcourse test with 10,000 links ro 20,000 this will take 5 minutes to build the index, but the results are more accurate. 


##### The required libraries are:

			NLTK	
			BS4
			Scrapy
			Lxml
			SortedContainers 



##### To Change the scraping limit: 
            
            Line 26 in main.py



##### Please note that the project runs as follows: 
			
			First step is crawling and scraping
			Second step is building the index
			Thirsd Step is running queries. 

