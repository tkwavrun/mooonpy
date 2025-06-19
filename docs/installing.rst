Installation
============

How to install and use the theme
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

   This is a place holder until mooonpy gets published to PyPi ``pip install mooonpy`` will not work


.. _howto_upgrade:

How to upgrade
--------------

Adding ``sphinx-rtd-theme`` to your project's dependencies will make pip install the latest compatible version of the theme.

If you want to test a **pre-release**, you need to be explicit about the version you specify.
Otherwise, pip will ignore pre-releases. Add for instance ``sphinx-rtd-theme==1.1.0b3`` to test a pre-release.

