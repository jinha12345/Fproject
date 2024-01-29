#pyinstaller -F -w app.py <- F는 파일하나. w는 윈도우 없이
#pyinstaller app.spec <- packaging code
#5770097152 <- Password

from flask import Flask, render_template, request, redirect, url_for, flash
from password import passgen
from drive import getStockxl, JsonKeySync
import openpyxl
from getfromDB import getby, getMSRP, getSeason, isThere
import copy
import Myfunctions
import webbrowser
import os
from pathlib import Path
import sys
from util import resource_path
import signal
from flask_socketio import SocketIO, emit
import time
from getImage import getImage, check_urls_parallel, a_check_urls_parallel_inner
import asyncio
#import threading

shop_list = ['NC불광', 'MD구리', 'TO분당', 'LT청주', 'MD부평', 'NC청주', 'NC송파', 'MD천안']

login_check = False

base_dir = '.'
if hasattr(sys, '_MEIPASS'):
    base_dir = os.path.join(sys._MEIPASS)

app = Flask(__name__,
        static_folder=os.path.join(base_dir, 'static'),
        template_folder=os.path.join(base_dir, 'templates'))
app.secret_key = 'your_secret_key_here'
socketio = SocketIO(app)

pong = False
something_doing = False

async def check_urls_app(URLs):
    result = await a_check_urls_parallel_inner(URLs)
    print("Valid URLs:", result)
    return result

#Printing base dir for debugging
#print(f'base_dir = {base_dir}')

'''
@app.route("/", methods = [ "GET", "POST"])
def home():
    global login_check
    if not login_check:
        return redirect(url_for('login'))

    model = '입력...'
    cloth_type = ''
    MSRP = '조회시 출력'
    Season = '조회시 출력'
    cloth_type_original = ''
    invalidity = 'false'
    size = {'mbtm' : ['28','30','32','34','36','38','40','계'],
            'wbtm' : ['23/30','24/31','25','26','27','28','29','계'],
            'mtop' : ['85(XS)','90(S)','95(M)','100(L)','105(XL)','X','X','계'],
            'wtop' : ['80(XS)','85(S)','90(M)','95(L)','X','X','X','계'],
            'acc'  : ['70','75','90','95','100/F','X','X','계']}
    
    
    initial_data = {'size' : ["", "", "", "", "", "", "", ""],
                    'NC불광': ["", "", "", "", "", "", "", ""],
                    'MD구리': ["", "", "", "", "", "", "", ""],
                    'TO분당': ["", "", "", "", "", "", "", ""],
                    'LT청주': ["", "", "", "", "", "", "", ""],
                    'MD부평': ["", "", "", "", "", "", "", ""],
                    'NC청주': ["", "", "", "", "", "", "", ""],
                    'NC송파': ["", "", "", "", "", "", "", ""],
                    'MD천안': ["", "", "", "", "", "", "", ""],
                    '계'   : ["", "", "", "", "", "", "", ""]}
    
    ware_initial_data = {'창고' : ["", "", "", "", "", "", "", ""]}
    
    stock_data = copy.deepcopy(initial_data)
    sell_data = copy.deepcopy(initial_data)
    ware_data = copy.deepcopy(ware_initial_data)

    if request.method == 'GET':
        model = request.args.get("model")
        cloth_type = request.args.get("type")
        print(f'Search_Call = model : {model}, type : {cloth_type}')

        if model is not None and cloth_type is not None:
            cloth_type_original = cloth_type
            cloth_type = cloth_type.lower()
            model = model.upper()
            if len(model) == 9:
                model = model[:5] + '-' + model[5:]

            if not isThere(workbook, model, cloth_type):
                invalidity = 'true'
                if model == '':
                    model = '입력...'

                return render_template('home.html', stock_data = stock_data, sell_data = sell_data, MSRP = MSRP, Season = Season, model = model, cloth_type = cloth_type_original, invalidity = invalidity, ware_data = ware_data)
            
            #재고 현황 파악
            for shop in shop_list:
                stock_data[shop] = getby(workbook, shop, model, cloth_type, is_stock = True)
            stock_data['size'] = size[cloth_type]
            stock_data['계'] = [sum(val if isinstance(val, (int, float)) else 0 for val in column) if any(isinstance(val, (int, float)) for val in column) else None for column in zip(*list(stock_data.values())[1:-1])]
            for key, values in stock_data.items():
                stock_data[key] = [value if value is not None else "" for value in values]


            #판매 현황 파악
            for shop in shop_list:
                sell_data[shop] = getby(workbook, shop, model, cloth_type, is_stock = False)
            sell_data['size'] = size[cloth_type]
            sell_data['계'] = [sum(val if isinstance(val, (int, float)) else 0 for val in column) if any(isinstance(val, (int, float)) for val in column) else None for column in zip(*list(sell_data.values())[1:-1])]
            for key, values in sell_data.items():
                sell_data[key] = [value if value is not None else "" for value in values]

            #임시 창고 재고 파악
            ware_data['창고'] = getby(workbook, '창고', model, cloth_type, is_stock = True)
            for key, values in ware_data.items():
                ware_data[key] = [value if value is not None else "" for value in values]

            MSRP = Myfunctions.format_price(getMSRP(workbook, model, cloth_type))
            Season = getSeason(workbook, model, cloth_type)
        else:
            model = '입력...'

    return render_template('home.html', stock_data = stock_data, sell_data = sell_data, MSRP = MSRP, Season = Season, model = model, cloth_type = cloth_type_original, invalidity = invalidity, ware_data = ware_data)
'''

