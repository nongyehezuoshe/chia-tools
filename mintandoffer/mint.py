#! /usr/bin/env python3

import hashlib,os,csv,sys,subprocess,time

options={
	"f":"708222379", # 
	"i":"3", # 包含DID的nft钱包ID
	"rp":"500", # 版税
	"ra":"xch1l63jc638ln892za2ur6ml3p7n0ez6llt45mjuuxyz24zz8erphnqs8l4m2", # 版税接收地址
	"ta":"xch1l63jc638ln892za2ur6ml3p7n0ez6llt45mjuuxyz24zz8erphnqs8l4m2", # nft接收地址
	"nftaddr":"https://test.com/", # nft图片文件网址
	"metaaddr":"https://test.com/", # meta文件网址
	"r":"1:1" # offer文件对应的请求xch的金额，格式：xch钱包id:xch金额
}
maindata={
	"amount":0,
	"lastnft":["NONE","NONE"],
	"nftaddr":"NONE",
	"data":{
		"name_nft":"",
		"name_meta":"",
		"hash_nft":"",
		"hash_meta":""
	}

}

def tool_print(line,text):
	print("\033[7;31;47m Line:"+str(line)+" \033[0m",text)

def mint_new_nft():
	with open('hash.csv', 'r') as inp:
		reader = csv.DictReader(inp)
		_flag=0
		for row in reader:
			if _flag==1:
				for i in maindata["data"]:
					maindata["data"][i]=row[i]
				break
			_flag=_flag+1

	_f=options["f"]
	_i=options["i"]
	_ra=options["ra"]
	_ta=options["ta"]

	_u=options["nftaddr"]+maindata["data"]["name_nft"]
	_nh=maindata["data"]["hash_nft"]

	_mu=options["metaaddr"]+maindata["data"]["name_meta"]
	_mh=maindata["data"]["hash_meta"]

	while True:
		_mint=subprocess.run(['chia', 'wallet', 'nft', 'mint', '-f', _f, '-i', _i, '-ra', _ra, '-ta', _ta, '-u', _u, '-nh', _nh, '-mu', _mu, '-mh', _mh, '-rp', '1', '-m', '0'],capture_output=True,text=True)
		print(_mint.stdout.split("\n"))
		if _mint.returncode==0:
			_out=_mint.stdout.split("\n")
			for i in range(0,len(_out)):
				if "NFT minted Successfully" in _out[i]:
					return True
		time.sleep(5)

def mint_get_current():
	while True:
		_sub=subprocess.run(['chia', 'wallet', 'nft', 'list', '-f', options["f"], '-i', options["i"]],capture_output=True,text=True)
		_value=["",""]
		if _sub.returncode==0 :
			_out=_sub.stdout.split("\n")
			for i in range(len(_out)-1,0,-1):
				if "NFT identifier" in _out[i]:
					_value[0]=_out[i].split()[2]
				if "Current NFT coin ID" in _out[i]:
					_value[1]=_out[i].split()[4]
				if _value[0] and _value[1]:
					return _value
			return ["NONE","NONE"]
		time.sleep(5)

def mint_done():
	while True:
		_current_nft=mint_get_current()
		tool_print(sys._getframe().f_lineno,_current_nft[0])
		if _current_nft[0]!="NONE" and maindata["lastnft"][0]!=_current_nft[0]:
			tool_print(sys._getframe().f_lineno,maindata["lastnft"][0])
			tool_print(sys._getframe().f_lineno,"!=")
			maindata["lastnft"]=_current_nft
			return True
		else:
			tool_print(sys._getframe().f_lineno,maindata["lastnft"][0])
			tool_print(sys._getframe().f_lineno,"=")
			time.sleep(10)

def set_offer():
	tool_print(sys._getframe().f_lineno,"generating offer file")
	_f=options["f"]
	_i=options["i"]
	_p=maindata["lastnft"][0]+".offer"
	_o=maindata["lastnft"][0]+":1"
	_r=options["r"]

	print(['chia', 'wallet', 'make_offer', '-f', _f, '-p', 'offer/'+maindata["lastnft"][0]+'.offer', '-o', _o, '-r', _r])
	while True:
		_offer=subprocess.run(['chia', 'wallet', 'make_offer', '-f', _f, '-p', 'offer/'+maindata["lastnft"][0]+'.offer', '-o', _o, '-r', _r],capture_output=True,text=True,input="y\ny")
		if _offer.returncode==0 :
			print(_offer.stdout)
			break
	return

def set_hash():
	def get_hash(url):
		with open(url,'rb') as f:
			sha1obj = hashlib.sha256()
			sha1obj.update(f.read())
			hash = sha1obj.hexdigest()
			return hash

	open('hash.csv', 'w').close()
	f_m = open('hash.csv', 'a')
	conf={
		"m_writer":""
	}
	conf["m_writer"]=csv.writer(f_m)
	conf["m_writer"].writerow(("name_nft","hash_nft","name_meta","hash_meta"))

	path = "nft"
	files= os.listdir(path)
	maindata["amount"]=len(files)
	for file in files: 
		if not os.path.isdir(file):
			name_nft=file
			hash_nft=get_hash(path+"/"+file)
			name_meta=file.split(".")[0]+".json"
			hash_meta=get_hash("meta"+"/"+name_meta)
			conf["m_writer"].writerow((name_nft,hash_nft,name_meta,hash_meta))

def update_csv():
	with open('hash.csv', 'r') as inp, open('hash_tmp.csv', 'w') as outp:
		reader = csv.DictReader(inp)
		writer = csv.DictWriter(outp, fieldnames=["name_nft","hash_nft","name_meta","hash_meta"])
		writer.writerow({"name_nft":"name_nft","hash_nft":"hash_nft","name_meta":"name_meta","hash_meta":"hash_meta"})
		for row in reader:
			if row["name_nft"]!=maindata["data"]["name_nft"]:
				writer.writerow(row)
				continue
	outp.close()
	subprocess.run(["mv","hash_tmp.csv","hash.csv"],capture_output=True,text=True)

	with open('nft.csv', 'a') as nftout:
		writer = csv.writer(nftout)
		writer.writerow(maindata["lastnft"])
	nftout.close()

def mint_nft():
	set_hash()
	mint_amount=maindata["amount"]
	maindata["lastnft"]=mint_get_current()
	tool_print(sys._getframe().f_lineno,"start mint, total: "+str(mint_amount))
	while mint_amount>0:
		tool_print(sys._getframe().f_lineno,"START")
		mint_new_nft()
		mint_done()
		set_offer()
		mint_amount=mint_amount-1
		update_csv()
		tool_print(sys._getframe().f_lineno,"DONE, left: "+str(mint_amount))
		time.sleep(5)
	return

if __name__ == "__main__":
	mint_nft()