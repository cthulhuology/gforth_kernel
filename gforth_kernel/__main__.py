from ipykernel.kernelapp import IPKernelApp
from . import GForthKernel

IPKernelApp.launch_instance(kernel_class=GForthKernel)
