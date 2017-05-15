import websocket, codecs, json, threading
from tkinter import *
from time import strftime
import json

socket_url = input(" Socket URL : ")

with codecs.open("setting.json","r",encoding="UTF-8") as f:
    settings = json.loads("".join(f.readlines()).replace("\r","").replace("\n",""))

keys= [ str(x).split(":")[0].split("{")[1][1:-1] for x in settings['numbers']]
numbers= [ str(x).split(":")[1].split("}")[0][2:-1] for x in settings['numbers']]

is_first = True

time = strftime("-%Y%m%d")


def procedure(ws, message):
    command(ws,message)

def whisper(to, m):
    global ws
    ws.send('{"type":"talk","whisper":"'+to+'","value":"'+m+'"}')

def message(m):
    global ws
    ws.send('{"type":"talk","value":"'+m+'"}')

def log(type, m):
    with codecs.open(type+time+".txt","a",encoding="UTF-8") as f:
        f.write(strftime("[%Y.%m.%d %H:%M:%S]")+" "+m+"\n")
    
def command(ws,message):
    global is_first
    if is_first == True:
        with codecs.open("output"+time+".txt","a",encoding="UTF-8") as f:
            f.write(" #### Daemon Started (time : %s)####\n" % strftime("%Y%m%d-%H%M%S"))
        with codecs.open("chat"+time+".txt","a",encoding="UTF-8") as f:
            f.write(" #### Daemon Started (time : %s)####\n" % strftime("%Y%m%d-%H%M%S"))
        with codecs.open("whisper"+time+".txt","a",encoding="UTF-8") as f:
            f.write(" #### Daemon Started (time : %s)####\n" % strftime("%Y%m%d-%H%M%S"))
        is_first = False
        
        ws.send('{"type":"talk","whisper":"이은학","value":"=== Report Daemon Started ==="}')
        pass
    else:
        jsonstring = json.loads(message)
        if "from" in jsonstring.keys():
            print(" Whisper from %s : %s"% (jsonstring['from'],jsonstring['value']))
            threading.Thread(target=log, args=("whisper"," Whisper from %s : %s"% (jsonstring['from'],jsonstring['value']) ) ).start()
            cmd = jsonstring['value'].split(" ")

            nickname = jsonstring['from'].replace(" ","")
            
            if cmd[0] == "!commands":
                whisper(nickname," 안녕하세요 끄투 신고봇입니다. 아래는 명령어 목록입니다.")
                whisper(nickname," !report [신고번호] [고유번호 or 닉네임(띄어쓰기없음)] [자세한설명] / 유저를 신고하는 기능입니다.")
                whisper(nickname," !number / 신고번호를 조회합니다.")
                whisper(nickname," !info / 끄투봇의 정보를 봅니다.")
                
            elif cmd[0] == "!report":
                arg={};
                if len(cmd) < 4:
                    whisper(nickname, " 잘못된 명령어 사용입니다. ")
                    whisper(nickname, " !report [신고번호] [고유번호 or 닉네임(띄어쓰기없음)] [자세한설명]")
                else:
                    arg['num']=cmd[1]; arg['person']=cmd[2:]; arg['reason'] = cmd[3:]
                    whisper(nickname," 준비중입니다.")
                
            elif cmd[0] == "!number":
                for n in range(len(keys)):
                    whisper(nickname, keys[n]+" "+numbers[n])
                whisper(nickname, " -- 위의 코드는 신고시에 필요한 코드입니다! 해당하는것을 골라주세요. --")
                
            elif cmd[0] == "!info":
                whisper(nickname," KKuTu Korea - Report Bot.")
                whisper(nickname," Powered By. 이은학(Eunhak Lee)")
                whisper(nickname," https://github.com/return0927")
            else:
                whisper(nickname," 잘못된 명령어입니다. !commands 를 입력해서 명령어를 확인해보세요!")

        elif jsonstring['type'] == "chat":
            if "title" in jsonstring['profile'].keys():
                nickname = jsonstring['profile']['title']
            else:
                nickname = jsonstring['profile']['name']
            if jsonstring['value'].replace(" ","") == "신고봇나와라":
                #ws.send('{"type":"talk","value":"안녕하세요 신고봇입니다! 명령어 사용은 귓속말로 해주세요 :D (귓속말은 /ㄷ [닉네임] [할말] 로 하실 수 있습니다!)"}')
                whisper(nickname.replace(" ",""), "안녕하세요 신고봇입니다! 채팅창에 /e GUEST3196 !commands 를 입력해보세요!")
            """elif jsonstring['value'] == '앙':
                ws.send('{"type":"talk","value":"기모띠"}')"""
            print(nickname+"("+jsonstring['profile']['id'][:5]+") : "+jsonstring['value'])
            threading.Thread(target=log, args=("chat", nickname+"("+jsonstring['profile']['id'][:5]+") : "+jsonstring['value'] ) ).start()
            #print(jsonstring)
            #print(jsonstring)
        else:
            threading.Thread(target=log, args=("output", str(jsonstring) )).start()
def on_close(ws):
    print(" ## Socket died ")

websocket.enableTrace(True)
ws = websocket.WebSocketApp(socket_url, on_message=procedure, on_close=on_close)
ws.run_forever()
