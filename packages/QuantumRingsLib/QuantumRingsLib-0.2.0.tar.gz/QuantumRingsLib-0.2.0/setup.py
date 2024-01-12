import os
from setuptools import setup
from prebuilt_binaries import prebuilt_binary, PrebuiltExtension

ext_module = PrebuiltExtension('C:\\Quantum Rings\\QubitSimulator\\x64\\PythonLib\\QuantumRingsLib.pyd')

setup(
    name='QuantumRingsLib',
    version='0.2.0',
    description='A Quantum Development Library',
    cmdclass={
        'build_ext': prebuilt_binary,
    },
    ext_modules=[ext_module]
)


classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research/Developers',
        'Topic :: Software Development :: Quantum Build Tools',
        'Operating System :: WINDOWS',        
        'Programming Language :: Python :: 3.9',
    ],