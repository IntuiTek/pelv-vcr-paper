SHELL := /bin/bash
.PHONY: all pdf check clean

all: pdf

pdf:
	latexmk -pdf draft/main.tex

check:
	pdffonts draft/main.pdf | awk 'NR>2 && ($2!="yes" || $3!="yes"){print "ERROR: Font embed or subset missing"; exit 1}'
	gs -dPDFSETTINGS=/prepress -dSubsetFonts=true -dEmbedAllFonts=true \
	   -sDEVICE=pdfwrite -o draft/main_pdfa.pdf draft/main.pdf
	mv draft/main_pdfa.pdf draft/main.pdf

clean:
	latexmk -CA 