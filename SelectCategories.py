# add different inflections of verbs as separate words under
# different categories like v.prs and v.cmp

from tkinter import *
import os
import subprocess
# import random

SOURCE = 'MixtecDict'
NAME = 'MixtecDictionary'
FOLDER = 'Dictionary'

LETTERCOLUMN = 4
PARTOFSPEECHCOLUMN = 5
PRONOUNCECOLUMN = 3
SEGMENTCOLUMN = 2

VOWELCOLUMN = 0
QUALITYCOLUMN = 1
SYLLABLECOLUMN = 2
TONECOLUMN = 3

master = Tk()

def createFolder(directory):
	try:
		if not os.path.exists(directory):
			os.makedirs(directory)
	except OSError:
		print ('Error: Creating directory. ' + directory)

def stringToList(someString,symbol):
	'''string with commas delimiting chunks to list'''
	result = []
	item = ''
	for char in someString: 
		if char != symbol:
			item += char
		else: 
			result += [item]
			item = ''
	result += [item] 
	return result

def superList(someList):
	'''Embeds sublists into the pronunciation column'''
	newList = []
	for entry in someList:
		newEntry = []
		for field in entry:
			newEntry += [field]

		newEntry[PRONOUNCECOLUMN] = []
		segmentList = stringToList(entry[PRONOUNCECOLUMN],' ')
		for segment in segmentList:
			if any(syl in segment for syl in '0123456789'):
				featureList = []
				featureList += [segment.strip("ON0123456789HML")]
				featureList += [segment.strip("aeiou'0123456789HML")]
				featureList += [segment.strip("aeiou'ONHML")]
				featureList += [segment.strip("aeiou'ON0123456789")]
				newEntry[PRONOUNCECOLUMN] += [featureList]
			else:
				newEntry[PRONOUNCECOLUMN] += [[segment]]

		newList += [newEntry]
	return newList

def countSyll(someVowel):
	'''return how many syllables there are in someVowel'''
	result = 0
	for segment in someVowel:
		if len(segment) > 1:
			result += 1
		else:
			pass
	return result 

# def featureSeq(someVowel,featureColumn):
#	'''Makes a list of sequences of features for each entry'''
#	contour = ''
#	for segment in someVowel:
#		if len(segment) > 1:
#			contour += segment[featureColumn]
#		else:
#			pass
#	return contour

def categories(someList):
	'''Makes a nonredundant list of items'''
	different = []
	for entry in someList:
		if any(z == entry for z in different): 
			pass
		else:
			different += [entry]
	return different

def wanted(fullList,selectList):
	'''Makes a list of the desired entries from a full list'''
	want = []
	num = 0
	for pick in selectList:
		if pick.get() == 1:
			want += [fullList[num]]
		else:
			pass
		num += 1
	return want

f = open(SOURCE,'r')
'''Makes a list of entries in f, with each entry converted into a list'''
asList = []
for line in f:
	entry = stringToList(line,',')
	asList += [entry]
goodList = superList(asList)
f.close()

listLetter = []
'''Makes a list of letter categories for every entry'''
for entry in goodList:
	listLetter += [entry[LETTERCOLUMN]]

listPoS = []
'''Makes a list of parts of speech for every entry'''
for entry in goodList:
	listPoS += [entry[PARTOFSPEECHCOLUMN]]

listVowel = []
listQuality = []
listTone = []
listConsonant = []
listSyllable = []
'''Makes lists of vowels and consonants for every entry'''
for entry in goodList:
	seqQuality = ''
	seqTone = ''
	syllable = 0
	for phone in entry[PRONOUNCECOLUMN]:
		if len(phone) > 1:
			listVowel += [phone[VOWELCOLUMN]]
			seqQuality += phone[QUALITYCOLUMN]
			seqTone += phone[TONECOLUMN]
			syllable += 1
		else:
			listConsonant += [phone[0]]
	listQuality += [seqQuality]
	listTone += [seqTone]
	listSyllable += [syllable]

class Checkbar(Frame):
	'''Create a checkbar '''
	def __init__(self, parent=None, picks=[], side=LEFT, anchor=W):
		Frame.__init__(self, parent)
		self.vars = []
		for pick in picks:
			var = IntVar()
			chk = Checkbutton(self, text=pick, variable=var)
			chk.select()
			chk.pack(side=side, anchor=anchor, expand=YES)
			self.vars.append(var)
		self.winfo_toplevel().title("Print a PDF Dictionary with LaTeX")
	def state(self):
		return map((lambda var: var), self.vars)
