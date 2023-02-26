#! /usr/bin/env python3
import requests,json,time,subprocess,sys,os,sqlite3
import numpy as np
import urllib3
from bech32m_chia import bech32m
urllib3.disable_warnings()

options={}

def tool_print(line,text):
	print("\033[7m"+time.strftime("%H:%M:%S ", time.localtime())+str(line)+": "+"\033[0m",text)

def tool_checkstatus():
	tool_print(str(sys._getframe().f_lineno)+" "+"checking chia wallet status","...")
	while True:
		try:
			_obj_log_in={
				"fingerprint": tool_options("fingerprint")
			}
			log_in=tool_requests("wallet","log_in",json.dumps(_obj_log_in))
			if log_in["success"]:
				while True:
					try:
						sync_status=tool_requests("wallet","get_sync_status",'{"fingerprint":""}')
						if sync_status["success"] and sync_status["synced"] and not sync_status["syncing"]:
							return True
						else:
							time.sleep(10)
					except Exception as e:
						print(e)
						time.sleep(10)
			else:
				time.sleep(10)
		except Exception as e:
			print(e)
			time.sleep(10)

def tool_options(type):
	return options[type]["value"]

def tool_requests(type,endpoint,data):
	while True:
		try:
			headers = {'Content-Type': 'application/json','Accept': 'application/json'}
			url = "https://localhost:"+str(tool_options("chia_port")[type])+"/"+endpoint
			cert=(os.path.join(tool_options("chia_ssl"),type,"private_"+type+".crt"),os.path.join(tool_options("chia_ssl"),type,"private_"+type+".key"))
			if data:
				req=requests.post(url, data=data, headers=headers, cert=cert, verify=False).text
			else:
				req=requests.post(url, headers=headers, cert=cert, verify=False).text
			response = json.loads(req)
			# print(response)
			return response
		except Exception as e:
			tool_print(str(sys._getframe().f_lineno)+" "+"flag","tool_requests error")
			print(e)
			time.sleep(10)

def nft_transfer(ids):
	tool_print(str(sys._getframe().f_lineno)+" "+"pushing to memorypool","...")
	_j={
		"nft_coin_list":ids,
		"target_address":tool_options("target_address"),
		"fee":tool_options("fee")
	}

	while True:
		try:
			_transfer=tool_requests("wallet","nft_transfer_bulk",json.dumps(_j))
			if _transfer["success"]:
				tool_print(str(sys._getframe().f_lineno)+" "+"pushed to memorypool","...")
				while True:
					tool_print(str(sys._getframe().f_lineno)+" "+"checking","...")
					nftid,walletid,checked=ids[0]["nft_coin_id"],ids[0]["wallet_id"],True
					_check=tool_requests("wallet","nft_get_nfts",'{"wallet_id":'+str(ids[0]["wallet_id"])+'}')
					for i in _check["nft_list"]:
						if i["nft_coin_id"][2:]==nftid and i["pending_transaction"]==True:
							checked=False
							break
					if checked:
						return True
					else:
						time.sleep(5)
			else:
				time.sleep(10)
		except Exception as e:
			print(e)
			time.sleep(10)

def nft_ids():
	tool_print(str(sys._getframe().f_lineno)+" "+"geting nft ids","...")
	ids=[]
	wallets=tool_requests("wallet","get_wallets",'{"include_data": false}')
	for i in wallets["wallets"]:
		if i["type"]==10:
			nfts=tool_requests("wallet","nft_get_nfts",'{"wallet_id": '+str(i["id"])+'}')
			for _nft in nfts["nft_list"]:
				if _nft["minter_did"] and bech32m.encode(_nft["minter_did"],"did:chia:")==tool_options("minter_did"):
					_j={
						"nft_coin_id":_nft["nft_coin_id"],
						"wallet_id":str(i["id"])
					}
					ids.append(_j)
	return ids

if __name__ == "__main__":
	start_time = time.time()
	options=json.loads(open("config/options.json","rb").read())
	tool_checkstatus()

	ids=nft_ids()
	ids=np.array_split(ids, int(len(ids)/25)+1)
	for i in ids:
		nft_transfer(list(i))

	tool_print(str(sys._getframe().f_lineno)+" "+"time total used",str(time.time() - start_time)+" s")


