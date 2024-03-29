.. imgfilt documentation master file, created by
   sphinx-quickstart on Sun Oct  1 12:04:29 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

imgfilt Documentation
=====================

.. toctree::
   :maxdepth: 2
   :caption: Contents:
   
   self
   /api.rst
   /examples.rst
   /requirements.rst


Why did you write this?
-----------------------
I've been working on some code to procedurally generate images and
video. It is getting pretty bloated, so I thought I could carve the
the filters functions into its own module. For that reason, I'm not
sure if this is useful to anyone else, but I figured I'd put it out
there just in case.


How do I run the code?
----------------------
The best way to get started is to clone the repository to your local
system and take a look at the examples in the example directory.


Is it portable?
---------------
It should be, but I've not tested that.


Can I install this package from pip?
------------------------------------
Yes, but imgfilt is not currently available through PyPI. You will
need to clone the repository to the system you want to install
imgfilt on and run the following::

    pip install path/to/local/copy

Replace `path/to/local/copy` with the path for your local clone of
this repository.


How do I run the tests?
-----------------------
The `Makefile` in the root of the repository is set up to simplify
testing. To run just the unit tests::

    make test

To run the verbose version of the unit tests::

    make testv

To run the full suite of tests and checks::

    make pre


How do I contribute?
--------------------
At this time, this is code is really just me exploring and learning.
I've made it available in case it helps anyone else, but I'm not really
intending to turn this into anything other than a personal project.

That said, if other people do find it useful and start using it, I'll
reconsider. If you do use it and see something you want changed or
added, go ahead and open an issue. If anyone ever does that, I'll
figure out how to handle it.


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
