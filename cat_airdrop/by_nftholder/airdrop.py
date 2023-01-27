#! /usr/bin/env python3
import requests,json,time,subprocess,sys,os,sqlite3
import urllib3
urllib3.disable_warnings()

options={}

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

def cat_transfer(inner_address):
	tool_print(str(sys._getframe().f_lineno)+" "+"inner_address",inner_address)
	tool_checkstatus()
	amount=sql_amount(inner_address)
	print(inner_address,amount)
	return False
	while amount:
		_j={
			"wallet_id":tool_options("cat_wallet_id"),
			"amount":amount,
			"fee":tool_options("cat_fee"),
			"inner_address":inner_address
		}
		cat_spend=tool_requests("wallet","cat_spend",json.dumps(_j))
		if cat_spend["success"] and cat_spend["transaction_id"]:
			tool_print(str(sys._getframe().f_lineno)+" "+"transfer",inner_address+" "+str(amount))
			return cat_spend["transaction_id"]
		else:
			time.sleep(10)
	return False

def cat_transfer_check(transaction_id,xchaddr):
	tool_print(str(sys._getframe().f_lineno)+" "+"check id",transaction_id)
	tool_checkstatus()
	while True:
		try:
			_j={
				"transaction_id":transaction_id
			}
			get_transaction=tool_requests("wallet","get_transaction",json.dumps(_j))
			if get_transaction["success"] and get_transaction["transaction"]["confirmed"]:
				tool_print(str(sys._getframe().f_lineno)+" "+"transfer_check",transaction_id+" OK")
				sql_update(xchaddr)
				return True
			else:
				tool_print(str(sys._getframe().f_lineno)+" "+"transfer_check",transaction_id+" ing...")
				return False
		except Exception as e:
			tool_print(str(sys._getframe().f_lineno)+" "+"flag","transfer_check error")
			print(e)
			time.sleep(10)

def sql_all(holders):
	table="""list_"""+str(int(time.time()))
	conn = sqlite3.connect('cat_airdrop.db')
	cur = conn.cursor()
	cur.execute("""CREATE TABLE IF NOT EXISTS """+table+""" (xch varchar(100), num INTEGER,transfer INTEGER);""")

	xch_array=[]
	for i in holders:
		_xch_addr=i
		cur.execute("""INSERT INTO """+table+""" VALUES(?,?,?);""",(_xch_addr,holders[i],0))
		xch_array.append(_xch_addr)

	conn.commit()
	cur.close()
	conn.close()
	return xch_array,table

def sql_update(xchaddr):
	conn = sqlite3.connect('cat_airdrop.db')
	cur = conn.cursor()
	cur.execute("""UPDATE """+table+""" SET transfer= (?) WHERE xch=(?);""",(1,xchaddr))
	conn.commit()
	cur.close()
	conn.close()

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
	holders=[]
	for ii in tool_options("nft_collection_id"):
		page=""
		while True:
			try:
				tool_print(str(sys._getframe().f_lineno)+" "+"request:","https://api.mintgarden.io/collections/"+ii+"/nfts?"+page+"size=100")
				r = requests.get("https://api.mintgarden.io/collections/"+ii+"/nfts?"+page+"size=100")
				if r.status_code==200:
					for i in r.json()["items"]:
						_holder_xch=i["owner_address_encoded_id"]
						_holder_nft=i["encoded_id"]
						if _holder_xch in tool_options("nft_exclude_addr") or _holder_nft in tool_options("nft_exclude_nftid"):
							continue
						else:
							tool_print(str(sys._getframe().f_lineno)+" "+"holders",i["owner_address_encoded_id"])
							holders.append(i["owner_address_encoded_id"])

				page="page="+r.json()["next"]+"&"
				if r.json()["next"]==r.json()["page"]:
					break
				time.sleep(3)
				continue
			except Exception as e:
				tool_print(sys._getframe().f_lineno,e)
				time.sleep(10)

	dict = {}
	for key in holders:
		dict[key] = dict.get(key, 0) + 1
	# print(dict)
	return dict

if __name__ == "__main__":
	options=json.loads(open("config/options.json","rb").read())
	holders=nft_holders()
	xchaddrs,table=sql_all(holders)
	for i in xchaddrs:
		tool_print(str(sys._getframe().f_lineno)+" "+"i",i)
		transaction_id=cat_transfer(i)
		tool_print(str(sys._getframe().f_lineno)+" "+"transaction_id",transaction_id)
		while transaction_id:
			if not cat_transfer_check(transaction_id,i):
				time.sleep(tool_options("cat_check_time"))
			else:
				break
