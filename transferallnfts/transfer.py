#! /usr/bin/env python3

import os,sys,subprocess,time

maindata={
	"f":"708222379", # 指纹 - 设置指纹指定使用哪个钱包 / fingerprint - Set the fingerprint to specify which wallet  to use
	"i":"3", # 钱包ID / Id of the NFT wallet to use
	"ta":"xch1qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqm6ks6e8mvy", # 目标地址 - 接收方钱包地址 / target-address - Target recipient wallet address
	"m":"0", # 手续费 - 设置交易手续费，单位XCH，默认0 / fee - Set the fees per transaction, in XCH.[default: 0]
}

def tool_print(line,text):
	print("\033[7;31;47m Line:"+str(line)+" \033[0m",text)

def nft_trans(id):
	while True:
		tool_print(sys._getframe().f_lineno,"transfer begain")
		_sub=subprocess.run(['chia', 'wallet', 'nft', 'transfer', '-f', maindata["f"], '-i', maindata["i"], '-m', maindata["m"], '-ni',id[1],"-ta",maindata["ta"]],capture_output=True,text=True)
		print(_sub.stdout.split("\n"))
		if _sub.returncode==0:
			_out=_sub.stdout.split("\n")
			for i in range(0,len(_out)):
				if "NFT transferred successfully" in _out[i]:
					tool_print(sys._getframe().f_lineno,"transfer done")
					return True
		time.sleep(5)

def nft_get_current():
	while True:
		_sub=subprocess.run(['chia', 'wallet', 'nft', 'list', '-f', maindata["f"], '-i', maindata["i"]],capture_output=True,text=True)
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

def nft_writefile(id):
	with open("nft_transed","a") as f:
		f.writelines(id[0]+","+id[1]+"\n")
		tool_print(sys._getframe().f_lineno,id[0]+","+id[1])

def fn_main():
	tool_print(sys._getframe().f_lineno,"START")
	while True:
		_current_nft=nft_get_current()
		if _current_nft[1]!="NONE":
			nft_trans(_current_nft)
			while True:
				_check_nft=nft_get_current()
				tool_print(sys._getframe().f_lineno,_check_nft[0]+","+_current_nft[0])
				if _current_nft[0]!=_check_nft[0]:
					tool_print(sys._getframe().f_lineno,"!")
					nft_writefile(_current_nft)
					_current_nft=_check_nft
					break
				else:
					tool_print(sys._getframe().f_lineno,"=")
					time.sleep(5)
		else:
			break


if __name__ == "__main__":
	fn_main()
