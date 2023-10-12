burmish-download:
	git clone https://github.com/lexibank/hillburmish/ --branch v0.2 cldf-data/hillburmish/
burmish-download:
	git clone https://github.com/lexibank/hillburmish/ --branch v0.2 cldf-data/hillburmish/
burmish-wordlist:
	edictor wordlist --data=cldf-data/hillburmish/cldf/cldf-metadata.json --addon=partial_cognacy:cogids --name=data/burmish
burmish-reconstruction:
	python analysis.py Burmish
burmish-pdf:
	pandoc -i burmish.md -o burmish.pdf --pdf-engine=xelatex
burmish: burmish-wordlist burmish-reconstruction burmish-pdf
burmish: burmish-wordlist burmish-reconstruction burmish-pdf

karen-download:
	git clone https://github.com/lexibank/luangthongkumkaren/ --branch v0.2 cldf-data/luangthongkumkaren/
karen-download:
	git clone https://github.com/lexibank/luangthongkumkaren/ --branch v0.2 cldf-data/luangthongkumkaren/
karen-wordlist:
	edictor wordlist --data=cldf-data/luangthongkumkaren/cldf/cldf-metadata.json --addon=partial_cognacy:cogids --name=data/karen
karen-reconstruction:
	python analysis.py Karen
karen-pdf:
	pandoc -i karen.md -o karen.pdf --pdf-engine=xelatex
karen: karen-wordlist karen-reconstruction karen-pdf

pano-wordlist:
	edictor wordlist --data=cldf-data/oliveiraprotopanoan/cldf/cldf-metadata.json --preprocessing=data/panoan_prep.py --addon="cognacy:cogid","alignment:alignment" --name=data/panoan
pano-reconstruction:
	python analysis.py Panoan
pano-pdf:
	pandoc -i panoan.md -o panoan.pdf --pdf-engine=xelatex
pano: pano-wordlist pano-reconstruction pano-pdf

analysis: burmish karen pano
full: download prepare analysis
