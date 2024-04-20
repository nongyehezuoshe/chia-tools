#! /usr/bin/env python3

import requests,json,time,subprocess,sys

options={
	"collectionid":"col14v8xqlfkkjqdxudecr2p9y6363dec0hzl0lucnufv92u26cm38yqrlf2wy",
	"page":10
}

def tool_print(line,text):
	print("\033[7;31;47m Line:"+str(line)+" \033[0m",text)

def get_addrfromspacescan():
	_page=options["page"]
	for x in range(_page):
		try:
			r = requests.post("https://api-fin.spacescan.io/collection/nfts/"+options["collectionid"]+"?version=0.1.0&network=xch",json={"count":100,"page":x})

			print(r.json()["data"])
			if r.status_code==200:
				with open("airdrop_addr.csv","a") as f:
					for i in r.json()["data"]:
						f.writelines(i["nft_id"].strip()+","+i["owner"]["address"].strip()+"\n")

			time.sleep(2)
			continue
		except Exception as e:
			print(e)

if __name__ == "__main__":
	get_addrfromspacescan()
