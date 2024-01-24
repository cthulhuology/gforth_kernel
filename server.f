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

