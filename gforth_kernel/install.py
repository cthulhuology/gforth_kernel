import argparse
import json
import os
import sys
import shutil

from jupyter_client.kernelspec import KernelSpecManager
from tempfile import TemporaryDirectory

kernel_json = {
	"argv":[sys.executable,"-m","gforth_kernel", "-f", "{connection_file}"],
	"display_name":"GForth",
	"language":"Forth",
	"name": "Forth"
}

def install_my_kernel_spec(user=True, prefix=None):
	with TemporaryDirectory() as td:
		os.chmod(td,0o755)
		with open(os.path.join(td,'kernel.json'),'w') as f:
			json.dump(kernel_json,f,sort_keys=True)
		print('Installing Jupyter kernel spec')
		cur_path = os.path.dirname(os.path.realpath(__file__))
		for logo in [ "logo-32x32.png","logo-64x64.png"]:
			try:
				shutil.copy(os.path.join(cur_path,logo),td)
			except FileNotFoundError:
				print("Custom logo files not found. Default logos will be used.")
		KernelSpecManager().install_kernel_spec(td,'gforth',user=user,prefix=prefix)

def _is_root():
	try:
		return os.geteuid() ==0
	except AttributeError:
		return False


def main(argv=None):
	ap = argparse.ArgumentParser()
	ap.add_argument('--user', action='store_true',help='Install to the per-user kernels registry')
	ap.add_argument('--sys-prefix', action='store_true',help='Install to a sys.prefix. conda/venv')
	ap.add_argument('--prefix',action='store_true',help='Install to given prefix')
	args = ap.parse_args(argv)

	if args.sys_prefix:
		args.prefix = sys_prefix
	if not args.prefix and not __is_root():
		args.user = True

	install_my_kernel_spec(user=args.user, prefix=args.prefix)


if __name__ == '__main__':
	main()
