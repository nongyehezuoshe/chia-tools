#! /usr/bin/env python3
import os,sys,subprocess,time,json,shutil

options={}

def tool_print(line,text):
	print("\033[7m"+time.strftime("%H:%M:%S ", time.localtime())+str(line)+": "+"\033[0m",text)

def plots_check():
	tool_print(str(sys._getframe().f_lineno)+" "+"START","...")
	_path=os.path.abspath(os.path.expanduser(os.path.expandvars(options["plots_path"])))
	_dir=os.listdir(_path)
	for _plot in _dir: 
		if not os.path.isdir(_plot) and _plot.endswith("plot"):
			tool_print(str(sys._getframe().f_lineno)+" "+"checking",_plot)
			_sub=subprocess.run(['chia', 'plots', 'check', '-g', _path+'/'+_plot],capture_output=True,text=True)
			_out=_sub.stderr.split('Proofs')
			if len(_out)>1:
				_out=_sub.stderr.split("Proofs")[1].split(", ")[1].split("\n")[0].split("\x1b[0m")[0].strip()
				tool_print(str(sys._getframe().f_lineno)+" "+"checked",_out)
				if float(_out)>=options["ratio"]:
					try:
						tool_print(str(sys._getframe().f_lineno)+" "+"Moving","...")
						shutil.copy2(_path+"/"+_plot,options["plots_path_target"]+"/"+_plot)
						os.remove(_path+"/"+_plot)
						tool_print(str(sys._getframe().f_lineno)+" "+"Moved",_plot)
					except Exception as err:
						print(err)
				else:
					os.remove(_path+"/"+_plot)
					tool_print(str(sys._getframe().f_lineno)+" "+"deleted",_plot)
			else:
				os.remove(_path+"/"+_plot)
				tool_print(str(sys._getframe().f_lineno)+" "+"deleted",_plot)
				continue

if __name__ == "__main__":
	while True:
		options=json.loads(open("options.json").read())
		plots_check()
		time.sleep(10)