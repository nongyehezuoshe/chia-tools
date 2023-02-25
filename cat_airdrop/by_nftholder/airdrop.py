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

async def httpx_cat_spend(data,inner_address):
	url="https://localhost:9256/cat_spend"
	cert=(os.path.join(tool_options("chia_ssl"),"wallet","private_"+"wallet"+".crt"),os.path.join(tool_options("chia_ssl"),"wallet","private_"+"wallet"+".key"))
	headers = {'Content-Type': 'application/json','Accept': 'application/json'}
	async with sem:
		async with httpx.AsyncClient(cert=cert,headers=headers,verify=False) as client:
			while True:
				try:
					res=await client.post(url,data=data)
					tool_print(str(sys._getframe().f_lineno)+" "+"status code",""+str(res.status_code))
					res.raise_for_status()
					return res.json()
				except httpx.HTTPError as e:
				# except Exception as e:
					tool_print(str(sys._getframe().f_lineno)+" "+"flag","httpx post error @ "+inner_address)
					print(e)
					# return False
					time.sleep(1)

async def cat_transfer(inner_address):
	# tool_print(str(sys._getframe().f_lineno)+" "+"inner_address",inner_address)
	amount=sql_amount(inner_address)
	# while amount:
	_j={
		"wallet_id":tool_options("cat_wallet_id"),
		"amount":amount*1000,
		"fee":tool_options("cat_fee"),
		"inner_address":inner_address
	}
	cat_spend=await httpx_cat_spend(json.dumps(_j),inner_address)
	print(cat_spend)
	if cat_spend["success"] and cat_spend["transaction_id"]:
		_id=cat_spend["transaction_id"]
		tool_print(str(sys._getframe().f_lineno)+" "+"transfer id",_id)
		if _id:
			maindata["success_memory"].append([_id,inner_address])
			return _id
	else:
		maindata["failed"].append([inner_address,amount*1000])
	return False

	# if cat_spend["success"] and cat_spend["transaction_id"]:
	# 	tool_print(str(sys._getframe().f_lineno)+" "+"transfer",inner_address+" "+str(amount))
	# 	_id=cat_spend["transaction_id"]
	# 	while _id:
	# 		if not cat_transfer_check(_id,inner_address):
	# 			time.sleep(tool_options("cat_check_time"))
	# 		else:
	# 			break
	# 	return _id
	# else:
	# 	tool_print(str(sys._getframe().f_lineno)+" "+"flag","cat_transfer MAYBE failed")
	# 	f=open("out_may_failed_"+str(table)+".csv","a")
	# 	f.writelines(inner_address+","+str(amount*1000)+"\n")
	# 	time.sleep(10)
	# return False

	# return True

def cat_transfer_check(transArray):
	tool_print(str(sys._getframe().f_lineno)+" "+"check id",str(transArray[0]))

	while True:
		try:
			_j={
				"transaction_id":str(transArray[0])
			}
			get_transaction=tool_requests("wallet","get_transaction",json.dumps(_j))
			if get_transaction["success"] and get_transaction["transaction"]["confirmed"]:
				tool_print(str(sys._getframe().f_lineno)+" "+"transfer_check",str(transArray[0])+" OK")
				sql_update(transArray[1])
				return True
			else:
				tool_print(str(sys._getframe().f_lineno)+" "+"transfer_check",str(transArray[0])+" NO")
				return False
		except Exception as e:
			tool_print(str(sys._getframe().f_lineno)+" "+"flag","transfer_check error")
			print(e)
			time.sleep(10)

	# while True:
	# 	try:
	# 		_j={
	# 			"transaction_id":transaction_id
	# 		}
	# 		get_transaction=tool_requests("wallet","get_transaction",json.dumps(_j))
	# 		if get_transaction["success"] and get_transaction["transaction"]["confirmed"]:
	# 			tool_print(str(sys._getframe().f_lineno)+" "+"transfer_check",transaction_id+" OK")
	# 			sql_update(xchaddr)
	# 			return True
	# 		else:
	# 			tool_print(str(sys._getframe().f_lineno)+" "+"transfer_check",transaction_id+" ing...")
	# 			return False
	# 	except Exception as e:
	# 		tool_print(str(sys._getframe().f_lineno)+" "+"flag","transfer_check error")
	# 		print(e)
	# 		time.sleep(10)

