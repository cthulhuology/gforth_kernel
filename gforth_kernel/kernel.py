from ipykernel.kernelbase import Kernel
from subprocess import Popen
from ipykernel.kernelapp import IPKernelApp
from sys import stderr
server = """
\ this is gforth code we will run to redirect stdin & stdout (and maybe stderr)
\ we're using named sockets for output, mkdir -p /var/forth && mkfifo /var/forth/{in,out,err}
: forth/in s" /var/forth/in" ;
: forth/out s" /var/forth/out" ;
: forth/err s" /var/forth/err" ;

: print-starting cr ." starting gforth server" cr ;

\ this server reads from our named fifo /var/forth/in and writes to /var/forth/out
\ outfile-id is a gforth 
: server
	['] print-starting stderr outfile-execute
	BEGIN
		forth/in r/o open-file ?dup 0=
	WHILE
		forth/out w/o open-file throw to outfile-id
		['] include-file  				\ consumes the forth/in content
		catch ?dup IF					\ if we errr
			<# DoError clearstacks			\ do the converted errorno and clear
		ELSE
			." ok" cr				\ otherwise print ok
			outfile-id flush-file throw		\ and flush the output
		THEN
		outfile-id stdout to outfile-id close-file throw \ reset stdout and close out
	REPEAT
	bye ;

server
"""

class GForthKernel(Kernel):
	"""Forth server inspired by the work of Ulrich Hoffmann uho@xlerb.de, and Jonathan Frederic"""

	implementation = 'Gforth'
	implementation_version = '1.0'
	language_version = "1.0"
	language_info = {
		'name' : 'forth',
		'mimetype': 'text/plain',
		'file_extension' : '.f'
	}
	banner = "GForth"
	def do_execute(self,  code, silent, store_history=True, user_expressions=None, allow_stdin=False):
		with open("/var/forth/in","wb") as forth_in:
			print(f"executing: { code }", file=stderr)
			forth_in.write(bytes(code,"utf-8"))
			forth_in.write(bytes("\n","utf-8"))
			forth_in.flush()
		with open("/var/forth/out","rb") as forth_out:
			content = { 'name': 'stdout', 'text': forth_out.read().decode('utf-8') }
			print(f"resp: { content }",file=stderr)
			self.send_response(self.iopub_socket, 'stream', content)
		return { 'status': 'ok', 'execution_count': self.execution_count, 'payload': [], 'user_expressions': {}}	

if __name__ == '__main__':
	forth = Popen(["gforth"],stdin=PIPE,stdout=PIPE,close_fds=True)
	print(f"sending {server} to gforth",file=stderr)
	forth.stdin.write(server)
	forth.stdin.flush()
	IPKernelApp.launch_instance(kernel_class=GforthKernel)
