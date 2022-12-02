#! /usr/bin/env python3
import hashlib,os,csv,sys,subprocess,time,json
# ,requests
# from pathlib import Path

options={
	"f":"87247851", # 
	"i":"6", # 包含DID的nft钱包ID
	"rp":"500", # 版税
	"m":"0.0000001", # 手续费
	"ra":"xch19f2w4knrnrdmv95u7ats90fx05wrjfs627jkc62v6037289cvyrqy5nw0n", # 版税接收地址
	"ta":"xch124mstdlmzvyd27ruvvgq0g2aunj8zmar2dnhl23ppa52g4pkfdsq0dsdzk", # nft接收地址
	"nftaddr":"https://bafybeihzzpvsolpzaliooz5m3cmdjef7zcmygzv4gdq2aaofzvssyalgt4.ipfs.nftstorage.link/", # nft图片文件网址
	"metaaddr":"https://bafybeihzzpvsolpzaliooz5m3cmdjef7zcmygzv4gdq2aaofzvssyalgt4.ipfs.nftstorage.link/", # meta文件网址
	"lu":"https://bafybeie5dicifbwhrimvlvux7ycgszjjdkleywk5lf4savr4oa542acuei.ipfs.nftstorage.link/", # 许可文件网址
	"lh":"f138ce36b89a0829c34b363d0a577c511f5392b2b3b9aaecacab663bfba41338" # 许可文件hash
}
options_from_file=""
maindata={
	"chia":"/Applications/Chia.app/Contents/Resources/app.asar.unpacked/daemon/chia",
	"lang":"",
	"lastnft_id":"NONE",
	"index":0
}

def tool_print(line,text):
	print("\033[7;31;47m Line:"+str(line)+" \033[0m",text)

def tool_lang(langstr):
	options_from_file=json.load(open("options_mint.json"))
	_i18n=options_from_file["i18n"]
	return _i18n[langstr][maindata["lang"]]

def set_hash():
	tool_print(str(sys._getframe().f_lineno)+" "+"set hash","...")
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
	conf["m_writer"].writerow(("name_nft","hash_nft","name_meta","hash_meta","mint"))

	# _path_nft = os.path.abspath(os.path.expanduser(os.path.expandvars("nft")))
	# _path_meta = os.path.abspath(os.path.expanduser(os.path.expandvars("meta")))

	# print(os.listdir(os.path.expanduser('./nft')))

	_path_nft=os.path.abspath(os.path.expanduser(os.path.expandvars("nft")))
	_path_meta=os.path.abspath(os.path.expanduser(os.path.expandvars("meta")))
	tool_print(str(sys._getframe().f_lineno)+" "+"",_path_nft)
	_nfts= os.listdir(_path_nft)
	for _nft in _nfts: 
		if not os.path.isdir(_nft):
			print(_nft)
			name_nft=_nft
			hash_nft=get_hash(_path_nft+"/"+_nft)
			name_meta=_nft.split(".")[0]+".json"
			hash_meta=get_hash(_path_meta+"/"+name_meta)
			conf["m_writer"].writerow((name_nft,hash_nft,name_meta,hash_meta,"n"))

def nft_mint():
	tool_print(str(sys._getframe().f_lineno)+" "+"minting","...")
	_f=options["f"]
	_i=options["i"]
	_ra=options["ra"]
	_ta=options["ta"]

	_files=open("hash.csv").readlines()
	for i in range(0,len(_files)):
		tool_print(str(sys._getframe().f_lineno)+" "+"flags",_files[i].split(",")[4].strip())
		if _files[i].split(",")[4].strip()=="n":
			maindata["index"]=i
			_u=options["nftaddr"]+_files[i].split(",")[0].strip()
			_nh=_files[i].split(",")[1].strip()
			_mu=options["metaaddr"]+_files[i].split(",")[2].strip()
			_mh=_files[i].split(",")[3].strip()
			_rp=options["rp"]
			_m=options["m"]
			_lu=options["lu"]
			_lh=options["lh"]
			while True:
				# print([maindata["chia"], 'wallet', 'nft', 'mint', '-f', _f, '-i', _i, '-ra', _ra, '-ta', _ta, '-u', _u, '-nh', _nh, '-mu', _mu, '-mh', _mh, '-rp', _rp, '-m', _m])
				_mint=subprocess.run([maindata["chia"], 'wallet', 'nft', 'mint', '-f', _f, '-i', _i, '-ra', _ra, '-ta', _ta, '-u', _u, '-nh', _nh, '-mu', _mu, '-mh', _mh, '-lu', _lu, '-lh', _lh, '-rp', _rp, '-m', _m],capture_output=True,text=True)
				print(_mint.stdout.split("\n"))
				if _mint.returncode==0:
					_out=_mint.stdout.split("\n")
					for i in _out:
						if "NFT minted Successfully" in i:
							tool_print(str(sys._getframe().f_lineno)+" "+"minting:","NFT minted Successfully")
							return True
				time.sleep(5)
	return False

