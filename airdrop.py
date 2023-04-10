#! /usr/bin/env python3
import requests,json,time,subprocess,sys,os,sqlite3
import httpx,asyncio
import urllib3
urllib3.disable_warnings()

options={}
maindata={
	"failed":[],
	"success":[]
}

def tool_print(line,text):
	# tool_print(str(sys._getframe().f_lineno)+" "+"show","message")
	print("\033[7m"+time.strftime("%H:%M:%S ", time.localtime())+str(line)+": "+"\033[0m",text)

def tool_checkstatus():
	while True:
		try:
			_obj_log_in={
				"fingerprint": tool_options("cat_fingerprint")
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
	# tool_requests("wallet","nft_mint_nft",json.dumps(_obj))
	while True:
		try:
			# print(type,endpoint,data)
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

def cat_transfer(bundle):
	tranfer=tool_requests("full_node","push_tx",bundle)
	print(tranfer)

def sql_all(holders):
	tool_print(str(sys._getframe().f_lineno)+" "+"flag","holders")
	print(holders)
	table="""list_"""+time.strftime("%Y_%m_%d_%H_%M_%S ", time.localtime())
	conn = sqlite3.connect('cat_airdrop.db')
	cur = conn.cursor()
	cur.execute("""CREATE TABLE IF NOT EXISTS """+table+""" (xch varchar(100), num INTEGER,transfer INTEGER,transferid varchar(100));""")

	xch_array=[]
	for i in holders:
		_xch_addr=i
		cur.execute("""INSERT INTO """+table+""" VALUES(?,?,?,?);""",(_xch_addr,holders[i],0,0))
		xch_array.append(_xch_addr)

	conn.commit()
	cur.close()
	conn.close()
	return xch_array,table

def sql_update(transArray):
	conn = sqlite3.connect('cat_airdrop.db')
	cur = conn.cursor()
	cur.execute("""UPDATE """+table+""" SET transfer= (?), transferid=(?) WHERE xch=(?);""",(1,transArray[0],transArray[1]))
	conn.commit()
	cur.close()
	conn.close()
	if transArray in maindata["success_memory"]:
		maindata["success_memory"].remove(transArray)
	tool_print(str(sys._getframe().f_lineno)+" "+"update sql","...")

def sql_amount(xchaddr):
	conn = sqlite3.connect('cat_airdrop.db')
	cur = conn.cursor()
	cur.execute("SELECT num FROM """+table+""" WHERE xch=(?);""",(xchaddr,))
	_get=cur.fetchall()
	conn.commit()
	cur.close()
	conn.close()
	return _get[0][0]

def nft_holders():
	tool_print(str(sys._getframe().f_lineno)+" "+"get holders data","...")
	# holders=[]
	holders={}
	nft_special=[]

	def check_special(dir):
		# print(dir)
		files= os.listdir(dir)
		for file in files:
			if os.path.isfile(os.path.join(dir,file)):
				if file.endswith(".csv"):
					_lines=open(os.path.join(dir,file),"r").read().split("\n")
					def not_empty(ele):
						return ele and ele.strip()
					_lines=list(filter(not_empty,_lines))
					for _line in _lines:
						nft_special.append(_line)
			else:
				check_special(os.path.join(dir,file))
	check_special("./additional_amount")

	for ii in tool_options("nft_collection_id"):
		page=""
		while True:
			try:
				tool_print(str(sys._getframe().f_lineno)+" "+"request:","https://api.mintgarden.io/collections/"+list(ii.keys())[0]+"/nfts?"+page+"size=100")
				r = requests.get("https://api.mintgarden.io/collections/"+list(ii.keys())[0]+"/nfts?"+page+"size=100")
				if r.status_code==200:
					for i in r.json()["items"]:
						_holder_xch=i["owner_address_encoded_id"]
						_holder_nft=i["encoded_id"]
						_holder_amount=int(list(ii.values())[0])
						if _holder_xch in tool_options("nft_exclude_addr") or _holder_nft in tool_options("nft_exclude_nftid"):
							continue
						else:
							for iii in nft_special:
								if iii.split(",")[0].strip() == _holder_nft:
									_holder_amount=_holder_amount+int(iii.split(",")[1].strip())
									break

							if _holder_xch in holders:
								holders[_holder_xch]=int(holders[_holder_xch])+_holder_amount
							else:
								holders[_holder_xch]=_holder_amount

					page="page="+str(r.json()["next"])+"&"
					if r.json()["next"]==r.json()["page"]:
						break
				time.sleep(3)
				continue
			except Exception as e:
				tool_print(sys._getframe().f_lineno,e)
				time.sleep(10)

	return holders

def cat_bundle(holders):
	headers = {'Content-Type': 'application/json','Accept': 'application/json'}
	url = "http://localhost:3333/batch_send"
	data ={
		"privateKey":tool_options("privateKey"),
		"transferTarget":[
		]
	}
	flag=0
	for i in holders:
		_trans={
			"assetId":tool_options("cat_Id"),
			"address":i,
			"amount":holders[i]*1000,
			"fee":tool_options("cat_fee")
		}
		data["transferTarget"].append(_trans)

	data=json.dumps(data,indent=4, sort_keys=True)
	req=requests.post(url, data=data, headers=headers).text
	req=json.loads(req)

	for i in req["spend_bundle"]["coin_spends"]:
		for key,value in i.items():
			if key=="coin":
				value["amount"]=int(value["amount"])
				break
	s_bundle=json.dumps(req)
	print(s_bundle)
	return s_bundle

if __name__ == "__main__":
	while True:
		start_time = time.time()
		tool_print(str(sys._getframe().f_lineno)+" "+"get nft holders","...")
		options=json.loads(open("config/options.json","rb").read())
		tool_checkstatus()
		holders=nft_holders()
		xchaddrs,table=sql_all(holders)
		tool_print(str(sys._getframe().f_lineno)+" "+"time for get nft holders",str(time.time() - start_time)+" s")
		tool_print(str(sys._getframe().f_lineno)+" "+"time total used",str(time.time() - start_time)+" s")

		time_bundle = time.time()
		tool_print(str(sys._getframe().f_lineno)+" "+"geting bundle","...")
		bundle=cat_bundle(holders)
		# bundle=test()
		tool_print(str(sys._getframe().f_lineno)+" "+"time for geting bundle",str(time.time() - time_bundle)+" s")
		tool_print(str(sys._getframe().f_lineno)+" "+"time total used",str(time.time() - start_time)+" s")

		time_tranfer = time.time()
		tool_print(str(sys._getframe().f_lineno)+" "+"pushing to memorypool","...")
		transfer=cat_transfer(bundle)
		tool_print(str(sys._getframe().f_lineno)+" "+"time for pushing to memorypool",str(time.time() - time_tranfer)+" s")
		tool_print(str(sys._getframe().f_lineno)+" "+"time total used",str(time.time() - start_time)+" s")

		tool_print(str(sys._getframe().f_lineno)+" "+"\nThis round of airdrop completed! time for current round",str(time.time() - start_time)+" s")
		tool_print(str(sys._getframe().f_lineno)+" "+"wating for next round","...")
		time.sleep(tool_options("loop_time")*60*60)