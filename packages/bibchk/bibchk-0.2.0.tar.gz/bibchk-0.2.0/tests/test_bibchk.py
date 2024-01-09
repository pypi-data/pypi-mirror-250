from bibchk import *

#  ──────────────────────────────────────────────────────────────────────────
# tests

def test_cli_doi():
    """Test DOIs
    """

    doi_bib = '@article{Houpert_2016,\n\tdoi = {10.1002/2016jc011857},\n\turl = {https://doi.org/10.1002%2F2016jc011857},\n\tyear = 2016,\n\tmonth = {nov},\n\tpublisher = {American Geophysical Union ({AGU})},\n\tvolume = {121},\n\tnumber = {11},\n\tpages = {8139--8171},\n\tauthor = {L. Houpert and X. Durrieu de Madron and P. Testor and A. Bosse and F. D{\\textquotesingle}Ortenzio and M. N. Bouin and D. Dausse and H. Le Goff and S. Kunesch and M. Labaste and L. Coppola and L. Mortier and P. Raimbault},\n\ttitle = {Observations of open-ocean deep convection in the northwestern Mediterranean Sea: Seasonal and interannual variability of mixing and deep water masses for the 2007-2013 Period},\n\tjournal = {Journal of Geophysical Research: Oceans}\n}'

    doi_url = "https://doi.org/10.1002/2016JC011857"
    doi_str = "10.1002/2016JC011857"

    bib_dict = parse_args([doi_url, doi_str])

    for ID in bib_dict.keys():
        assert bib_dict[ID] == doi_bib


def test_cli_isbn():
    """Test ISBNs
    """

    isbn_bib = '@book{9780486600611,\n     title = {Fundamentals Of Astrodynamics},\n    author = {Roger R. Bate and Donald D. Mueller and Jerry E. White},\n      isbn = {9780486600611},\n      year = {1971},\n publisher = {Courier Corporation}\n}'

    isbn10 = "0-486-60061-0"

    bib_dict = parse_args([isbn10])

    for ID in bib_dict.keys():
        assert bib_dict[ID] == isbn_bib


def test_cli_multi():
    """Test DOI, URL, and ISBN for the same source.
    """

    doi_bib = '@book{2013,\n\tdoi = {10.1016/c2009-0-63394-8},\n\turl = {https://doi.org/10.1016%2Fc2009-0-63394-8},\n\tyear = 2013,\n\tpublisher = {Elsevier},\n\ttitle = {An Introduction to Dynamic Meteorology}\n}'
    isbn_bib = '@book{9780123848666,\n     title = {An Introduction To Dynamic Meteorology},\n    author = {James R. Holton and Gregory J Hakim},\n      isbn = {9780123848666},\n      year = {2013},\n publisher = {Academic Press}\n}'

    book_doi = "https://doi.org/10.1016/C2009-0-63394-8"
    book_url = "https://www.sciencedirect.com/book/9780123848666/an-introduction-to-dynamic-meteorology"
    book_isbn = "978-0-12-384866-6" # matches the url output

    # doi
    bib_dict = parse_args([book_doi])

    for ID in bib_dict.keys():
        assert bib_dict[ID] == doi_bib

    # isbn
    bib_dict = parse_args([book_url, book_isbn])

    for ID in bib_dict.keys():
        assert bib_dict[ID] == isbn_bib
