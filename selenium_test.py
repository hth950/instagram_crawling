import http
import io
import os
import sys
import time
import urllib.request
from datetime import datetime
from urllib.parse import quote

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')
# 크롤링할 url 주소
tags = "여자코디"
tag_name = quote("여자코디")
print(tag_name)
url = "https://www.instagram.com/explore/tags/"+tags

date = datetime.today().strftime("%Y.%m.%d")

DRIVER_DIR = '/path/to/chromedriver'
# 크롬 드라이버를 이용해 임의로 크롬 브라우저를 실행시켜 조작한다.
driver = webdriver.Chrome("C://chromedriver1/chromedriver.exe")
# 암묵적으로 웹 자원을 (최대) 5초 기다리기DRIVER_DIR)
driver.implicitly_wait(5)
# 크롬 브라우저가 실행되며 해당 url로 이동한다.
driver.get(url)
# 총 게시물 수를 클래스 이름으로 찾기
elem = driver.find_element_by_tag_name("body")
# alt 속성의 값을 담을 빈 리스트 선언
alt_list = []
url_list = []
folder_name = date + tags
if not os.path.isdir("D:\photos/" + folder_name + "/"):
    os.mkdir("D:\photos/" + folder_name + "/")
# 페이지 스크롤을 위해 임시 변수 선언
pagedowns = 1
# 스크롤을 20번 진행한다.
while pagedowns < 20:
        elem.send_keys(Keys.PAGE_DOWN)
        # 페이지 스크롤 타이밍을 맞추기 위해 sleep
        time.sleep(1)
        img = driver.find_elements_by_xpath('//img[@*]')
        img_url = driver.find_elements_by_xpath("//a[@*]")
        # 위에서 선언한 alt_list 리스트에 alt 속성의 값을 중복을 방지하며 할당한다.
        for i in img:
            if not i.get_attribute('srcset') in alt_list:
                alt_list.append(i.get_attribute('srcset'))
        for j in img_url:
            if not j.get_attribute('href') in url_list:
                url_list.append(j.get_attribute('href'))
        pagedowns += 1
del(alt_list[0])
del(url_list[0])

#print (alt_list[0])
#print (url_list[0])
#print("1")

#처음부터 제거하면 배열이 앞으로 설정되어 동작 안함, 뒤에서부터 지움
for k in url_list[::-1]:
    if not k.find('/p/') > -1:
        url_list.remove(k)

def localHttpRequest(file_name , from_url):
    params = urllib.parse.urlencode(
        {'file_name' : file_name, 'from_url' : from_url, 'tag' : '["여자코디"]'})
    headers = {"Content-type": "application/x-www-form-urlencoded",
               "Accept": "application/json"}
    conn = http.client.HTTPConnection("210.89.190.201")
    conn.request("POST", "/v/image", params, headers)
    response = conn.getresponse()
    print(response.status, response.reason)

for i in range(len(alt_list)):
    photo = alt_list[i].split(',')[3]
    result = photo.replace("480w", "")
    download = "D:\photos/" + folder_name + "/"
    name = url_list[i].split('/')[4]
    urllib.request.urlretrieve(result , download+name+"_"+str(i)+".jpg")
    #localHttpRequest(name+"_"+str(i)+".jpg", url_list[i])
# 드라이버를 종료한다.
