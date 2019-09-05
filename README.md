# Fundamentals of Radio Interferometry

An ipython notebook-based book on the Fundamentals of Radio Interferometry. This is a community effort with the aim to be constantly improving and adding to the content in an effort to make interferometry as accessible as possible.  Please contribute, whether it is content, editing, or even suggestions.

This book is currently being used to teach the NASSP [Fundamentals of Radio Interferometry](https://ratt-ru.github.io/fundamentals_of_interferometry/) Masters' Course.

## Usage

It is assumed you are familiar with the console and have git, Python 3 and make installed. on Ubuntu/Debian you can install this with:
```
$ sudo apt install python3-pip make
```

Now get yourself a copy of this repository (if you didn't already)
```
$ git clone https://github.com/griffinfoster/fundamentals_of_interferometry.git
$ cd fundamentals_of_interferometry
```

Inside the project just run make to initialise the virtual environment, download the data and start the notebook:
$ make
```

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

### Contributors

* Alexander Akoto-Danso ([@akotodanso](https://github.com/akotodanso))
* Marcellin Atemkeng ([@atemkeng](https://github.com/atemkeng))
* Landman Bester ([@landmanbester](https://github.com/landmanbester))
* Tariq Blecher ([@TariqBlecher](https://github.com/TariqBlecher))
* Roger Deane ([@rdeane](https://github.com/rdeane))
* Griffin Foster ([@griffinfoster](https://github.com/griffinfoster))
* Marisa Geyer ([@marisageyer](https://github.com/marisageyer))
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
* Tim Staley ([@timstaley](https://github.com/timstaley))
* Cyril Tasse ([@cyriltasse](https://github.com/cyriltasse))
* Kshitij Thorat ([@KshitijT](https://github.com/KshitijT))
* Etienne Bonnassieux ([@ebonnassieux](https://github.com/ebonnassieux))
