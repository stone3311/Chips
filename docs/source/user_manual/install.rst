Installation
============

Download (github)
-----------------

You can download the 
`source <https://github.com/benfre/Chips/archive/master.zip>`_ 
from the
`GitHub <https://github.com/benfre/Chips>`_ 
homepage. Alternatively clone the project using git::

    ~$ git clone --recursive https://github.com/benfre/Chips.git

Install from github
-------------------

::

        $ cd Chips
        $ sudo python3 setup.py install


Install from PyPi
-----------------

::

        $ pip3 install chips-python


Icarus Verilog
--------------

Chips can automatically simulate the verilog it generates, to simulate verilog
you will need the `Icarus Verilog <http://iverilog.icarus.com/>`_
        simulator. This will need to be installed in your command path.

C Preprocessor
--------------

Chips uses an external C processor. Make sure you have a c preprocessor `cpp`
installed in your path

Other packages
--------------

While not strictly speaking dependencies, you may want to install the following
packages to use all the libraries and examples:

+ numpy
+ scipy
+ matplotlib
+ pil
+ wxpython