@app.route('/')
def home():
    global something_doing
    global login_check

    if not login_check:
        something_doing = False
        print('something_doing = False : 137')
        return redirect(url_for('login'))

    something_doing = True
    print('something_doing = True : 141')
    model = '입력...'
    cloth_type = 'Mbtm'
    MSRP = '조회시 출력'
    Season = '조회시 출력'
    cloth_type_original = 'Mbtm'
    invalidity = 'false'
    Image_num = 0
    URLs=[]
    size = {'mbtm' : ['28'     ,'30'   ,'32'   ,'34'    ,'36'     ,'38','40','계'],
            'wbtm' : ['23/30'  ,'24/31','25'   ,'26'    ,'27'     ,'28','29','계'],
            'mtop' : ['85(XS)' ,'90(S)','95(M)','100(L)','105(XL)','X' ,'X' ,'계'],
            'wtop' : ['80(XS)' ,'85(S)','90(M)','95(L)' ,'X'      ,'X' ,'X' ,'계'],
            'acc'  : ['70'     ,'75'   ,'90'   ,'95'    ,'100/F'  ,'X' ,'X' ,'계']}
    
    initial_data = {'size' : ["", "", "", "", "", "", "", ""],
                    'NC불광': ["", "", "", "", "", "", "", ""],
                    'MD구리': ["", "", "", "", "", "", "", ""],
                    'TO분당': ["", "", "", "", "", "", "", ""],
                    'LT청주': ["", "", "", "", "", "", "", ""],
                    'MD부평': ["", "", "", "", "", "", "", ""],
                    'NC청주': ["", "", "", "", "", "", "", ""],
                    'NC송파': ["", "", "", "", "", "", "", ""],
                    'MD천안': ["", "", "", "", "", "", "", ""],
                    '계'   : ["", "", "", "", "", "", "", ""]}
    
    ware_initial_data = {'창고' : ["", "", "", "", "", "", "", ""]}
    
    stock_data = copy.deepcopy(initial_data)
    sell_data = copy.deepcopy(initial_data)
    ware_data = copy.deepcopy(ware_initial_data)

    if request.method == 'GET':
        model = request.args.get("model")
        #model = '04511-1907'
        cloth_type = request.args.get("type")
        #cloth_type = 'Mbtm'
        print(f'Search_Call = model : {model}, type : {cloth_type}')

        if model is not None and cloth_type is not None:
            cloth_type_original = cloth_type
            cloth_type = cloth_type.lower()
            model = model.upper()
            if len(model) == 9:
                model = model[:5] + '-' + model[5:]

            if not isThere(workbook, model, cloth_type):
                invalidity = 'true'
                if model == '':
                    model = '입력...'

                something_doing = False
                print('something_doing = False : 192')
                return render_template('home.html', stock_data = stock_data, sell_data = sell_data, MSRP = MSRP, Season = Season, model = model, cloth_type = cloth_type_original, invalidity = invalidity, ware_data = ware_data, URLs = URLs)
            
            
            #재고 현황 파악
            start_time = time.time()
            for shop in shop_list:
                stock_data[shop] = getby(workbook, shop, model, cloth_type, is_stock = True)
            stock_data['size'] = size[cloth_type]
            print(stock_data)
            stock_data['계'] = [sum(val if isinstance(val, (int, float)) else 0 for val in column) if any(isinstance(val, (int, float)) for val in column) else None for column in zip(*list(stock_data.values())[1:-1])]
            for key, values in stock_data.items():
                stock_data[key] = [value if value is not None else "" for value in values]
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"재고현황파악 시간: {elapsed_time:.2f} 초")

            #판매 현황 파악
            start_time = time.time()
            for shop in shop_list:
                sell_data[shop] = getby(workbook, shop, model, cloth_type, is_stock = False)
            sell_data['size'] = size[cloth_type]
            print(sell_data)
            sell_data['계'] = [sum(val if isinstance(val, (int, float)) else 0 for val in column) if any(isinstance(val, (int, float)) for val in column) else None for column in zip(*list(sell_data.values())[1:-1])]
            for key, values in sell_data.items():
                sell_data[key] = [value if value is not None else "" for value in values]
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"판매현황파악 시간: {elapsed_time:.2f} 초")

            #임시 창고 재고 파악
            start_time = time.time()
            ware_data['창고'] = getby(workbook, '창고', model, cloth_type, is_stock = True)
            for key, values in ware_data.items():
                ware_data[key] = [value if value is not None else "" for value in values]
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"임시창고재고파악 시간: {elapsed_time:.2f} 초")

            #이미지 다운로드
            #Image_num = getImage(model, resource_path("static/images"))
            #URL TEST
            start_time = time.time()
            URLs = getImage(model, '', only_URLs=True)
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"getImage() 시간: {elapsed_time:.2f} 초")

            start_time = time.time()
            ###################


            #기존
            #URLs = check_urls_parallel(URLs)



            #새로운것
            URLs = asyncio.run(check_urls_app(URLs))


            ####################
            #URLs = ['https://lsco.scene7.com/is/image/lsco/288331183-front-pdp-lse?fmt=avif&qlt=40&resMode=bisharp&fit=crop,0&op_usm=0.6,0.6,8&wid=155&hei=155']
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"check_url_parallel 시간: {elapsed_time:.2f} 초")

            #ddsk
            start_time = time.time()
            MSRP = Myfunctions.format_price(getMSRP(workbook, model, cloth_type))
            Season = getSeason(workbook, model, cloth_type)
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"MSRP, Season 시간: {elapsed_time:.2f} 초")

        else:
            model = '입력...'
    something_doing = False
    print('something_doing = False : 227')
    return render_template('home.html', stock_data = stock_data, sell_data = sell_data, MSRP = MSRP, Season = Season, model = model, cloth_type = cloth_type_original, invalidity = invalidity, ware_data = ware_data, URLs = URLs)


