import json
import requests
from bs4 import BeautifulSoup
import re
import selenium
import selenium.webdriver
from selenium.webdriver.common.by import By
import time
f = open("yahoo-news.json","w")



#reference from :https://stackoverflow.com/questions/48850974/selenium-scroll-to-end-of-page-in-dynamically-loading-webpage
#scroll to the bottom of the website
def scroll_down():
    count = 0
    """A method for scrolling the page."""

    # Get scroll height.
    last_height = driver.execute_script("return document.documentElement.scrollHeight")

    while True:
        count += 1

        # Scroll down to the bottom.
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

        # Wait to load the page.
        time.sleep(2)

        # Calculate new scroll height and compare with last scroll height.
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        #print(new_height)
        #print(last_height)

        if count >= 11:

            break

        last_height = new_height

total = []
dic = {}
l = []
c = 0
driver = selenium.webdriver.Chrome("./chromedriver");
driver.get("https://tw.news.yahoo.com/entertainment");

#load all object first
scroll_down()
#driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight)")

#Collect url for all news first
#
#The five bis news
element = driver.find_element_by_xpath("//*[@id='Col1-1-Hero-Proxy']/div/ul/li/img")
alt = element.get_attribute("alt")
l.append(alt)
print(alt)
print("==")

for i in range (1,3):
    #print(i)
    element = driver.find_elements_by_xpath("//*[@id='Col1-2-CategoryWrapper-Proxy']/div/div[%d]/ul[1]/li/img"% i)
    for image in element:
        alt = image.get_attribute("alt")
        l.append(alt)
        print(alt)
print("===")
for i in range (1,3):
    element = driver.find_element_by_xpath("//*[@id='Col1-3-CategoryWrapper-Proxy']/div/div[%d]/ul[1]/li/img"% i)
    alt = element.get_attribute("alt")
    l.append(alt)
    print(alt)

print("====")


c = 5;

#Other news
for i in range (1,198):
    try:
        element = driver.find_element_by_xpath("//*[@id='YDC-Stream']/ul/li[%d]/div/div/div[2]/h3/a"% i)
        alt = element.get_attribute("href")
        m= re.search('https://tw.news.yahoo.com/*', alt)
        if(m != None):
            l.append(alt)
            print(alt)
            c += 1
    except:
        continue


print("total time")
print(c)


#close driver 
driver.close()
driver.quit()

#Get each url and access web
for i in range(0,len(l)):
    url = l[i]
    content = ''
    r = requests.get(l[i])
    if r.status_code == requests.codes.ok:
        soup = BeautifulSoup(r.text, 'html.parser')
        #Get title (h1)
        title = soup.find("h1").text.strip()
        print("title" , title)

        ts = soup.findAll("p")
        #print("content")

        #Get content 
        for t in ts:
            content += t.text   #append in the same string
            #print(t.text)


            #Use re to find if is hyper link to other news.
            #if find , it reach the bottom of the news
            
            if (re.search("href*",str(t)) != None): #P.S. regular expression in python have some bug
                break                               #Can't use *herf* .
            if(re.search("class=*",str(t)) != None):
                break
            #print(t.find('p').text())

        
        
        #try if no image file
        #can be two type of url ( src) and (data-src)
        #Use two try and except to figure it out
        try:
            t = soup.find("div", {"class":"caas-img-container"})
            tmp = t.find('img')
            try:
                print("image url" , tmp['data-src'])
                im = tmp['data-src']
                dic = {'title':title, 'url':url, 'img_src':im, 'content':content}   #write in the dic
                total.append(dic)   #add dic to list
            except:
                try:
                    print("image url" , tmp['src'])
                    im = tmp['src']
                    dic = {'title':title, 'url':url, 'img_src':im, 'content':content}
                    total.append(dic)
                except:         #can't find neither src nor data-src
                    print("None")
                    dic = {'title':title, 'url':url, 'img_src':'', 'content':content}
                    total.append(dic)
                    continue
        except:             #Can't find img object
            print("None")
            dic = {'title':title, 'url':url, 'img_src':'', 'content':content}
            total.append(dic)
            continue


print('final')
print(total)
print(len(total))
js = json.dumps(total, indent=4)    #transfer list of dict to json
f.write(js)         #write to output.json file 
f.close()           #close file 





            






