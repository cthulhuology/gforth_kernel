gforth_kernel
-------------

This is a quick and dirty implementation of a gforth kernel for jupyter notebooks that has a few problems but works.


Getting Started
---------------

To use this:

* install gforth
* install jupyter (should work with python3.10+)
* sudo mkdir -p /var/forth
* sudo mkfifo /var/forth/{in,out}
* sudo chown -R your_user:your_group /var/forth
* gforth server.f
* jupyter notebook


Credits
-------

The forth server is based on the work of Ulrich Hoffmann uho@xlerb.de
and kernel rewrite was inspired by the work of Jonathan Frederic
All of the code was typed by hand, nothing copied nothing pasted.