def sql_all(holders):
	table="""list_"""+str(int(time.time()))
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

# def sql_update(xchaddr):
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

	if os.path.exists("config/nft_special.csv"):
		nft_special=open("config/nft_special.csv","r").read().split("\n")
		def not_empty(ele):
			return ele and ele.strip()
		nft_special=list(filter(not_empty,nft_special))

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
						_holder_mount=int(list(ii.values())[0])
						if _holder_xch in tool_options("nft_exclude_addr") or _holder_nft in tool_options("nft_exclude_nftid"):
							continue
						else:
							for iii in nft_special:
								if iii.split(",")[0].strip() == _holder_nft:
									_holder_mount=int(iii.split(",")[1].strip())
									break

							# tool_print(str(sys._getframe().f_lineno)+" "+"holders",i["owner_address_encoded_id"])
							if _holder_xch in holders:
								holders[_holder_xch]=int(holders[_holder_xch])+_holder_mount
							else:
								holders[_holder_xch]=_holder_mount

				page="page="+str(r.json()["next"])+"&"
				if r.json()["next"]==r.json()["page"]:
					break
				time.sleep(3)
				continue
			except Exception as e:
				tool_print(sys._getframe().f_lineno,e)
				time.sleep(10)

	return holders

if __name__ == "__main__":
	# loop = asyncio.get_event_loop()
	# tasks=[]
	while True:
		maindata["failed"]=[]
		maindata["success_memory"]=[]

		start_time = time.time()
		tool_print(str(sys._getframe().f_lineno)+" "+"get nft holders","...")
		options=json.loads(open("config/options.json","rb").read())
		tool_checkstatus()
		holders=nft_holders()
		xchaddrs,table=sql_all(holders)
		tool_print(str(sys._getframe().f_lineno)+" "+"time for get nft holders",str(time.time() - start_time)+" s")
		tool_print(str(sys._getframe().f_lineno)+" "+"time total used",str(time.time() - start_time)+" s")

		time_push = time.time()
		tool_print(str(sys._getframe().f_lineno)+" "+"push to memorypool","...")
		sem = asyncio.Semaphore(int(tool_options("coroutine_num")))
		loop=asyncio.new_event_loop()
		asyncio.set_event_loop(loop)
		tasks=[]
		for i in xchaddrs:
			tasks.append(cat_transfer(i))
		loop.run_until_complete(asyncio.wait(tasks))
		tool_print(str(sys._getframe().f_lineno)+" "+"time for push to memorypool",str(time.time() - time_push)+" s")
		tool_print(str(sys._getframe().f_lineno)+" "+"time total used",str(time.time() - start_time)+" s")

		time_check = time.time()
		tool_print(str(sys._getframe().f_lineno)+" "+"check transaction","...")
		# while len(maindata["success_memory"])!=0:
		# 	for i in maindata["success_memory"]:
		# 		cat_transfer_check(i)
		# 	time.sleep(1)
		
		# while len(maindata["success_memory"])!=0:
		# 	sem = asyncio.Semaphore(int(tool_options("coroutine_num")))
		# 	loop=asyncio.new_event_loop()
		# 	asyncio.set_event_loop(loop)
		# 	tasks_check=[]
		# 	for i in maindata["success_memory"]:
		# 		tasks_check.append(cat_transfer_check(i))
		# 	loop.run_until_complete(asyncio.wait(tasks_check))
		# 	time.sleep(1)
		tool_print(str(sys._getframe().f_lineno)+" "+"time for check transaction",str(time.time() - time_check)+" s")

		tool_print(str(sys._getframe().f_lineno)+" "+"some transaction MAYBE failed","!!!")
		f=open("out_may_failed_"+str(table)+".csv","a")
		for i in maindata["failed"]:
			f.writelines(str(maindata["failed"][0])+","+str(maindata["failed"][1])+"\n")
		maindata["failed"]=[]

		tool_print(str(sys._getframe().f_lineno)+" "+"\nThis round of airdrop completed! time for current round",str(time.time() - start_time)+" s")
		tool_print(str(sys._getframe().f_lineno)+" "+"wating for next round","...")
		time.sleep(tool_options("loop_time")*60*60)


