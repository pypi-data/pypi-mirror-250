#  ──────────────────────────────────────────────────────────────────────────
# local imports

import bibchk.doi as doi
import bibchk.isbn as isbn
import bibchk.bibtex as bibtex

# ──────────────────────────────────────────────────────────────────────────

def determine_standard(standard):

    if doi.is_doi(standard):
        doi_bib = doi.doi_to_bib(standard)
        doi_bib_dict = bibtex.bib_to_dict(doi_bib)

        return doi_bib_dict

    elif isbn.is_isbn(standard):
        isbn13 = isbn.get_isbn13(standard)
        isbn_bib = isbn_to_bib(isbn13)
        isbn_bib_dict = bibtex.bib_to_dict(isbn_bib)

        return isbn_bib_dict

    else:
        print('Given ID is invalid')

        return None


def build_bib(bib_dict, bibkey=None):
    """Build the BibTeX string with the given Bibkey.

    Generates a Bibkey based off the Doc object information if no Bibkey is provided.

    Parameters
    ----------
    bibkey : str
        Unique Bibkey string for the BibTeX string. Defaults to None.

    Returns
    -------
    bib : str
        BibTeX string.
    """

    if bibkey:
        bib_dict['key'] = bibkey

    else:
        bibkey = build_bibkey(bib_dict)

        if not bibkey:
            # console.cprint("DOC: Bibkey not provided and unable to be generated. Please provide a Bibkey.")
            print("Bibkey not provided and unable to be generated. Please provide a Bibkey.")
            return

        bib_dict['key'] = bibkey
    
    bib = bibtex.build_bib(bib_dict)

    return bib


def lastname(bib_dict):
    """Returns first author's lastname.
    """

    authors = bib_dict['author'].split(' and ')

    first_author = authors[0]
    first_author_lastname = bibtex.author_lastname(first_author)

    return first_author_lastname


def build_bibkey(bib_dict):
    """Builds a unique Bibkey based on the Doc object information.

    Fails if the Doc doesn't have an author or year of publication.

    Returns
    -------
    bibkey : str
        Unique Bibkey or None, if generation fails.
    """

    bibkey_list = []
    
    if 'author' in bib_dict:
        bibkey_list.append(lastname(bib_dict))
    
    if 'year' in bib_dict:
        bibkey_list.append(bib_dict['year'])
    
    bibkey = ''.join(bibkey_list)

    if len(bibkey) > 0:
        return bibkey
    else:
        return None

# ──────────────────────────────────────────────────────────────────────────
# print

def et_al(bib_dict):
    """Returns an 'et al.' variant of the authors if there's more than one author.
    """

    if 'author' in bib_dict:
        authors = bib_dict['author'].split(' and ')

        first_author = authors[0]
        first_author_lastname = bibtex.author_lastname(first_author)

        if len(authors) > 1:
            return first_author_lastname + ' et al.'
        else:
            return first_author_lastname

    else:
        return None
