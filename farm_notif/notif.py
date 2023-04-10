#! /usr/bin/env python3

import json
import datetime,time
import websocket
import ssl
import requests,uuid
import os

options={}
maindata={
    "id":str(uuid.uuid4()).replace("-",""),
    "passed_filter":0,
    "passed_filter_last_hour":0,
    "passed_filter_current_hour":0,
    "passed_filter_min":0,
    "time_start":time.time(),
    "time_start_hour":time.time(),
    "time_heartbeat":time.time()
}

def tool_options(type):
    return options[type]["value"]

def on_message(ws, message):
    wsmsg=json.loads(message)
    heartbeat("push")
    if wsmsg["command"]=="new_farming_info":
        print('{0} farming_info : {1}'.format(datetime.datetime.now(),wsmsg["data"]["farming_info"]))
        if tool_options("notif_point") and (time.time()-maindata["time_start_hour"])/60/60>1:
            if maindata["passed_filter_last_hour"]>0 and (maindata["passed_filter_last_hour"]-maindata["passed_filter_current_hour"])/maindata["passed_filter_last_hour"]>0.1:
                notifi_point([maindata["passed_filter_last_hour"],maindata["passed_filter_current_hour"]])

            maindata["passed_filter_last_hour"]=maindata["passed_filter_current_hour"]
            maindata["passed_filter_current_hour"]=0
            maindata["time_start_hour"]=time.time()

        if tool_options("notif_reward") and wsmsg["data"]["farming_info"]["proofs"]>0:
            notifi_reward(wsmsg["data"]["farming_info"])

        if wsmsg["data"]["farming_info"]["passed_filter"]>0:
            maindata["passed_filter_current_hour"]+=wsmsg["data"]["farming_info"]["passed_filter"]
            maindata["passed_filter"]+=wsmsg["data"]["farming_info"]["passed_filter"]

            maindata["passed_filter_min"]=maindata["passed_filter"]/((time.time()-maindata["time_start"])/60)
            print("min:",maindata["passed_filter_min"],"current_hour:",maindata["passed_filter_current_hour"],"last_hour:",maindata["passed_filter_last_hour"])

def on_close(ws, e):
    print("{0}: Websocket closed: {1}".format(datetime.datetime.now(), e))

def on_open(ws):
    message = {"destination": "daemon", "command": "register_service", "request_id": maindata["id"], "origin": "", "data": { "service": 'wallet_ui'}}
    print('{0}: Sent Message: {1}'.format(datetime.datetime.now(), message))
    ws.send(json.dumps(message))

def on_ping(ws, data):
    print('{0}: Got ping: {1}'.format(datetime.datetime.now(), data))

def notification(data):
    url = tool_options("notif_url")
    headers = {'Content-Type': 'application/json'}

    while True:
        try:
            response = requests.post(url, data=json.dumps(data), headers=headers).json()
            print("notif response:", response)
            return response
        except Exception as e:
            print("notif err:", e)
            time.sleep(10)

def notifi_reward(info):
    date_string = datetime.datetime.fromtimestamp(info["timestamp"]).strftime('%Y-%m-%d %H:%M:%S')
    data = {'title': tool_options("name")+': New chia farmed', "content": f'New chia farmed @ {date_string} !\n\n current filter is: {maindata["passed_filter_min"]}  \n\n {json.dumps(info)}'}
    notification(data)

def notifi_point(info):
    data = {'title': tool_options("name")+': Farm Abnormal', "content": f'Last hour passed filter is: {maindata["passed_filter_last_hour"]};\n\n  Current hour passed filter is {maindata["passed_filter_current_hour"]}'}
    notification(data)

def heartbeat(type):
    if not tool_options("notif_heartbeat"):
        return False

    time_intervals=max(tool_options("notif_heartbeat_interval"),30)
    def push():
        url=tool_options("notif_heartbeat_url")
        data={"type":type,"name":tool_options("name"),"time":time_intervals,"id":maindata["id"],"url":tool_options("notif_url")}
        headers = {'Content-Type': 'application/json'}

        print(data)
        while True:
            try:
                print("post heartbeat")
                response = requests.post(url, data=json.dumps(data), headers=headers).json()
                print("heartbeat response:",response)
                maindata["time_heartbeat"]=time.time()
                return response
            except Exception as e:
                print("heartbeat err:", e)
                # time.sleep(10)
                maindata["time_heartbeat"]=time.time()
                return False

    if type=="push" and (time.time()-maindata["time_heartbeat"])/60>time_intervals:
        push()
    elif type=="exit":
        push()

if __name__ == "__main__":
    options=json.loads(open("config/options.json","rb").read())
    try:
        ws = websocket.WebSocketApp(
            tool_options("chia_server"),
            on_open=on_open,
            on_message=on_message,
            on_close=on_close,
            on_ping=on_ping)

        ws.run_forever(
            sslopt={
                "cert_reqs": ssl.CERT_NONE,
                "certfile": os.path.join(tool_options("chia_ssl"),"wallet/private_wallet.crt"),
                "keyfile": os.path.join(tool_options("chia_ssl"),"wallet/private_wallet.key"),
                "ssl_context.check_hostname": False
            }
        )
    except KeyboardInterrupt:
        heartbeat("exit")