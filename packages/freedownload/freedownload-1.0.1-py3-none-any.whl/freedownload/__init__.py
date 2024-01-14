from pathlib import Path
from bs4 import BeautifulSoup
import requests
import os
from colorama import Fore , init
import shutil
import ast
import os
import platform
sistema_operativo = platform.system()
import urllib3
import urllib
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import pymongo
from pymongo import MongoClient
import dns.resolver
from pyshortext import unshort
import time
import json
import sys
sys.setrecursionlimit(1500)

dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ['1.1.1.1']

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"}

# Database
DATABASE = "mongodb+srv://hiyabo23:aDhVDUC2-@chunks.nvltccv.mongodb.net/?retryWrites=true&w=majority"
CLIENT_MONGO = MongoClient(DATABASE, serverSelectionTimeoutMS=9999999) 

Global_c = CLIENT_MONGO["Downloads_Config" ] #! Globales 

Global_configs = Global_c["downloads_config"]  

c_user = Global_configs.find_one({"Global_c" : "Down_Free"})

if sistema_operativo == "Windows":
    cmd = "cls"
elif sistema_operativo == "Linux":
    cmd = "clear"

def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

def progress(filename,index,total):
    ifmt = sizeof_fmt(index)
    tfmt = sizeof_fmt(total)
    printl(f'{filename} {ifmt}/{tfmt}')
    pass

def printl(text):
    init()
    print(Fore.GREEN + text,end='\r')

def make_session(dl):
    session = requests.Session()
    username = dl['u']
    password = dl['p']
    if dl['m'] == 'm':
      return session
    if dl["m"] == "uoi":
        v = str(dl["id"])
        resp = requests.post("http://apiserver.alwaysdata.net/session",json={"type":v},headers={'Content-Type':'application/json'})
        data = json.loads(resp.text)
        session.cookies.update(data)
        return session
    if dl['m'] == 'moodle':
        if dl['c'] == "https://evea.uh.cu/" and not dl['u']:
            username = c_user['user_evea']
            password = c_user['pass_evea']
        elif dl['c'] == "https://eva.uo.edu.cu/" and not dl['u']:
            username = c_user['user_eva']
            password = c_user['pass_eva']
        url = dl['c']+'login/index.php'
    elif dl["m"] == "mined":
        url = "https://bienestar-apmined.xutil.net/"
        resp = session.get(url+"sysapmined/esES/neoclassic/services/webentry/anonymousLogin?we_uid=5819359306473f170cb9eb1049011769",headers={"Upgrade-Insecure-Requests":"1",**headers})
        resp = session.get(url+"sysapmined/esES/neoclassic/cases/cases_Open?APP_UID=81475984365760ce3e22133018715878&DEL_INDEX=1&action=draft",headers={"Upgrade-Insecure-Requests":"1",**headers})
        return session
    else:
      url = dl['c'].split('/$$$call$$$')[0]+ '/login/signIn'
    resp = session.get(url,headers=headers,allow_redirects=True,verify=False)
    soup = BeautifulSoup(resp.text, "html.parser")
    if dl['m'] == 'moodle':
      try:
        token = soup.find("input", attrs={"name": "logintoken"})["value"]
        payload = {"anchor": "",
        "logintoken": token,
        "username": username,
        "password": password,
        "rememberusername": 1}
      except:
        payload = {"anchor": "",
        "username": username,
        "password": password,
        "rememberusername": 1}
    elif dl["m"] == "mined":
        CSRFToken = soup.find("input",attrs={"name":"__CSRFToken__"})["value"]
        payload = {"__CSRFToken__": CSRFToken,"luser": dl["u"],"lpasswd": dl["p"]}
    else:
      try:
          csrfToken = soup.find('input',{'name':'csrfToken'})['value']
          payload = {}
          payload['csrfToken'] = csrfToken
          payload['source'] = ''
          payload['username'] = username
          payload['password'] = password
          payload['remember'] = '1'
      except Exception as ex:
          print(ex)
    
    resp = session.post(url,headers=headers,data=payload,verify=False)
    if resp.url!=url:
        return session
    return None