'''
@app.route('/login', methods = [ "GET", "POST"])
def login():
    global login_check

    id = ""
    pw = ""

    if request.method == 'GET':
        id = request.args.get("login")
        pw = request.args.get("password")
        if id is not None:
            if passgen(id) == pw:
                login_check = True

                maintain_session = True
                return redirect(url_for('home'))
            if id == 'jinha12345':
                login_check = True

                maintain_session = True
                return redirect(url_for('home'))
            else:
                flash('아이디 또는 비밀번호가 일치하지 않습니다.', 'error')
    
    return render_template('login.html')
'''

@app.route('/login', methods = [ "GET", "POST"])
def login():
    global something_doing
    global login_check

    something_doing = True
    print('something_doing = True : 265')
    
    id = ""
    pw = ""

    if request.method == 'GET':
        id = request.args.get("login")
        pw = request.args.get("password")
        if id is not None:
            if passgen(id) == pw:
                login_check = True
                something_doing = False
                print('something_doing = False : 279')
                return redirect(url_for('home'))
            if id == 'jinha12345':
                login_check = True
                something_doing = False
                print('something_doing = False : 286')
                return redirect(url_for('home'))
            else:
                flash('아이디 또는 비밀번호가 일치하지 않습니다.', 'error')
    something_doing = False
    print('something_doing = False : 291')
    return render_template('login.html')

