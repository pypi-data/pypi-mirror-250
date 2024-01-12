
.. _minimum-system-requirements:

Minimum System Requirements
---------------------------

A system with a configuration better than the minimum requirements is advised. 
Lower configurations may affect the number of qubits that can be supported and
may perform poorly.

-  Operating system:

   -  Preferred: Windows 11 Pro

-  64-bit x86 CPU (14 cores 20 logical processors)

-  32 GB Installed physical memory ( 64 GB Recommended )

-  18 GB Available physical memory

-  64-bit Python version 3.9


============
Installation
============

The Quantum Rings SDK can be installed directly using pip. 
Many users find Anaconda a good way to install the Quantum Rings SDK.
From Anaconda, select a Python 3.9 channel and launch `CMD.exe Prompt` to go to the
command prompt and execute the following command.

.. code-block:: console

    pip install QuantumRingsLib


If you do not have a Python 3.9 or higher channel, select `Environments` from the left channel, `+ Create` button from the menu bar
at the bottom and select Python 3.9 from the `Create New Environment` dialog.



Quantum Rings SDK requires a 64-bit version of Python 3.9.


=====
Usage
=====

Obtain your account name and token from the Quantum Rings team. You can then use them to create the backend for execution.
You can follow the reference code below for further information:


.. code-block:: python
        
    import QuantumRingsLib
    from QuantumRingsLib import QuantumRegister, AncillaRegister, ClassicalRegister, QuantumCircuit
    from QuantumRingsLib import QuantumRingsProvider
    from QuantumRingsLib import job_monitor
    from QuantumRingsLib import JobStatus
    from matplotlib import pyplot as plt
    import numpy as np

    provider = QuantumRingsProvider(token =<YOUR_TOKEN_HERE>, name=<YOUR_ACCOUNT_NAME_HERE>)
    backend = provider.get_backend("scarlet_quantum_rings")
    shots = 100

    provider.active_account()



==================
Executing the Code
==================

You can execute the code in the backend as illustrated below and setup a job monitor to watch for completion. The code is executed in a background thread so
you can use your system normally.

*Using job_monitor function*

.. code-block:: python

    job = backend.run(qc, shots)
    job_monitor(job)
    result = job.result()
    counts = result.get_counts()
    print (counts)


*Using wait_for_final_state function*

.. code-block:: python

    def jobCallback(job_id, state, job):
        #print("Job Status: ", state)
        pass

    # Execute the circuit
    job = backend.run(qc, shots)
    job.wait_for_final_state(0, 5, jobCallback)
    counts = job.result().get_counts() 


==========================
Version 0.2.0 Known Issues
==========================


* At times, the :math:`cs` and :math:`csdg` gates may generate errors.
* qasm2 importer does not process include statements.


