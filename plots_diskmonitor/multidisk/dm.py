#! /usr/bin/env python3
import os,sys,time,json,shutil
from multiprocessing import Pool

options={}

def tool_print(type,line,text):
	if type=="warning":
		print("\033[7;43m"+time.strftime("%H:%M:%S ", time.localtime())+str(line)+": "+"\033[0m",text)
	elif type=="important":
		print("\033[7;41m"+time.strftime("%H:%M:%S ", time.localtime())+str(line)+": "+"\033[0m",text)
	else:
		print("\033[7m"+time.strftime("%H:%M:%S ", time.localtime())+str(line)+": "+"\033[0m",text)

def tool_options(type):
	return options[type]["value"]

def plots_diskcheck(disk):
	while True:
		disk_free=shutil.disk_usage(disk["disk_path"])[2]/1024**3
		tool_print("normal",str(sys._getframe().f_lineno)+" "+disk["disk_path"],"Disk Free: "+str(disk_free)+" G")
		if disk_free<disk["disk_size"]:
			plots_remove(disk)
		time.sleep(disk["time_interval"])

def plots_remove(disk):
	if not os.path.exists(disk["file_remove"]):
		tool_print("warning",str(sys._getframe().f_lineno)+" "+disk["disk_path"]+"","file_remove path does not exist")
		return
	else:
		file_list=os.listdir(disk["file_remove"])

	new_filelist= sorted(file_list,  key=lambda x: os.path.getctime(os.path.join(disk["file_remove"], x)),reverse = False)
	for _file in new_filelist:
		for ends in disk["file_endswith"]:
			if _file.endswith(ends.lower()):
				_file_time=time.strftime("%Y%m%d",time.localtime(os.path.getctime(disk["file_remove"]+"/"+_file)))
				if _file_time>= disk["file_time"].split("-")[0] and _file_time<= disk["file_time"].split("-")[1]:
					os.remove(disk["file_remove"]+"/"+_file)
					tool_print("important",str(sys._getframe().f_lineno)+" "+disk["disk_path"],"Removed: "+disk["file_remove"]+"/"+_file)
					return
	tool_print("warning",str(sys._getframe().f_lineno)+" "+disk["disk_path"]+"","no more file can be removed")

if __name__ == "__main__":
	options=json.loads(open("options.json","rb").read())

	disk=tool_options("disk")
	p=Pool(len(disk))
	for i in disk:
		p.apply_async(plots_diskcheck,args=(i,))
		time.sleep(1)
	p.close()
	p.join()