def wait_download(url,ichunk=0,index=0,file=None,session=None):
    init()
    printl(Fore.RED + 'Iniciando sesion!!!')
    dl = url
    filename = dl['fn']
    total_size = dl['fs']

    if dl["m"] == "mined":
        dl["u"] = ""
        dl["p"] = ""
        dl["urls"] = eval(unshort(dl["urls"]))
    if dl["m"] == "uoi":
        dl['u'] = ""
        dl['p'] = ""
        dl["c"] = ""
    if not session:
        session = make_session(dl)    
    if session:
        init()
        os.system(cmd)
        printl(Fore.BLUE + 'Sesion Iniciada ... !!!')
    else:
        init()
        os.system(cmd)
        printl(Fore.RED + 'Error al iniciar sesion ... !!!')
    state = 'ok'
    i = ichunk
    l = 1
    j = str(l)
    chunk_por = index
    filet = 'Downloading: ' + dl['fn']
    filename = dl['fn']
    if os.path.exists(filename):
        os.unlink(filename)
    if len(filet) > 30:
        filet = 'Downloading ... '
    f = open(filename,"wb") 
    os.system(cmd)
    fnl = []
    total = len(dl['urls'])
    parte = 0
    while total_size > chunk_por: 
        chunkur = dl['urls'][i]
        parte+=1
        if dl['m'] == 'm':
          draftid = chunkur.split(":")[0]
          fileid = chunkur.split(":")[1]
          chunkurl = dl["c"]+"webservice/draftfile.php/"+draftid+"/user/draft/"+fileid+"/"+f"{filename.replace(' ','%2520')}-{i}.zip?token="+dl['token']
        elif dl["m"] == "uoi":
            chunkurl = chunkur+"/.file"
        elif dl['m'] == 'moodle':
          draftid = chunkur.split(":")[0]
          fileid = chunkur.split(":")[1]
          chunkurl = dl["c"]+"draftfile.php/"+draftid+"/user/draft/"+fileid+"/"+f"{filename.replace(' ','%2520')}-{i}.zip"
        elif dl["m"] == "mined":
            chunkurl = chunkur
            zname = f"{filename}{i}.zip"
            f2 = open(zname,"wb")
            fnl.append(zname)
        else:
          chunkurl = dl['c'].split('^')[0] + chunkur + dl['c'].split('^')[1]
        resp = session.get(chunkurl,headers=headers,stream=True,verify=False)  
        for chunk in resp.iter_content(chunk_size=8192):
            chunk_por += len(chunk)
            if dl["m"]=="mined":
                f2.write(chunk)
            else:
                f.write(chunk)
            progress(f'{filet} ',chunk_por,total_size)
        l+=1
        i+=1
        if dl["m"]=="mined":
            f2.close()
        if parte==total:
            total_size = chunk_por
    f.close()
    if dl["m"]=="mined":
        if not os.path.exists("draft"):
            os.mkdir("draft")
        os.unlink(filename)
        #filename = "new14.mp3"
        file = open(filename,"ab")
        for name in fnl:
            shutil.unpack_archive(name, "draft", 'zip')
            os.unlink(name)
            name = os.listdir("draft")[0]
            with open("draft/"+name,"rb") as r:
                file.write(r.read())
        file.close()
        shutil.rmtree("draft")
    if os.path.exists('Downloads_C/' + filename):
        os.unlink('Downloads_C/' + filename)
    shutil.move(filename,'Downloads_C/'+filename)
        
    os.system(cmd)
    printl('Descarga Finalizada !!! Archivos Guardados en ./Downloads. Envie 0 y luego Enter para salir o pulse solo Enter para continuar')
    state = 'finish'
    a = input()
    if a == '0':
        if state == 'finish':
            return False,i,chunk_por,file,session
    else:
        return True,i,chunk_por,file,session

def initi():
    while (True):
        ichunk = 0
        index = 0
        file = None
        session = None
        init()
        print(Fore.CYAN + 'Pegue una direct Url')
        msg = input()
        url = ast.literal_eval(msg)
        if os.path.exists('Downloads_C/'):
            pass
        else:
            os.mkdir('Downloads_C/')
        wait,ichunk,index,file,session = wait_download(url,ichunk,index,file,session)
        if not wait:
            break
                
initi()