def nft_mint_checked():
	while True:
		_sub=subprocess.run([maindata["chia"], 'wallet', 'nft', 'list', '-f', options["f"], '-i', options["i"]],capture_output=True,text=True)
		if _sub.returncode==0 :
			_out=_sub.stdout.split("\nNFT ident")
			if len(_out)==1:
				return False #!!!
			_list=_out[len(_out)-1].split("\n")
			for ii in _list:
				# print(ii)
				if ii.split(":")[0].strip()=="ifier":
					if maindata["lastnft_id"]=="NONE":
						maindata["lastnft_id"]=ii.split(":")[1].strip()
						continue
					if ii.split(":")[1].strip()==maindata["lastnft_id"]:
						tool_print(str(sys._getframe().f_lineno)+" "+"check false","last: "+maindata["lastnft_id"]+" || current: "+ii.split(":")[1].strip())
						return False
					else:
						tool_print(str(sys._getframe().f_lineno)+" "+"check true","last: "+maindata["lastnft_id"]+" || current: "+ii.split(":")[1].strip())
						maindata["lastnft_id"]=ii.split(":")[1].strip()
						file_update()
						return True
		time.sleep(5)

def file_update():
	if not os.path.exists("sucess/nft"):
		os.makedirs("sucess/nft")
	if not os.path.exists("sucess/meta"):
		os.makedirs("sucess/meta")

	_lines=open("hash.csv").readlines()
	_newdata=open("hash_new.csv","a")
	for line in range(0,len(_lines)):
		if line!=maindata["index"]:
			_newdata.writelines(_lines[line].strip()+"\n")
		else:
			_newdata.writelines(_lines[line].strip()[:-1]+maindata["lastnft_id"]+"\n")
			os.rename("nft/"+_lines[line].split(",")[0].strip(),"sucess/nft/"+_lines[line].split(",")[0].strip())
			os.rename("meta/"+_lines[line].split(",")[2].strip(),"sucess/meta/"+_lines[line].split(",")[2].strip())
	os.rename("hash_new.csv", "hash.csv")

def rpc_rq(rpcport,endpoint,data):
	headers = {'Content-Type': 'application/json','Accept': 'application/json'}
	url = "https://localhost:"+str(rpcport)+"/"+endpoint
	cert = ('/root/.chia/mainnet/config/ssl/wallet/private_wallet.crt', '/root/.chia/mainnet/config/ssl/wallet/private_wallet.key')
	if data:
		req=requests.post(url, data=data, headers=headers, cert=cert, verify=False).text
	else:
		req=requests.post(url, headers=headers, cert=cert, verify=False).text
	print(req)
	response = json.loads(req)
	print(json.dumps(response,indent=4, sort_keys=True))
	return response


def set_options():
	while True:
		_type=str(input("\n"+tool_lang("options_type_0")+tool_lang("options_type_1")+"\n"+"\033[7;31;47m"+tool_lang("options_type")+"\033[0m :")).strip()
		if _type=="0":
			for _opt in options:
				while True:
					if _opt=="f":
						_f=rpc_rq(9256,"get_public_keys",'{"fingerprint":""}')["public_key_fingerprints"]
						_str=""
						for i in range(0,len(_f)):
							_str=_str+str(i)+" : "+str(_f[i])+"\n"
						options[_opt]=str(_f[int(str(input("\n"+_str+"\033[7;31;47m"+str(tool_lang(str(_opt)+"_des"))+"\033[0m :")).strip())]).strip()
						rpc_rq(9256,"log_in",'{"fingerprint":'+options[_opt]+'}')
					elif _opt=="i":
						_i=rpc_rq(9256,"get_wallets",'{"include_data":false}')["wallets"]
						_str=""
						for i in range(0,len(_i)):
							_str=_str+str(i)+" : "+str(_i[i])+"\n"
						options[_opt]=str(_i[int(str(input("\n"+_str+"\033[7;31;47m"+str(tool_lang(str(_opt)+"_des"))+"\033[0m ：")).strip())]["id"])
					# elif _opt=="ra":

					else:
						options[_opt]=str(input("\033[7;31;47m"+str(tool_lang(str(_opt)+"_des"))+"\033[0m ：")).strip()
					if options[_opt]=="" and str(_opt).strip() not in ["lu","lh"]:
						continue
					else:
						break
			print(options)
			break

		elif _type=="1":
			break
			

if __name__ == "__main__":
	# while True:
	# 	_lang=["zh_CN","en"]
	# 	_input=input("\n0 : 简体中文 - zh_CN \n1 : English - en \n"+"\033[7;31;47m选择语言？| Chose language type? [1] \033[0m :").strip()
	# 	if _input=="":
	# 		_input="1"
	# 	if _input in ["0","1"]:
	# 		maindata["lang"]=_lang[int(_input)]
	# 		break

	# set_options()
	set_hash()
	while nft_mint():
		while not nft_mint_checked():
			time.sleep(5)