How to install mooonpy using pip
--------------------------------

Install the ``mooonpy`` package (or add it to your ``requirements.txt`` file):

.. code:: console

    $ pip install mooonpy

After mooonpy is installed you can load mooonpy as:

.. code:: python

    import mooonpy
	
    molecule = mooonpy.molspace('detda.mol2')
    molecule.atoms.shift(x=5, y=10, z=30)

.. note::

   This is a place holder until mooonpy gets published to PyPi, so ``pip install mooonpy`` will not work!

