from tkinter import *
import os
import subprocess
import random

SOURCE = 'MixtecDict'
NAME = 'MixtecDictionary'
FOLDER = 'Dictionary'

LETTERCOLUMN = 4
PARTOFSPEECHCOLUMN = 5
PRONUNCIATIONCOLUMN = 3

master = Tk()

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)

def stringToList(someString):
	'''string with commas delimiting chunks to list'''
	result = []
	item = ''
	for char in someString: 
		if char != ',':
			item += char
		else: 
			result += [item]
			item = ''
	result += [item] 
	return result

def count(someString,someChars):
	'''return how many instances of 
	someChars there are in someString'''
	result = -1	 # start at -1 because there's 1 extra #
	for char in someString:
		if char in someChars:
			result += 1
	return result 

def categories(emptyList,listOfLists,column):
	'''Makes a list of the different categories found in a column'''
	for entry in listOfLists:
		cat = entry[column]
		if any(z == cat for z in emptyList): 
			pass
		else:
			emptyList += [cat]
	return emptyList

f = open(SOURCE,'r')
'''Makes a list of entries in f, with each entry converted into a list'''
asList = []
for line in f:
	entry = stringToList(line)
	asList += [entry]
f.close()

Letters = []
'''Makes a list of the different letters each word is categorized under'''
categories(Letters,asList,LETTERCOLUMN)

partsOfSpeech = []
'''Makes a list of the different parts of speech each word is categorized under'''
categories(partsOfSpeech,asList,PARTOFSPEECHCOLUMN)

selectedPartsSpeech = []
'''Make a list of selected parts of speech'''
numPartsOfSpeech = 1
for part in partsOfSpeech:
	var = IntVar()
	checkIt = Checkbutton(master, text=part, variable=var)
	checkIt.grid(row=numPartsOfSpeech, sticky=W)
	checkIt.select()
	selectedPartsSpeech += [var]
	numPartsOfSpeech += 1

def buildDict():
	Wanted = []
	num = 0
	for pick in selectedPartsSpeech:
		if pick.get() == 1:
			Wanted += [partsOfSpeech[num]]
		else:
			pass
		num += 1
	# makes a list of the desired parts of speech as Wanted

	numOfWords = 0

	for lett in Letters:
		for entry in asList:
			if (entry[LETTERCOLUMN] == lett) and (entry[PARTOFSPEECHCOLUMN] in Wanted):
				numOfWords += 1
			else:
				pass

	createFolder('./'+FOLDER+'/')
	# Creates a folder in the current directory called Dictionary
	
	g = open(FOLDER+'/'+NAME+'.tex','w')

	g.write('% '+NAME+'.tex\n')
	g.write('\\documentclass[12pt]{article}\n')
	g.write('\\usepackage[margin=1in]{geometry}\n')
	g.write('\\usepackage{palatino}\n')
	g.write('\\usepackage{setspace} % for line spacing\n')
	g.write('\\usepackage{booktabs}\n')
	g.write('\\usepackage{longtable}\n')
	g.write('\\usepackage{array} % for defining a new column type\n')
	g.write('\n')

	g.write('%\\renewcommand{\\familydefault}{\\sfdefault}\n')
	g.write('\n')
	g.write('\\newcolumntype{C}{>{\\bf}c}\n')
	g.write('\\newcolumntype{A}{>{\\it}l}\n')
	g.write('\\newcolumntype{T}{>{--\ } l}\n')
	g.write('\n')

	g.write('\\begin{document}\n')
	g.write('\n')
	g.write('\\title{')
	g.write("\\underline{tutu t\\`u'un s\\`av\\`i \\~nuu$\\star$ n\\`u\\`u$\\star$ yuk\\`u}\\\\\n")
	g.write('\\underline{Diccionario Mixteco de San Miguel Cuevas}\\\\\n')
	g.write('Cuevas Mixtec Dictionary}\n')
	g.write('\\author{CBDIO}\n')
	g.write('% \\date{}\n')
	g.write('\n')
	g.write('\\maketitle\n')
	g.write('\n')
	g.write('\\onehalfspacing\n')
	g.write('\n')

	g.write('\\begin{center}\n')
	g.write('\\begin{longtable}{rl}\n')
	g.write('\\toprule\n')
	g.write('\\textbf{Selected categories}: & \\emph{'+', '.join(Wanted)+'}\n')
	g.write('\\\\\n')
	g.write('\\textbf{Number of words}: & \\emph{'+str(numOfWords)+'}\n')
	g.write('\\\\\n')
	g.write('\\bottomrule\n')
	g.write('\\end{longtable}\n')
	g.write('\\end{center}\n')
	g.write('\n')	

	for lett in Letters:
		g.write('\\section*{'+lett+'}\n')
		g.write('\n')
		g.write('\\begin{longtable}[l]{CATT}\n')
		g.write('\\toprule\n')
		for entry in asList:
			if (entry[LETTERCOLUMN] == lett) and (entry[PARTOFSPEECHCOLUMN] in Wanted):
				# remove second part above for full dictionary
				g.write(entry[0])
				for field in entry[PARTOFSPEECHCOLUMN:]:
					g.write(' & '+field)
				g.write('\\\\\n')
			else:
				pass
		g.write('\\bottomrule\n')
		g.write('\\end{longtable}\n')
		g.write('\n')	

	g.write('\\end{document}'+'\n')

	g.close()

	print('fishihed '+NAME+'.tex')

	os.chdir(FOLDER)
	# Changes directory to Dictionary folder
	os.system('pdflatex '+NAME+'.tex')
	# Runs pdflatex on the tex file in dictionary folder
	subprocess.Popen("%s %s" % ('C:\\Program Files\\SumatraPDF\\SumatraPDF.exe', NAME+'.pdf'))
	# Runs pdflatex on the tex file in dictionary folder
	os.chdir(os.path.dirname(os.getcwd()))
	# Changes directory back to parent folder of Dictionary folder

	print('building '+NAME+'.pdf now')

Label(master, text="Desired parts of speech:").grid(row=0, sticky=W)

Button(master, text='Build', command=buildDict).grid(row=numPartsOfSpeech+1, sticky=W, pady=4)

Button(master, text='Quit', command=master.quit).grid(row=numPartsOfSpeech+2, sticky=W, pady=4)

mainloop()