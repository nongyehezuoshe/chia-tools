#! /usr/bin/env python3

import requests,json,time,subprocess,sys,os

options={
	"collectionid":"col1lqdkghxfwj7v0ajka0ww4q5ljkzjh8xgm28h7e3s4sh03smrmxxsn8qcpw",
	"page":60
}
maindata={
	"uris":[]
}

def tool_print(line,text):
	print("\033[7;31;47m Line:"+str(line)+" \033[0m",text)

def get_addrfromspacescan():
	_page=1
	while _page<=options["page"]:
		try:
			r = requests.get("https://api2.spacescan.io/api/nft/collection/"+options["collectionid"]+"?coin=xch&version=1&page="+str(_page)+"&count=40")
			print(r.json()["data"])
			if(len(r.json()["data"])==0):
				break
			if r.status_code==200:
				for i in r.json()["data"]:
					maindata["uris"].append(i["nft_info"]["data_uris"][0].split("/")[3])
					tool_print(sys._getframe().f_lineno,i["nft_info"]["data_uris"][0].split("/")[3])

			_page=_page+1
			time.sleep(10)
			continue
		except Exception as e:
			print(e)

	print(maindata["uris"]);

	path = "nft_minted"
	files= os.listdir(path)
	for file in files: 
		if not os.path.isdir(file):
			if file not in maindata["uris"]:
				with open("not_minted_img","a") as f:
					f.writelines(file+"\n")
					tool_print(sys._getframe().f_lineno,"not_minted: "+file)

if __name__ == "__main__":
	get_addrfromspacescan()
