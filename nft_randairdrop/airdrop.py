#! /usr/bin/env python3
import sys,subprocess,random,os

options={
	"chia_cmd":"chia", # chia路径 /chia cmd location
	"f":"708222379", # 
	"i":"4", #
	"m":"0" # 手续费 | fee
}

maindata={
	"transfer_id":"",
	"addr_index":""
}

def tool_print(line,text):
	print("\033[7;31;47m"+str(line)+" \033[0m",text)

def get_allnfts():
	tool_print(str(sys._getframe().f_lineno)+" "+"get all nft ids","...")
	_sub=subprocess.run([options["chia_cmd"], 'wallet', 'nft', 'list', '-f', options["f"], '-i', options["i"]],capture_output=True,text=True)
	_allnfts=[]
	if _sub.returncode==0 :
		_out=_sub.stdout.split("\nNFT ident")
		for i in _out:
			_list=i.split("\n")
			_nft=[]
			for ii in _list:
				# _nft=[]
				print(ii)
				if ii.split(":")[0].strip()=="Current NFT coin ID":
					_nft.append(ii.split(":")[1].strip())
				if ii.split(":")[0].strip()=="NFT is pending for a transaction" and ii.split(":")[1].strip()=="True":
					_nft=[]
					break
			if len(_nft)>0:
				_allnfts.append(_nft)
	print(_allnfts)
	return _allnfts

def get_rand_addr():
	_len=len(open("input_data.csv").readlines())
	_rand=random.randint(0,_len-1)
	maindata["addr_index"]=_rand
	_lines=open("input_data.csv").readlines()
	return _lines[_rand].strip()

def get_rand_nft():
	_allnfts=get_allnfts()
	if len(_allnfts)<1:
		return False
	_id=random.randint(0,len(_allnfts)-1)
	return _allnfts[_id]

def nft_trans(id,addr):
	tool_print(str(sys._getframe().f_lineno)+" "+"random airdrop id:",str(id))
	tool_print(str(sys._getframe().f_lineno)+" "+"random airdrop addr:",str(addr))
	while True:
		tool_print(sys._getframe().f_lineno,"transfer begain")
		_sub=subprocess.run(['chia', 'wallet', 'nft', 'transfer', '-f', options["f"], '-i', options["i"], '-m', options["m"], '-ni',str(id),"-ta",str(addr)],capture_output=True,text=True)
		print(_sub.stdout.split("\n"))
		if _sub.returncode==0:
			_out=_sub.stdout.split("\n")
			for i in range(0,len(_out)):
				if "NFT transferred successfully" in _out[i]:
					tool_print(sys._getframe().f_lineno,"transfer done")
					maindata["transfer_id"]=id
					return True
		time.sleep(5)

def nft_trans_checked():
	tool_print(str(sys._getframe().f_lineno)+" "+"transfer checking","...")
	while True:
		_sub=subprocess.run([options["chia_cmd"], 'wallet', 'nft', 'list', '-f', options["f"], '-i', options["i"]],capture_output=True,text=True)
		_allnfts=[]
		if _sub.returncode==0 :
			_out=_sub.stdout.split("\nNFT ident")
			for i in _out:
				_list=i.split("\n")
				_nft=[]
				for ii in _list:
					print(ii)
					if ii.split(":")[0].strip()=="Current NFT coin ID":
						if ii.split(":")[1].strip()==maindata["transfer_id"]:
							return False
							break
			file_update()
			return True
		time.sleep(5)

def file_update():
	open("input_data_new.csv", 'w').close()
	_lines=open("input_data.csv").readlines()
	_newdata=open("input_data_new.csv","a")
	for line in range(0,len(_lines)):
		if line!=maindata["addr_index"]:
			_newdata.writelines(_lines[line].strip()+"\n")
	os.rename("input_data_new.csv", "input_data.csv")

def nft_airdrop():
	_addr=get_rand_addr()
	_nft=get_rand_nft()
	if _addr and _nft:
		nft_trans(_nft,_addr)
		return True
	else:
		return False

if __name__ == "__main__":
	while nft_airdrop():
		time.sleep(5)
		while not nft_trans_checked():
			time.sleep(5)