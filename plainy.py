#!/usr/bin/python
import subprocess
import magic
import sys

def usage():
	""" Print out usage of this Program """
	print 'Plainy extracts plaintext from various file formats.'
	print 'Usage: plainy filename.ext'
	sys.exit()

if __name__ == '__main__':
	try: 
		dfile = sys.argv[1]
	except:
		usage()

	print dfile

	m = magic.open(magic.MAGIC_MIME)
	m.load()
	mime = m.file(dfile)
	print mime

	if mime.startswith('application/pdf'):
		print subprocess.Popen("pdftotext -layout " + dfile + " - ", \
			shell=True, stdout=subprocess.PIPE).communicate()[0]

	if mime.startswith('application/vnd.oasis.opendocument.text'):
		print subprocess.Popen("unzip -p '"+ dfile + \
		"' content.xml | xmlstarlet sel -N "\
		+ "text='urn:oasis:names:tc:opendocument:xmlns:text:1.0'"\
		+"  -T -t -m '//text:p' -v . -n", shell=True, \
			stdout=subprocess.PIPE).communicate()[0]

	if mime.startswith('text/rtf'):
		print subprocess.Popen("unrtf --nopict -t text " + dfile \
			+ " 2> /dev/null | sed -e '/^###.*/d' -e '/^----.*/d'"\
			, shell=True, \
			stdout=subprocess.PIPE).communicate()[0]

	if mime.startswith('text/html'):
		print 'HTML'

	if mime.startswith('application/zip') and dfile.endswith('.docx'):
		import docx
		document = docx.opendocx(dfile)
		paratextlist = docx.getdocumenttext(document)
		print '\n\n'.join(paratextlist)
