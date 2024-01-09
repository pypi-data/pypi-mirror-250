import click
import json

#  ──────────────────────────────────────────────────────────────────────────
# local imports

import bibchk.bibtex as bibtex
import bibchk.document as document

#  ──────────────────────────────────────────────────────────────────────────
# global variables

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

#  ──────────────────────────────────────────────────────────────────────────

@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-o', '--output', help='Output type, can be one of the following: bib, json.', type=str, default=None)
@click.argument('standard', type=str)
def bibchk(output, standard):
    """Output the BibTeX information of a DOI or ISBN.
    """

    doc = document.determine_standard(standard)

    outputs = ['bib', 'json']
    if output and output in outputs:

        if output == 'bib':
            doc = document.build_bib(doc)

        if output == 'json':
            doc = json.dumps(doc, sort_keys=True, indent=4, ensure_ascii=False)

    print(doc)
