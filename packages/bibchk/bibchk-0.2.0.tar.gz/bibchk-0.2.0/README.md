# bibchk

Simple program to return the BibTeX string of a given DOI(s) or ISBN(s).

## Install

`pip install bibchk`

## Example Usage

An example with a DOI and DOI URL:

```bash
$ bibchk 10.1002/2016JC011857 https://doi.org/10.1002/2016JC011857
@article{Houpert_2016,
	doi = {10.1002/2016jc011857},
	url = {https://doi.org/10.1002%2F2016jc011857},
	year = 2016,
	month = {nov},
	publisher = {American Geophysical Union ({AGU})},
	volume = {121},
	number = {11},
	pages = {8139--8171},
	author = {L. Houpert and X. Durrieu de Madron and P. Testor and A. Bosse and F. D{\textquotesingle}Ortenzio and M. N. Bouin and D. Dausse and H. Le Goff and S. Kunesch and M. Labaste and L. Coppola and L. Mortier and P. Raimbault},
	title = {Observations of open-ocean deep convection in the northwestern Mediterranean Sea: Seasonal and interannual variability of mixing and deep water masses for the 2007-2013 Period},
	journal = {Journal of Geophysical Research: Oceans}
}

@article{Houpert_2016,
	doi = {10.1002/2016jc011857},
	url = {https://doi.org/10.1002%2F2016jc011857},
	year = 2016,
	month = {nov},
	publisher = {American Geophysical Union ({AGU})},
	volume = {121},
	number = {11},
	pages = {8139--8171},
	author = {L. Houpert and X. Durrieu de Madron and P. Testor and A. Bosse and F. D{\textquotesingle}Ortenzio and M. N. Bouin and D. Dausse and H. Le Goff and S. Kunesch and M. Labaste and L. Coppola and L. Mortier and P. Raimbault},
	title = {Observations of open-ocean deep convection in the northwestern Mediterranean Sea: Seasonal and interannual variability of mixing and deep water masses for the 2007-2013 Period},
	journal = {Journal of Geophysical Research: Oceans}
}
```

Or with an ISBN:

```bash
$ bibchk 0-486-60061-0
@book{9780486600611,
     title = {Fundamentals Of Astrodynamics},
    author = {Roger R. Bate and Donald D. Mueller and Jerry E. White},
      isbn = {9780486600611},
      year = {1971},
 publisher = {Courier Corporation}
}
```
