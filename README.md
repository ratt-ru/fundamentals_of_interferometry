# Fundamentals of Radio Interferometry

An ipython notebook-based book on the Fundamentals of Radio Interferometry. This is a community effort with the aim to be constantly improving and adding to the content in an effort to make interferometry as accessible as possible.  Please contribute, whether it is content, editing, or even suggestions.

This book is currently being used to teach the NASSP 2016 [Fundamentals of Radio Interferometry](https://griffinfoster.github.io/fundamentals_of_interferometry/) Masters' Course.

## Data Files

There are additional large files (> 1MB), mainly FITS images, which are needed for some of the sections, these can be downloaded [here](http://www.mth.uct.ac.za/~siphelo/admin/interferometry/data/fundamentals_fits.tar.gz) ([alt](https://www.dropbox.com/s/n3jyiajytwuldpu/fundamentals_fits.tar.gz?dl=0)), the original simulated KAT-7 measurement sets can be downloaded [here](http://www.mth.uct.ac.za/~siphelo/admin/interferometry/data/simulated_KAT-7_ms.tar.gz) ([alt](https://www.dropbox.com/s/kb3p2mthei8dgl9/simulated_KAT-7_ms.tar.gz?dl=0)). These are tarballs which should be extracted in the data directory.

```
cd fundamentals_of_interferometry/data/
tar xvzf fundamentals_fits.tar.gz
cd simulated_kat_7_vis
tar xvzf simulated_KAT-7_ms.tar.gz
```

## Style Guide

In order to keep the content consistent across sections we have written a [style guide](https://github.com/griffinfoster/fundamentals_of_interferometry/blob/master/0_Introduction/0_introduction.ipynb) in the introduction. Additionally, we have an [editing guide](https://github.com/griffinfoster/fundamentals_of_interferometry/blob/master/0_Introduction/editing_guide.ipynb) for those who wish to suggest changes and edits to the current content.

## Setup contributor virtualenv

If you would like to contribute to notebooks it is useful to setup a python virtual environment to ensure your environment is consistent with other contributors. This section provides a guide for how to do this in an Ubuntu system (tested on 14.04), other systems should work with slight modifications.

Currently we are using pip to install packages, the most important package versions are:

* pip 7.1.2
* python 2.7.6
* numpy 1.10.1
* matplotlib 1.5.0
* scipy 0.16.1
* ipython 4.2.0
* astropy 1.1.1
* aplpy 1.0
* ipywidgets 4.1.1
* healpy 1.10.3
* ephem 3.7.6.0

This guide was developed from these references:

* <http://jeffskinnerbox.me/posts/2013/Oct/06/ipython-notebook-in-virtualenv/>
* <http://iamzed.com/2009/05/07/a-primer-on-virtualenv/>
* <http://jonathanchu.is/posts/virtualenv-and-pip-basics/>
* <https://warpedtimes.wordpress.com/2012/09/23/a-tutorial-on-virtualenv-to-isolate-python-installations/>

Before setting up a virtual environment there are a few system level libraries which need to be installed

```
sudo apt-get install libpng-dev libncurses5-dev
```

To setup a clean environment to run our ipython-notebook standard system, start by making sure virtualenv is installed on your system. Run:

```
$ which pip
```

If there is no output, then you need to install pip:

```
$ sudo easy_install pip
```

Next, run:

```
$ which virtualenv
```

If there is no output, then you need to install virtualenv:

```
$ sudo apt-get install python-virtualenv
$ sudo pip install virtualenvwrapper
```

Once you have all the basic packages installed you can create a vitrualenv, I tend to keep all my virtualenvs in one place, e.g. a .virtualenv directory in my home directory

```
$ cd .virtualenv
$ virtualenv --no-site-packages fundamentals
```

This creates a virtualenv called fundamentals in the .virtualenv directory which is completely independent of any system site-packages, to active the virtualenv run the activation script

```
$ cd fundamentals
$ source bin/activate
```

First, lets clone the repository from github, you should use your own forked version if you want to make changes

```
$ git clone https://github.com/[username]/fundamentals_of_interferometry.git
```

If you just want to run the notebooks interactively you can just use this repository.

```
$ git clone https://github.com/griffinfoster/fundamentals_of_interferometry.git
```

Now this is a completely clean environment, there are no python packages installed, we need to set those up. There are two ways to do this, first is by running the following pip install commands, the other is by installing from the requirements file included in the this repository. I recommend the requirements file as it contains current version information (but, this may fail due to the package ordering, then you will need to try the to install packages manually, described below). The file is in the main directory of the repository or can be downloaded [here](https://raw.githubusercontent.com/griffinfoster/fundamentals_of_interferometry/master/requirements.txt). This will take a bit of time to setup, I recommend a tea break.

```
$ pip install --upgrade pip
$ pip install -r [path to file]/requirements.txt
```

or

```
$ pip install --upgrade pip
$ pip install yolk
$ pip install numpy
$ pip install matplotlib
$ pip install scipy
$ pip install ipython[all]
$ pip install --no-deps astropy
$ pip install aplpy
$ pip install healpy
$ pip install ipywidgets
$ pip install ephem
```

We are now ready to start the ipython notebook server:

```
$ cd fundamentals_of_interferometry
$ jupyter notebook
```

To kill the server, type ctrl-c at the terminal and input y. To deactivate the virtualenv and return to your normal environment run:

```
$ deactivate
```

In the future, when you wish to return to the virtualenv, change to the fundamentals directory and run:

```
$ source bin/activate
```

### Data

We have tried to not include too many large files (e.g. FITS, measurement sets) into the repository to keep the size small. In order to fully utilize the notebooks please download the data sets [here](https://www.dropbox.com/s/n3jyiajytwuldpu/fundamentals_fits.tar.gz?dl=0), and the simulated KAT-7 measurement sets [here](https://www.dropbox.com/s/kb3p2mthei8dgl9/simulated_KAT-7_ms.tar.gz?dl=0).

In the root directory of the repository there is a ``data/`` directory, this is where we want to decompress the data into. To do so:

```
$ cd [fundamentals root]/data/
$ mv [location of download]/fundamentals_fits.tar.gz .
$ tar xvzf fundamentals_fits.tar.gz
$ cd simulated_kat_7_vis/
$ mv [location of download]/simulated_KAT-7_ms.tar.gz .
$ tar xvzf simulated_KAT-7_ms.tar.gz
```

### Ubuntu 12.04 Issues

The system setuptools/distribute (0.6.24) is not new enough and needs to be updated with easy_install

```
easy_install -U distribute
```

### Ubuntu 14.04 Issues

Matplotlib and numpy have many system-level dependencies, you may be required to install package before the virtualenv setup will work.

#### freetype

If there is a freetype related error, try:

```
sudo apt-get install libfreetype6-dev
```

#### fortran

If there is a fortran related error, try:

```
sudo apt-get install gfortran
```

### Contributors

* Alexander Akoto-Danso ([@akotodanso](https://github.com/akotodanso))
* Marcellin Atemkeng ([@atemkeng](https://github.com/atemkeng))
* Landman Bester ([@landmanbester](https://github.com/landmanbester))
* Tariq Blecher ([@TariqBlecher](https://github.com/TariqBlecher))
* Roger Deane ([@rdeane](https://github.com/rdeane))
* Griffin Foster ([@griffinfoster](https://github.com/griffinfoster))
* Julien Girard ([@JulienNGirard](https://github.com/JulienNGirard))
* Trienko Grobler ([@Trienko](https://github.com/Trienko))
* Benna Hugo ([@bennahugo](https://github.com/bennahugo))
* Gyula (Josh) Jozsa ([@gigjozsa](https://github.com/gigjozsa))
* Ermias Abebe Kassaye ([@Ermiasabebe](https://github.com/Ermiasabebe))
* Jonathan Kenyon ([@JSKenyon](https://github.com/JSKenyon))
* Sphesihle Makhathini ([@SpheMakh](https://github.com/SpheMakh))
* Modhurita Mitra ([@modhurita](https://github.com/modhurita))
* Gijs Molenaar ([@gijzelaerr](https://github.com/gijzelaerr))
* Jared Norman ([@jfunction](https://github.com/jfunction))
* Ridhima Nunhokee ([@Chuneeta](https://github.com/Chuneeta))
* Simon Perkins ([@sjperkins](https://github.com/sjperkins))
* Laura Richter ([@LauraRichter](https://github.com/LauraRichter))
* Lerato Sebokolodi ([@Sebokolodi](https://github.com/Sebokolodi))
* Oleg Smirnov ([@o-smirnov](https://github.com/o-smirnov))
* Ulrich Mbou Sob ([@ulricharmel](https://github.com/ulricharmel))
* Cyril Tasse ([@cyriltasse](https://github.com/cyriltasse))
* Kshitij Thorat ([@KshitijT](https://github.com/KshitijT))
* Etienne Bonnassieux ([@ebonnassieux](https://github.com/ebonnassieux))
