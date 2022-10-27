#! /usr/bin/env python3

import requests,json,time,subprocess,sys

options={
	"collectionid":"col17jxrr7pwxuhxra86z4gr08tajk3mpr7gjst643a7gv0dc8p8p9aqdcvj30",
	"page":3
}

def tool_print(line,text):
	print("\033[7;31;47m Line:"+str(line)+" \033[0m",text)

def get_addrfromspacescan():
	_page=options["page"]
	while _page:
		try:
			r = requests.get("https://api2.spacescan.io/api/nft/collection/"+options["collectionid"]+"?coin=xch&version=1&page="+str(_page)+"&count=40")
			print(r.json()["data"])
			if r.status_code==200:
				for i in r.json()["data"]:
					# print(i["nft_id"].strip()+" " + i["owner_hash"]+ " " +i["nft_info"]["nft_coin_id"])
					while True:
						tool_print(sys._getframe().f_lineno,i["owner_hash"])
						_xch=subprocess.run(['cdv', 'encode', i["owner_hash"]],capture_output=True,text=True)
						tool_print(sys._getframe().f_lineno,_xch.stdout)
						if _xch.returncode==0:
							with open("airdrop_addr","a") as f:
								f.writelines(i["nft_id"].strip()+" "+_xch.stdout.strip()+"\n")
							break
						time.sleep(5)

			_page=_page-1
			time.sleep(10)
			continue
		except Exception as e:
			print(e)

if __name__ == "__main__":
	get_addrfromspacescan()
