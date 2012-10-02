#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""Plainy. Einfach nur Plainy"""
try:
    import sys
    import subprocess
    import magic

except ImportError:
    print "Python failed to load some modules:"
    print  sys.exc_info()[1]
    exit(127)

def usage():
    """ Print out usage of this Program """
    print 'Plainy extracts plaintext from various file formats.'
    print 'Usage: plainy filename.ext'
    sys.exit()

if __name__ == '__main__':
    try:
        DFILE = sys.argv[1]
    except ImportError:
        usage()

    print DFILE

    M = magic.open(magic.MAGIC_MIME)
    M.load()
    MIME = M.file(DFILE)
    print MIME

    if MIME.startswith('application/pdf'):
        print subprocess.Popen("pdftotext -layout " + DFILE + " - ", \
            shell=True, stdout=subprocess.PIPE).communicate()[0]

    if MIME.startswith('application/vnd.oasis.opendocument.text'):
        print subprocess.Popen("unzip -p '"+ DFILE + \
        "' content.xml | xmlstarlet sel -N "\
        + "text='urn:oasis:names:tc:opendocument:xmlns:text:1.0'"\
        +"  -T -t -m '//text:p' -v . -n", shell=True, \
            stdout=subprocess.PIPE).communicate()[0]

    if MIME.startswith('text/rtf'):
        print subprocess.Popen("unrtf --nopict -t text " + DFILE \
            + " 2> /dev/null | sed -e '/^###.*/d' -e '/^----.*/d'"\
            , shell=True, \
            stdout=subprocess.PIPE).communicate()[0]

    if MIME.startswith('text/html'):
        print subprocess.Popen("w3m -dump "+ DFILE \
            , shell=True
            , stdout=subprocess.PIPE).communicate()[0]


    if MIME.startswith('application/zip') and DFILE.endswith('.docx'):
        try:
            import docx
        except ImportError:
            print "Module fuer Docx nicht gefunden!"
        DOCUMENT = docx.opendocx(DFILE)
        PARATEXTLIST = docx.getdocumenttext(DOCUMENT)
        print '\n\n'.join(PARATEXTLIST)

    if MIME.startswith('application/x-rar') and DFILE.endswith('.rar'):
        print subprocess.Popen("rar x " + DFILE \
            , shell=True, \
            stdout=subprocess.PIPE).communicate()[0]


