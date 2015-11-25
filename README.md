# Fundamentals of Radio Interferometry

An ipython notebook-based book on the fundamentals of radio interferometry

## Setup contributor virtualenv

If you would like to contribute to notebooks it is useful to setup a python virtual environment to ensure your environment is consistent with other contributors. This section provides a guide for how to do this in an Ubuntu system, other systems should work with slight modifications.

Currently we are using pip to install packages, the most important package versions are:

* pip 7.1.2
* python 2.7.6
* numpy 1.10.1
* matplotlib 1.5.0
* scipy 0.16.1
* ipython 4.0.0

This guide was developed from these references:

* <http://jeffskinnerbox.me/posts/2013/Oct/06/ipython-notebook-in-virtualenv/>
* <http://iamzed.com/2009/05/07/a-primer-on-virtualenv/>
* <http://jonathanchu.is/posts/virtualenv-and-pip-basics/>
* <https://warpedtimes.wordpress.com/2012/09/23/a-tutorial-on-virtualenv-to-isolate-python-installations/>


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

Now this is a completely clean environment, there are no python packages installed, we need to set those up. There are two ways to do this, first is by running the following pip install commands, the other is by installing from the requirements file included in the this repository. I recommend the requirements file as it contains current version information.

```
$ pip install -r [path to this repository]/requirements.txt
```

or

```
$ pip install --upgrade pip
$ pip install yolk
$ pip install numpy
$ pip install matplotlib
$ pip install scipy
$ pip install ipython[all]
```

We are now ready to check out the notebook repository and start the ipython notebook server:

```
$ git clone https://github.com/griffinfoster/fundamentals_of_interferometry.git
$ cd fundamentals_of_interferometry
$ ipython notebook
```

To kill the server, type ctrl-c at the terminal and input y. To deactivate the virtualenv and return to your normal environment run:

```
$ deactivate
```

In the future, when you wish to return to the virtualenv, change to the fundamentals directory and run:

```
$ source bin/activate
```