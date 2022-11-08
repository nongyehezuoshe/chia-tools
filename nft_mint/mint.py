#! /usr/bin/env python3
import hashlib,os,csv,sys,subprocess,time

options={
	"f":"708222379", # 
	"i":"9", # 包含DID的nft钱包ID
	"rp":"500", # 版税
	"m":"0", # 手续费
	"ra":"xch1l63jc638ln892za2ur6ml3p7n0ez6llt45mjuuxyz24zz8erphnqs8l4m2", # 版税接收地址
	"ta":"xch1l63jc638ln892za2ur6ml3p7n0ez6llt45mjuuxyz24zz8erphnqs8l4m2", # nft接收地址
	"nftaddr":"https://bafybeihsslxjl7bkjfs3kxjxgghxmni5xmezsoowvub3kwqflv56qkuw34.ipfs.nftstorage.link/", # nft图片文件网址
	"metaaddr":"https://bafybeibtuqeullh5vwdrqhizsmaufe4kphrzkb4oyozwxht24yqiu5pzhe.ipfs.nftstorage.link/", # meta文件网址
	"lu":"https://creativecommons.org/licenses/by/4.0/legalcode.txt", # 许可文件网址
	"lh":"9ba9550ad48438d0836ddab3da480b3b69ffa0aac7b7878b5a0039e7ab429411" # 许可文件hash
}
maindata={
	"lastnft_id":"NONE",
	"index":0
}

def tool_print(line,text):
	print("\033[7;31;47m Line:"+str(line)+" \033[0m",text)

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

	_path_nft = "nft"
	_path_meta = "meta"
	_nfts= os.listdir(_path_nft)
	for _nft in _nfts: 
		if not os.path.isdir(_nft):
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
				# print(['chia', 'wallet', 'nft', 'mint', '-f', _f, '-i', _i, '-ra', _ra, '-ta', _ta, '-u', _u, '-nh', _nh, '-mu', _mu, '-mh', _mh, '-rp', _rp, '-m', _m])
				_mint=subprocess.run(['chia', 'wallet', 'nft', 'mint', '-f', _f, '-i', _i, '-ra', _ra, '-ta', _ta, '-u', _u, '-nh', _nh, '-mu', _mu, '-mh', _mh, '-lu', _lu, '-lh', _lh, '-rp', _rp, '-m', _m],capture_output=True,text=True)
				# print(_mint.stdout.split("\n"))
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
		_sub=subprocess.run(['chia', 'wallet', 'nft', 'list', '-f', options["f"], '-i', options["i"]],capture_output=True,text=True)
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

if __name__ == "__main__":
	set_hash()
	while nft_mint():
		while not nft_mint_checked():
			time.sleep(5)