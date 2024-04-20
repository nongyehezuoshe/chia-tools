#! /usr/bin/env python3

import hashlib,os,csv,sys,subprocess,time

options={
	"f":"708222379", # fingerprint / 指纹
	"i":"4", # wallet_id / nft钱包ID
	"m":"0", # A fee to add to the offer when it gets taken / 手续费
	"r":"--request 1:1" # A wallet id of an asset to receive and the amount you wish to receive (formatted like wallet_id:amount) /offer文件对应的请求xch的金额，格式：xch钱包id:xch金额, 如果请求的是多个CAT，则再增加相应的--request即可（--request 1:1 --request 2:1）
}
maindata={
	"allnfts":[]
}

def tool_print(line,text):
	print("\033[7;31;47m Line:"+str(line)+" \033[0m",text)

def set_offer(nftid):
	tool_print(str(sys._getframe().f_lineno)+" "+"generating offer file","...")
	if not os.path.exists("offers"):
		os.makedirs("offers")
	_f=options["f"]
	_i=options["i"]
	_m=options["m"]
	_o=nftid+":1"
	_r=options["r"]
	_p=nftid+"_x_"+str(_r.split(":")[1])+".offer"

	while True:
		_offer=subprocess.run(['chia', 'wallet', 'make_offer', '-f', _f, '-m', _m, '-p', 'offers/'+_p, '-o', _o, _r],capture_output=True,text=True,input="y\ny")
		if _offer.returncode==0 :
			print(_offer.stdout)
			break
	return

def get_allnfts():
	tool_print(str(sys._getframe().f_lineno)+" "+"get all nft ids","...")
	_sub=subprocess.run(['chia', 'wallet', 'nft', 'list', '-f', options["f"], '-i', options["i"]],capture_output=True,text=True)
	_value=["",""]
	if _sub.returncode==0 :
		_out=_sub.stdout.split("\nNFT ident")
		for i in _out:
			_list=i.split("\n")
			if _list[0]:
				_nft=_list[0].split()[1].strip()
				maindata["allnfts"].append(_nft)
	print(maindata)

if __name__ == "__main__":
	get_allnfts()
	for i in maindata["allnfts"]:
		set_offer(i)