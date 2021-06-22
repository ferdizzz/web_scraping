import requests
from bs4 import BeautifulSoup
import csv
from jumia_db import *

##To crawl in disguise
headers = requests.utils.default_headers()

headers.update(
  {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
  }
)


## FOR NAIRALAND
# The desired web application
url = "https://nairaland.com"

my_response = requests.get(url, headers) ##.get() helps assess the url passed to it as arguments
# print(my_response.status_code) 

fresh_soup = BeautifulSoup(my_response.content, features ="lxml")
# print(fresh_soup.prettify())

first_search = fresh_soup.find("td", attrs={"class": "featured w"})
# print(first_search.prettify())

second_search = first_search.find_all("a")
# find_all() returns a list
# print(second_search[:5])
# pretty_second = [print(entry.text)  for entry in second_search]
mined_data = []

for index, entry in enumerate(second_search):
  index += 1
  news_headline = entry.text
  # print(entry.prettify())
  needed_link = entry["href"]

  # To navigate to the new url
  new_response = requests.get(needed_link, headers) 
  new_soup = BeautifulSoup(new_response.content, features = "lxml")
  # print(new_soup.prettify())
  
  desired_tag = new_soup.find("p", attrs= {"class": "bold"})
  # print(desired_tag.prettify())

  number_of_views = str(desired_tag).split("</a>")[-1].split("</p>")[0].strip(" () ").split(" ")[0]
  # print(number_of_views)

  mined_data.append([index, news_headline, number_of_views])

# print(mined_data)


new_file = open("/Users/drizzytom/Documents/PHYTHON/Data_Sci/nairaland_news_views.csv", mode="w", encoding="utf-8", newline="")

pen = csv.writer(new_file)

pen.writerow(["S/N", "News Headline", "Number of Views"])

# To write smartly
pen.writerows(mined_data)

new_file.close()