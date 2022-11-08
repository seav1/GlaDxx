# https://github.com/mybdye 🌟


import os, requests, base64, json
from seleniumbase import SB


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
        body = e
        return False
  

def checkin():
    global body
    print('- checkin')
    sb.open(urlCheckin)
    checkIn = 'button[class="ui positive button"]'
    sb.assert_element(checkIn)
    print('- click checkin')
    sb.click(checkIn)
    sb.sleep(4)
    userInfo = sb.get_text('div.row p')
    #print('userInfo:', userInfo)
    checkInfo = sb.get_text('div[class="ui icon positive message"]')
    #print('checkInfo:', checkInfo)
    body = userInfo + '\n' + checkInfo

def screenshot():
    global body
    print('- screenshot')
    sb.save_screenshot(imgFile, folder=os.getcwd())
    print('- screenshot done')
    sb.open_new_window()
    print('- screenshot upload')
    sb.open('http://imgur.com/upload')
    sb.choose_file('input[type="file"]', os.getcwd() + '/' + imgFile)
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
    # bark push
    if barkToken == '':
        print('*** No BARK_KEY ***')
    else:
        barkurl = 'https://api.day.app/' + barkToken
        title = urlBase
        rq_bark = requests.get(url=f'{barkurl}/{title}/{body}?isArchive=1')
        if rq_bark.status_code == 200:
            print('- bark push Done!')
        else:
            print('*** bark push fail! ***', rq_bark.content.decode('utf-8'))
    # tg push
    if tgBotToken == '' or tgUserID == '':
        print('*** No TG_BOT_TOKEN or TG_USER_ID ***')
    else:
        body = urlBase + '\n\n' + body
        server = 'https://api.telegram.org'
        tgurl = server + '/bot' + tgBotToken + '/sendMessage'
        rq_tg = requests.post(tgurl, data={'chat_id': tgUserID, 'text': body}, headers={
            'Content-Type': 'application/x-www-form-urlencoded'})
        if rq_tg.status_code == 200:
            print('- tg push Done!')
        else:
            print('*** tg push fail! ***', rq_tg.content.decode('utf-8'))
    print('- finish!')


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
urlBase = url_decode('Z2xhZG9zLnJvY2tz')
urlLogin = urlBase + '/login'
urlCheckin = urlBase + '/console/checkin'
##
body = ''
imgFile = urlBase + '.png'
json_temp = '''
[{"name": "koa:sess", "value": ""}, {"name": "koa:sess.sig", "value": ""}]
'''
cookie_path ='saved_cookies'


with SB(uc=True) as sb:  # By default, browser="chrome" if not set.
    print('- 🚀 loading...')
    if cookies != '':
        try:
            if login():
                checkin()
        except Exception as e:
            print('💥', e)
            try:
                screenshot()
            finally:
                push(e)
        push(body)
    else:
        print('- please check COOKIES')

# END
