from ipykernel.kernelapp import IPKernelApp
from .mikrokosmoskernel import MikrokosmosKernel
IPKernelApp.launch_instance(kernel_class=MikrokosmosKernel)