#! /usr/bin/env python3

import os,sys,subprocess,time

options={
	"f":"708222379", # Fingerprint
	"i":"4", # wallet ID
	"ta":"xch1qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqm6ks6e8mvy" # traget/burn address
}

maindata={
	"allnfts":[]
}

def tool_print(line,text):
	print("\033[7;31;47m "+str(line)+" \033[0m",text)

def nft_trans(id):
	while True:
		tool_print(sys._getframe().f_lineno,"transfer begain")
		_sub=subprocess.run(['chia', 'wallet', 'nft', 'transfer', '-f', options["f"], '-i', options["i"], '-ni',id[1],"-ta",options["ta"]],capture_output=True,text=True)
		# print(_sub.stdout.split("\n"))
		if _sub.returncode==0:
			_out=_sub.stdout.split("\n")
			for i in range(0,len(_out)):
				if "NFT transferred successfully" in _out[i]:
					tool_print(sys._getframe().f_lineno,"transfer done")
					return True
		time.sleep(5)

def nft_getall():
	tool_print(sys._getframe().f_lineno,"get all nfts...")
	while True:
		_sub=subprocess.run(['chia', 'wallet', 'nft', 'list', '-f', options["f"], '-i', options["i"]],capture_output=True,text=True)
		_value=["","",""]

		if _sub.returncode==0 :
			_out=_sub.stdout.split("\nNFT ident")
			if len(_out)<2:
				_value=["NONE","NONE","NONE"]
				maindata["allnfts"].append(_value)
				return 
			for i in _out:
				_list=i.split("\n")
				for ii in _list:
					if "ifier:" in ii:
						# print(ii.split())
						_value[0]=ii.split()[1].strip()
					if "Current NFT coin ID:" in ii:
						# print(ii.split("Current NFT coin ID:"))
						_value[1]=ii.split("Current NFT coin ID:")[1].strip()
					if "NFT is pending for a transaction:" in ii:
						_value[2]=ii.split("NFT is pending for a transaction:")[1].strip()
					if _value[0] and _value[1] and _value[2]:
						maindata["allnfts"].append(_value)
						tool_print(str(sys._getframe().f_lineno)+" found nft:",str(_value[0]))
						break;
			return
		time.sleep(10)

def nft_writefile(id):
	with open("nft_transed","a") as f:
		f.writelines(id[0]+","+id[1]+"\n")
		tool_print(sys._getframe().f_lineno,id[0]+","+id[1])

def fn_main():
	tool_print(sys._getframe().f_lineno,"START")
	nft_getall()
	for i in maindata["allnfts"]:
		if i[1]!="NONE" and i[2]=="False":
			nft_trans(i)
			nft_writefile(i)
			time.sleep(1)
		else:
			tool_print(sys._getframe().f_lineno,"next...")

if __name__ == "__main__":
	fn_main()
	# nft_getall()