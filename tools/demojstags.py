#!/usr/bin/env python

import os, glob, fileinput, sys

demofolder = "demo"
srcfolder = "src"
jstag = "<!-- J3DLIB -->"
warn = "<!-- Auto-generated by tools/demojstags.py. Do not edit this section -->"
j3dlib = """<script type="text/javascript" src="../build/j3d.js"></script>"""
script = """<script type="text/javascript" src="../%s"></script>"""
lib = """<script type="text/javascript" src="../lib/gl-matrix.js"></script>\n<script type="text/javascript" src="../lib/requestAnimationFrame.js"></script>"""

stdout = sys.stdout

def listSourceFiles():
	jsf = []
	for root, dirs, files in os.walk(srcfolder):
		for name in files:
			fname = os.path.join(root, name)
			if name[-2:] == "js":
				jsf.append(fname)
	return jsf

def log(m):
	stdout.write(m)
	stdout.write("\n")

def parseDemos(debug):
	jsf = listSourceFiles()
	for f in glob.glob( "%s/*.html" % demofolder ):
		injecting = False
		for line in fileinput.input(f, inplace=1):	
			if jstag in line:
				injecting = not injecting
				print line.strip()
				if injecting == True:
					log("Tag found on line %d in %s" % (fileinput.filelineno(), f))
					print warn
					if debug == True:
						print lib
						for js in jsf:
							print script % js
					else:
						print j3dlib
			elif injecting == True:
				pass
			else:
				print line,
			

# # # # # #
if(__name__ == '__main__'):
	print "[ 'debug' for individual js includes, no params - include library ]"
	cwd = os.getcwd().split("/")[-1]
	if cwd == "tools":
		os.chdir('../')
	debug = len(sys.argv) > 1 and sys.argv[1] == "debug"
	parseDemos(debug)




