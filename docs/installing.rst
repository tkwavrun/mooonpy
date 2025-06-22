Using pip from PyPi
-------------------

Install the ``mooonpy`` package (or add it to your ``requirements.txt`` file):

.. code:: console

    $ pip install mooonpy
	
.. note::

   This is a place holder until mooonpy gets published to PyPi, so ``pip install mooonpy`` will not work!
	
	
Using pip locally
-----------------

Install the ``mooonpy`` package locally in mooonpy/src/ directory:

Example Directory:
  
  .. code:: console
  
    mooonpy/src$ pwd
    GitHub/mooonpy/src
  
    mooonpy/src$ ls
    mooonpy
  
    mooonpy/src$ tree -L 1
    .
    └── mooonpy
  

Windows OS:

  .. code:: console

    $ python -m pip install -e .
	
Anaconda PowerShell:
  
  .. code:: console

    $ pip install -e .
	
.. note::

   Support for conda and Linux pip still not supported!
   
Dependency List
---------------

Mooonpy has numerous required dependencies. The following lists them all (as of July 2025).

  - Required Python package build time:
     #. ``pip``
	 
  - Required Sphinx documentation build time:
     #. ``sphinx``
     #. ``sphinx_rtd_theme``
     #. ``ghp-import``
     #. ``matplotlib``
  
  - Required run time:
     #. ``numpy``
     #. ``scipy``
     #. ``matplotlib``
   
Simple Python example
---------------------

.. code:: python

    import mooonpy
	
    molecule = mooonpy.molspace('detda.mol2')
    molecule.atoms.shift(x=5, y=10, z=30)



