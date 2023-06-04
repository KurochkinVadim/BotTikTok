import os
import telebot
import re
import wget
import random
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

prox = {}
headersUseragents = list()
proxiesList = list()
driver = None
bot = telebot.TeleBot('Bot Token')
count = 0


@bot.message_handler(commands=['start'])
def start(message):
    mess = f'Hello, <b>{message.from_user.first_name} {message.from_user.last_name}</b>'
    bot.send_message(message.chat.id, mess, parse_mode='html')


@bot.message_handler(content_types=['text'])
def get_user_text(message):
    if re.match(r'https?://\w{,2}.?tiktok.com', message.text) is not None:
        try:
            print('\n' + message.from_user.first_name)
            link = re.findall(r'\bhttps?://.*[(tiktok|douyin)]\S+', message.text)[0]
            link = link.split("?")[0]
            print('\n' + link)
            # useragent
            options = webdriver.FirefoxOptions()
            options.set_preference("general.useragent.override", random.choice(useragentList()))
            # proxy
            proxy = random.choice(getProxy())
            firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
            firefox_capabilities["marionette"] = True
            firefox_capabilities["proxy"] = {
                "proxyType": "MANUAL",
                "httpProxy": proxy
            }
            global driver
            driver = webdriver.Firefox(
                executable_path='C:\\Users\\Vadim\\PycharmProjects\\telega\\Driver\\geckodriver.exe',
                options=options, proxy=proxy
            )
            driver.get(link)
            time.sleep(3)
            element = driver.find_element(by=By.XPATH,
                                          value="//div[@class='tiktok-1h63bmc-DivBasicPlayerWrapper e1yey0rl2']/video[1]").get_attribute("src")
            print('\n' + element)
            wget.download(element, 'D:\\downloading\\savedVideo.mp4')
            doc = open('D:\\downloading\\savedVideo.mp4', 'rb')
            bot.send_document(message.chat.id, doc)
            doc.close()
            os.remove('D:\\downloading\\savedVideo.mp4')
        except Exception as ex:
            print(ex)
            bot.send_message(message.chat.id, f'Что-то пошло не так', parse_mode='html')
        finally:
            driver.close()
            driver.quit()
    else:
        bot.send_message(message.chat.id, f'Error', parse_mode='html')


@bot.message_handler(content_types=['sticker'])
def get_user_sticker(message):
    bot.send_message(message.chat.id, message)


def useragentList():
    global headersUseragents
    headersUseragents.append(
        'Some UsrAgent')
    return (headersUseragents)


def getProxy():
    global proxiesList
    r = requests.get('http://foxtools.ru/Proxy?al=True&am=True&ah=True&ahs=True&http=True&https=False')
    soup = BeautifulSoup(r.text, 'lxml')
    line = soup.find('table', id='theProxyList').find('tbody').find_all('tr')
    for tr in line:
        td = tr.find_all('td')
        ip = td[1].text
        port = td[2].text
        proxiesList.append(ip + ':' + port)
        if len(proxiesList) == 20:
            break
    return proxiesList


bot.polling(none_stop=True)
