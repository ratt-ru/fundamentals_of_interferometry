.PHONY: all pull_data setup_dependencies
all: setup_dependencies pull_data

pull_data:
	wget https://www.dropbox.com/s/n3jyiajytwuldpu/fundamentals_fits.tar.gz?dl=0
	wget https://www.dropbox.com/s/kb3p2mthei8dgl9/simulated_KAT-7_ms.tar.gz?dl=0
	tar -xvzf fundamentals_fits.tar.gz?dl=0 --directory=data/
	tar -xvzf simulated_KAT-7_ms.tar.gz?dl=0 --directory=data/simulated_kat_7_vis
	rm fundamentals_fits.tar.gz?dl=0
	rm simulated_KAT-7_ms.tar.gz?dl=0

setup_dependencies:
	pip install --upgrade pip
	pip install -r requirements.txt
	git clone https://github.com/krosenfeld/slimscat.git
	cd slimscat; python setup.py install 
	rm -rf slimscat
