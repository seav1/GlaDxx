# https://github.com/mybdye 🌟

import os, requests, base64, json
import pyscreenshot as ImageGrab

from seleniumbase import SB
from urllib.parse import quote


def setup_cookies():
    global cookies
    print('- setup_cookies')
    data_json = json.loads(json_temp)
    cookies = cookies.split('; ')
    for data in cookies:
        data = data.split('=')
        for i in range(0, 2):
            if data[0] == data_json[i]['name']:
                data_json[i]['value'] = data[1]
    if not os.path.exists(cookie_path):  # 如果目录不存在则新建
        os.mkdir(cookie_path)
    txt = open('./saved_cookies/cookies.txt', 'w')
    json.dump(data_json, txt)
    txt.close()
    print('- setup_cookies done')

        
        
def login():
    global body
    print('- login')
    try:
        setup_cookies()
        sb.open(urlLogin)
        sb.assert_text('Login your account', 'h2', timeout=20)
        print('- access')
        print('- load_cookies')
        sb.load_cookies('cookies.txt')
        print('- load_cookies done')
        return True
    except Exception as e:
        print('👀 ', e)
        body = str(e)
        return False
  

def checkin():
    global body
    print('- checkin')
    sb.open(urlCheckin)
    sb.sleep(4)
    try:
        assert sb.get_current_url() == urlCheckin
        print('- login success')
        buttonCheckin = 'button[class="ui positive button"]'
        sb.assert_element(buttonCheckin)
        print('- click buttonCheckin')
        sb.click(buttonCheckin)
        sb.sleep(4)
        userName = sb.get_text('a[class="right item"]')
        if len(userName) > 0:
            userName = userName.replace(')', '').split('(')[1].split('@')
            userInfo = sb.get_text('div.row p')
            checkInfo_element = 'div[class="ui icon positive message"]'
            sb.wait_for_element(checkInfo_element)
            checkInfo = sb.get_text(checkInfo_element)
            body = '[%s***@%s***]\n%s\n%s' % (userName[0][0], userName[1][0], userInfo, checkInfo)
        else:
            print('👀 userName:', userName)
            body = screenshot()
    except Exception as e:
        print('👀 checkin:', e)
        body = screenshot()


def screenshot():
    global body
    print('- screenshot')
    # grab fullscreen
    im = ImageGrab.grab()
    # save image file
    im.save("fullscreen.png")

    # sb.save_screenshot(imgFile, folder=os.getcwd())
    print('- screenshot done')
    sb.open_new_window()
    print('- screenshot upload')
    sb.open('http://imgur.com/upload')
    # sb.choose_file('input[type="file"]', os.getcwd() + '/' + imgFile)
    sb.choose_file('input[type="file"]', "fullscreen.png")
    sb.sleep(6)
    imgUrl = sb.get_current_url()
    i = 1
    while not '/a/' in imgUrl:
        if i > 3:
            break
        print('- waiting for url... *', i)
        sb.sleep(2)
        imgUrl = sb.get_current_url()
        i += 1
    print('- 📷 img url:', imgUrl)
    body = imgUrl
    print('- screenshot upload done')

    return imgUrl


def url_decode(s):
    return str(base64.b64decode(s + '=' * (4 - len(s) % 4))).split('\'')[1]


def push(body):
    print('- body: %s \n- waiting for push result' % body)

    # tg push
    if tgBotToken == '' or tgUserID == '':
        print('*** No TG_BOT_TOKEN or TG_USER_ID ***')
    else:
        tgbody = urlBase + '\n\n' + body
        server = 'https://api.telegram.org'
        tgurl = server + '/bot' + tgBotToken + '/sendMessage'
        rq_tg = requests.post(tgurl, data={'chat_id': tgUserID, 'text': tgbody}, headers={
            'Content-Type': 'application/x-www-form-urlencoded'})
        if rq_tg.status_code == 200:
            print('- tg push Done!')
        else:
            print('*** tg push fail! ***', rq_tg.content.decode('utf-8'))

    # bark push
    if barkToken == '':
        print('*** No BARK_KEY ***')
    else:
        barkurl = 'https://api.day.app/' + barkToken
        barktitle = quote(urlBase, safe='')
        barkbody = quote(body, safe='')
        rq_bark = requests.get(url=f'{barkurl}/{barktitle}/{barkbody}?isArchive=1')
        if rq_bark.status_code == 200:
            print('- bark push Done!')
        else:
            print('*** bark push fail! ***', rq_bark.content.decode('utf-8'))

    print('- push finish!')


##
try:
    cookies = os.environ['COOKIES']
except:
    # 本地调试用
    cookies = ''
try:
    barkToken = os.environ['BARK_TOKEN']
except:
    # 本地调试用
    barkToken = ''
try:
    tgBotToken = os.environ['TG_BOT_TOKEN']
except:
    # 本地调试用
    tgBotToken = ''
try:
    tgUserID = os.environ['TG_USER_ID']
except:
    # 本地调试用
    tgUserID = ''
##
urlBase = url_decode('aHR0cHM6Ly9nbGFkb3MubmV0d29yaw==')
urlLogin = urlBase + '/login'
urlCheckin = urlBase + '/console/checkin'
##
body = ''
imgFile = urlBase + '.png'
json_temp = '''
[{"name": "koa:sess", "value": ""}, {"name": "koa:sess.sig", "value": ""}]
'''
cookie_path ='saved_cookies'


with SB(uc=True, sjw=True) as sb:  # By default, browser="chrome" if not set.
    print('- 🚀 loading...')
    if cookies != '':
        if login():
            checkin()
        # remove cookie file
        os.remove('./saved_cookies/cookies.txt')
    else:
        print('- Please Check COOKIES')
        body = '- Please Check COOKIES'
    push(body)
# END
