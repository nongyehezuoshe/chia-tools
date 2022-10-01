#! /usr/bin/env python3

import os,sys,subprocess

options={
	"f":"708222379", # fingerprint / 指纹
	"i":"4", # wallet_id / nft钱包ID
}
maindata={
	"ra":[]
}

def tool_print(line,text):
	print("\033[7;31;47m Line:"+str(line)+" \033[0m",text)

def ra_writefile(ra):
	with open("ra_addr","a") as f:
		f.writelines(ra+"\n")

def get_allra():
	tool_print(str(sys._getframe().f_lineno)+" "+"get all ra","...")
	_sub=subprocess.run(['chia', 'wallet', 'nft', 'list', '-f', options["f"], '-i', options["i"]],capture_output=True,text=True)
	_value=["",""]
	if _sub.returncode==0 :
		_out=_sub.stdout.split("\nNFT ident")
		for i in _out:
			_list=i.split("\n")
			for ii in _list:
				if "Royalty puzhash:" in ii:
					_ra=ii.split("Royalty puzhash:")[1].strip()
					if _ra not in maindata["ra"]:
						maindata["ra"].append(_ra)
						ra_writefile(_ra)
						tool_print(str(sys._getframe().f_lineno)+" "+"find a new ra:",_ra)

	print(maindata)

if __name__ == "__main__":
	get_allra()