if __name__ == '__main__':
	'''create the selection window with rows'''
	pos = Checkbar(master, categories(listPoS))
	syl = Checkbar(master, categories(listSyllable))
	# qua = Checkbar(master, categories(listQuality))
	grm = Text(master, width=20, height=1, wrap=WORD)
	Label(master, text="Desired parts of speech:").pack(side=TOP, anchor=W)
	pos.pack(side=TOP,  fill=X)
	Label(master, text="Desired number of syllables:").pack(side=TOP, anchor=W)
	syl.pack(side=TOP, fill=X)
	# Label(master, text="Desired vowel quality sequences (O = oral, N = nasal):").pack(side=TOP, anchor=W)
	# qua.pack(side=TOP, fill=X)
	Label(master, text="Desired string of letters:").pack(side=TOP, anchor=W)
	grm.pack(side=TOP, fill=X)
	pos.config(relief=GROOVE, bd=2)
	syl.config(relief=GROOVE, bd=2)
	# qua.config(relief=GROOVE, bd=2)
	grm.config(relief=GROOVE, bd=2)

def buildDict():

	'''Lists of selected categories'''
	selectPoS = wanted(categories(listPoS),list(pos.state()))
	selectSyllable = wanted(categories(listSyllable),list(syl.state()))
	# selectQuality = wanted(categories(listQuality),list(qua.state()))
	selectString = grm.get("1.0",'end-1c').replace('\\','').replace('#','\\#').replace('$','\\$').replace('%','\\%').replace('^','\\^').replace('&','\\&').replace('_','\\_').replace("~","\\~")

	numWords = 0
	'''Counts the number of words printed'''
	for lett in categories(listLetter):
		for entry in goodList:
			if entry[LETTERCOLUMN] == lett:
				if entry[PARTOFSPEECHCOLUMN] in selectPoS:
					if countSyll(entry[PRONOUNCECOLUMN]) in selectSyllable:
						# if featureSeq(entry[PRONOUNCECOLUMN],QUALITYCOLUMN) in selectQuality:
						if grm.get("1.0",'end-1c') in entry[SEGMENTCOLUMN]:
							numWords += 1
						else:
							pass
						# else:
							# pass
					else:
						pass
				else:
					pass
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
	g.write('\\textbf{Selected parts of speech}: & \\emph{'+', '.join(selectPoS)+'}\n')
	g.write('\\\\\n')
	g.write('\\textbf{Selected syllable counts}: & \\emph{'+', '.join(str(x) for x in selectSyllable)+'}\n')
	g.write('\\\\\n')
	# g.write('\\textbf{Voive quality sequences}: & \\emph{'+', '.join(selectQuality)+'}\n')
	# g.write('\\\\\n')
	g.write("\\textbf{Selected letter string}: & \\emph{"+selectString+"}\n")
	g.write('\\\\\n')
	g.write('\\textbf{Selected words}: & \\emph{'+str(numWords)+'}\n')
	g.write('\\\\\n')
	g.write('\\textbf{Total words}: & \\emph{'+str(len(goodList))+'}\n')
	g.write('\\\\\n')
	g.write('\\textbf{Percent selected}: & \\emph{'+str(round(100*numWords/len(goodList),1))+'\\%}\n')
	g.write('\\\\\n')
	g.write('\\bottomrule\n')
	g.write('\\end{longtable}\n')
	g.write('\\end{center}\n')
	g.write('\n')	

	for lett in categories(listLetter):
		g.write('\\section*{'+lett+'}\n')
		g.write('\n')
		g.write('\\begin{longtable}[l]{CATT}\n')
		g.write('\\toprule\n')
		for entry in goodList:
			if entry[LETTERCOLUMN] == lett:
				if entry[PARTOFSPEECHCOLUMN] in selectPoS:
					if countSyll(entry[PRONOUNCECOLUMN]) in selectSyllable:
						# if featureSeq(entry[PRONOUNCECOLUMN],QUALITYCOLUMN) in selectQuality:
						if grm.get("1.0",'end-1c') in entry[SEGMENTCOLUMN]:
							g.write(entry[0])
							for field in entry[PARTOFSPEECHCOLUMN:]:
								g.write(' & '+field)
							g.write('\\\\\n')
						else:
							pass
						# else:
							# pass
					else:
						pass
				else:
					pass
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
	# Open the pdf with SumatraPDF
	os.chdir(os.path.dirname(os.getcwd()))
	# Changes directory back to parent folder of Dictionary folder

	print('building '+NAME+'.pdf now')

Button(master, text='Build\nDictionary', fg="green", command=buildDict).pack(side=LEFT, anchor=W)
Button(master, text='End\nSession', fg="red", command=master.quit).pack(side=RIGHT, anchor=W)

mainloop()