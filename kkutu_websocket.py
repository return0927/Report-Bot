import websocket, codecs, json, threading
from tkinter import *
from time import strftime
import json

with codecs.open("setting.json","r",encoding="UTF-8") as f:
    settings = json.loads("".join(f.readlines()).replace("\r","").replace("\n",""))



is_first = True

time = strftime("-%Y%m%d-%H%M%S")

"""
root = Tk()
lb = Label(root)
lb.pack(anchor="w")
lb.config(text="==============================", justify="left", font=('굴림체',10))

root.update()
"""

def procedure(ws, message):
    command(ws,message)

def whisper(to, m):
    global ws
    ws.send('{"type":"talk","whisper":"'+to+'","value":"'+m+'"}')
def command(ws,message):
    global is_first
    if is_first == True:
        with codecs.open("output"+time+".txt","w",encoding="UTF-8") as f:
            f.write(" #### Daemon Started ####\n")
        is_first = False
        #ws.send('{"type":"talk","value":""}')
        #ws.send('{"type":"talk","value":"신고 자동화시스템 제작중입니다. 제주도여행중에 일하고있습니다 ㅠ"}')
        #ws.send('{"type":"talk","value":"Powered by [운영자]이은학"}')
        ws.send('{"type":"talk","whisper":"이은학","value":"=== Report Daemon Started ==="}')
        #print(" ## Socket Message %d length" % len(message))
        pass
    else:
        #with codecs.open("output"+time+".txt","a",encoding="UTF-8") as f:
        #    f.write(message+"\n")
        #print(" ## Socket Message %d length" % len(message))
        jsonstring = json.loads(message)
        if "from" in jsonstring.keys():
            print(" Whisper from %s : %s"% (jsonstring['from'],jsonstring['value']))
            cmd = jsonstring['value'].split(" ")
            if cmd[0] == "!commands":
                whisper(jsonstring['from']," 안녕하세요 끄투 신고봇입니다. 아래는 명령어 목록입니다.")
                whisper(jsonstring['from']," !report [신고번호] [고유번호 or 닉네임] [자세한 설명] / 유저를 신고하는 기능입니다.")
                whisper(jsonstring['from']," !number / 신고번호를 조회합니다.")
                whisper(jsonstring['from']," !info / 끄투봇의 정보를 봅니다.")
                #whisper(jsonstring['from']," !")
            elif cmd[0] == "!report":
                whisper(jsonstring['from'], " 신고가 접수되었습니다. 유저정보와 시각이 모두 기록되므로 허위신고는 처벌받을 수 있습니다.")
                print(" %d" %len(cmd))
                print(" %s " %cmd[1])
                print(" %s " %" ".join(cmd[2:]))
            elif cmd[0] == "!number":
                whisper(jsonstring['from'], " K001 누가 저에게 비속어와 비방하는 말을 해서 기분이 나빠요!")
                whisper(jsonstring['from'], " K002 채팅창에서 비슷한 문구를 계속 작성해서 보기 안좋아요!")
                whisper(jsonstring['from'], " K003 여기 방 제목이 이상해요!")
                whisper(jsonstring['from'], " K004 게임이 이상해요! ")
                whisper(jsonstring['from'], " K005 뭐가 이상한지는 모르겠는데 이상해요!")
                whisper(jsonstring['from'], " -- 위의 코드는 신고시에 필요한 코드입니다! 해당하는것을 골라주세요. --")
            elif cmd[0] == "!info":
                whisper(jsonstring['from']," KKuTu Korea - Report Bot.")
                whisper(jsonstring['from']," Powered By. 이은학(Eunhak Lee)")
                whisper(jsonstring['from']," https://github.com/return0927")
            else:
                whisper(jsonstring['from']," 잘못된 명령어입니다. !commands 를 입력해서 명령어를 확인해보세요!")
                
        #lb.config(text=message, justify="left", font=('굴림체',10))

def on_close(ws):
    print(" ## Socket died ")

websocket.enableTrace(True)
ws = websocket.WebSocketApp("ws://kkutu.co.kr:8080/43f0a8be79a20cf67ecf8655add613a6866d2487c0cc87a3440415c5c34b8c7bee50626857c14f46c6a582a2cf2bbf0b", on_message=procedure, on_close=on_close)
ws.run_forever()