'''
@app.route('/passwordgen', methods = [ "GET", "POST"])
def passwordgen():
    id = ""
    pw = ""
    new_id = ""
    new_pw = ""
    login_check = False

    if request.method == 'GET':
        id = request.args.get("login")
        pw = request.args.get("password")
        new_id = request.args.get("IDID")
        if id is not None:
            if id == 'admin' and pw == 'admin':
                login_check = True
                new_pw = passgen(new_id)

                return render_template('passgen.html', id = id, pw = pw, new_id = new_id, new_pw = new_pw)
    
    return render_template('passgen.html')
'''

@app.route('/passwordgen', methods = [ "GET", "POST"])
def passwordgen():
    global something_doing
    something_doing = True
    id = ""
    pw = ""
    new_id = ""
    new_pw = ""
    login_check = False

    if request.method == 'GET':
        id = request.args.get("login")
        pw = request.args.get("password")
        new_id = request.args.get("IDID")
        if id is not None:
            if id == 'admin' and pw == 'admin':
                login_check = True
                new_pw = passgen(new_id)
                something_doing = False
                print('something_doing = False : 336')
                return render_template('passwordgen.html', id = id, pw = pw, new_id = new_id, new_pw = new_pw)
    something_doing = False
    print('something_doing = False : 339')
    return render_template('passwordgen.html')


@socketio.on('disconnect')
def handle_disconnect():
    global pong
    global something_doing
    pong = False
    print('Client disconnected')

    if something_doing:
        print('But something doing...')
        something_doing = False
        print('something_doing = False : 353')
        return

    # 연결이 끊겼을 때 타이머 시작
    disconnect_timer = 5
    while disconnect_timer > 0 and pong == False:
        if something_doing:
            print('But something doing...')
            something_doing = False
            print('something_doing = False : 362')
            return None
        #print(f"Waiting for pong... {disconnect_timer} seconds left")
        print(f"Waiting for something doing... {disconnect_timer} seconds left")
        disconnect_timer -= 1
        socketio.emit('ping')  # 클라이언트에게 ping 이벤트를 보냄
        time.sleep(1)
    else:
        #if pong == False:
        if not something_doing and pong == False:
            #print('No pong received, considering the client as disconnected')
            print('Doing nothing, considering the client as disconnected')
            os.kill(os.getpid(), signal.SIGINT)
        # 여기에서 페이지 종료에 따른 추가 로직을 수행할 수 있음
    pong = False


@socketio.on('pong')
def handle_pong():
    global pong
    print('Pong received from the client')
    pong = True


if __name__ == '__main__':
    #JsonKey를 drive, temp, appdata 동기화
    #JsonKeySync()

    #이건 실사용시 불러올 workbook
    #getStockxl('DB')
    #workbook = openpyxl.load_workbook(resource_path("DB/DB.xlsm"), data_only=True)

    #이건 디버깅시 불러올 workbook
    workbook = openpyxl.load_workbook(resource_path("DB/DB_fordebugging.xlsx"), data_only=True)

    webbrowser.open('http://127.0.0.1:5000/')
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, use_reloader=False, allow_unsafe_werkzeug=True)
    #dddd
