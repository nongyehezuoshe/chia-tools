#! /usr/bin/env python3
import os,sys,subprocess,json,time

options={}

def tool_print(line,text):
	print("\033[7m"+time.strftime("%H:%M:%S ", time.localtime())+str(line)+": "+"\033[0m",text)

def plots_check():
	_locations=options["plots_path"]["value"]
	_chia=options["chia_path"]["value"]
	print(_chia)
	for local in _locations:
		_path=os.path.abspath(os.path.expanduser(os.path.expandvars(local)))
		open(os.path.join(_path,'plots_check.csv'), 'w').close()
		_file=open(os.path.join(_path,'plots_check.csv'),"a")
		_dir= os.listdir(_path)
		for _plot in _dir: 
			if not os.path.isdir(_plot) and _plot.endswith("plot"):
				tool_print(str(sys._getframe().f_lineno)+" "+"checking",os.path.join( _path,_plot))
				_sub=subprocess.run([_chia, 'plots', 'check', '-g',os.path.join( _path,_plot)],capture_output=True,text=True)
				# print(_sub)
				_out=_sub.stderr.split('Proofs')
				if len(_out)>1:
					_out=_sub.stderr.split("Proofs")[1].split(", ")[1].split("\n")[0].split("\x1b[0m")[0].strip()
					tool_print(str(sys._getframe().f_lineno)+" "+"checked",_out)
					_file.writelines(_plot+","+_out+"\n")
				else:
					_file.writelines(_plot+","+"err"+"\n")
					continue

if __name__ == "__main__":
	options=json.loads(open("options.json","rb").read())
	plots_check()