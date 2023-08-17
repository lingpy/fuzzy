burmish-download:
	git clone https://github.com/lexibank/hillburmish/ --branch v0.2 cldf-data/hillburmish/
burmish-wordlist:
	edictor wordlist --data=cldf-data/hillburmish/cldf/cldf-metadata.json --addon=partial_cognacy:cogids --name=data/burmish
burmish-reconstruction:
	python example-1.py Burmish
burmish-pdf:
	pandoc -i burmish.md -o burmish.pdf --pdf-engine=xelatex
burmish: burmish-wordlist burmish-reconstruction burmish-pdf

karen-download:
	git clone https://github.com/lexibank/luangthongkumkaren/ --branch v0.2 cldf-data/luangthongkumkaren/
karen-wordlist:
	edictor wordlist --data=cldf-data/luangthongkumkaren/cldf/cldf-metadata.json --addon=partial_cognacy:cogids --name=data/karen
karen-reconstruction:
	python example-1.py Karen
karen-pdf:
	pandoc -i karen.md -o karen.pdf --pdf-engine=xelatex
karen: karen-wordlist karen-reconstruction karen-pdf
