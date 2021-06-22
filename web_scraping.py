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


phone_brand_list = []
specification_list = []
old_price_list = []
new_price_list = []
rating_list = []
url = "https://jumia.com.ng/smartphones/"
# #### FOR JUMIA

for i in range(50):
  print(url)
  my_response = requests.get(url, headers)
  fresh_soup = BeautifulSoup(my_response.content, features = "lxml")

  first_search = fresh_soup.find("div", attrs = {"class": "-paxs row _no-g _4cl-3cm-shs"})
  # .find_all returns a list and it finds all the children tag in a parent tag
  second_search = first_search.find_all("article", attrs = {"class": "prd _fb col c-prd"})
  # print(second_search[0].prettify())
  
  for phone_box in second_search:
    # print(phone_box.prettify())
    imp_details = phone_box.find("a")
    # print(imp_details.prettify())
    # print("\n")
    try:
      brand_of_phone = imp_details["data-brand"]
      phone_brand_list.append(brand_of_phone)
      # print("\n")
    except:
      pass

    try:
      spec_of_phone = imp_details["data-name"]
      # print(spec_of_phone)
      # print("\n")
      specification_list.append(spec_of_phone)
    except:
      pass
    

    try:
      old_price_container = imp_details.find("div", attrs = {"class": "old"})
      if old_price_container == False:
        pass
      else:
        try:
          old_price = (old_price_container.text).split(" ")[1].split(",").split(" -")
        except:
          old_price = (old_price_container.text).split(" ")[1].split(",")
        try: 
          old_price_compact = old_price[0]+old_price[1]
        except:
          old_price_compact = old_price[0]

        old_price_list.append(old_price_compact)
    except:
      old_price_list.append(0)


    current_price = imp_details.find("div", attrs = {"class": "prc"})
    try:
      price = (current_price.text).split(" ")[1].split(",").split(" -")
    except:
      price = (current_price.text).split(" ")[1].split(",")
    # print(price)
    try:
      price_compact = price[0]+price[1]
    except:
      price_compact = price[0]
    new_price_list.append(price_compact)
    
     
    try:
      rating_4_phone = imp_details.find("div", attrs = {"class": "stars _s"})
      rating = (rating_4_phone.text).split(" ")[0]
      # print(rating)
      rating_list.append(rating)
    except:
      rating_list.append(0.00)
  
  if i == 49:
    break

  navi_div = fresh_soup.find("div", attrs={"class": "pg-w -ptm -pbxl"})
  next_page = navi_div.find_all("a")

  for index, a_tag in enumerate(next_page):
    if index == len(next_page) - 2:
      needed_link = a_tag["href"] ###href is the key to a value (i.e the link) and href is an attribute in the tag as all attributes are keys to thier values.
    else:
      pass

  url = "https://www.jumia.com.ng/" + needed_link

  # print(phone_brand_list[-1])
  # print("\n")
  
  for phone_brand, specif, old_price, new_price, rate in zip(phone_brand_list, specification_list, old_price_list, new_price_list, rating_list):
    write_smartphones(phone_brand, specif, int(old_price), int(new_price), float(rate))
  

  





 