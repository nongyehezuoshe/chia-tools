#! /usr/bin/env python3

import requests,json,time,subprocess,sys

options={
	"collectionid":"col14swfyczt4xdpd6skneqw0wtf76fee78lq7jyuy2f2e8xgythjsysz6lh49",
	"page":1
}

def tool_print(line,text):
	print("\033[7;31;47m Line:"+str(line)+" \033[0m",text)

def get_id():
	open('lastid.csv', 'w').close()
	_page=options["page"]
	while _page:
		try:
			r = requests.get("https://api2.spacescan.io/api/nft/collection/"+options["collectionid"]+"?coin=xch&version=1&page="+str(_page)+"&count=40")
			print(r.json()["data"])
			if r.status_code==200:
				for i in r.json()["data"]:
					tool_print(sys._getframe().f_lineno,i["nft_id"].strip())
					with open("lastid.csv","a") as f:
						f.writelines(i["meta_info"]["name"].split("#")[1].strip()+","+i["nft_id"].strip()+"\n")

			_page=_page-1
			time.sleep(10)
			continue
		except Exception as e:
			print(e)

if __name__ == "__main__":
	get_id()