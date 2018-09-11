#!/usr/bin/python

from Tkinter import Tk, StringVar, IntVar, Text, Label, Button, Entry, Canvas, PhotoImage, ALL, END, INSERT, W, E
import os
import time
import itertools

#f = open('wordlist.txt', 'r')	
#f = open('en.txt', 'r')	
f = open('OWL3_Dictionary.txt', 'r')
dictList = f.read().splitlines()


class Words:
	def __init__(self,master):
		self.master = master 
		master.title("Word Cookies")

		letterCheck = master.register(self.CheckLetterEntry)
		wordLenCheck = master.register(self.CheckWordLenEntry)

		self.entryVariable = StringVar()
		self.entry = Entry(master,textvariable=self.entryVariable,validate='focusout',validatecommand=(letterCheck, '%P'))
		self.entry.grid(column=0,row=0,columnspan=2,sticky='EW',padx=10,pady=20,ipadx=10,ipady=10)
		#self.entry.bind("<Return>", self.OnButtonClick)
		self.entryVariable.set(u"Letters")

		wordLenLabel = Label(master,text="Word Length",anchor="e",justify="right",padx=10,pady=20)
		wordLenLabel.grid(column=0,row=1,sticky='E')

		self.wordLenVariable = StringVar()
		self.wordLenEntry = Entry(master,textvariable=self.wordLenVariable,validate='focusout',validatecommand=(wordLenCheck, '%P'))
		self.wordLenEntry.grid(column=1,row=1,padx=10,pady=10,ipadx=10,ipady=10)
		self.wordLenVariable.set("0")

		button = Button(master,text=u"Find Words!",command=self.OnButtonClick,pady=10,fg="#383a39",bg="#a1dbcd")
		button.grid(column=0,row=2,columnspan=2,pady=10)
		#button['state'] = "disabled"

		self.canvas = Canvas(master,width=300,height=50)
		self.canvas.grid(column=0,row=4,columnspan=2)

		self.resultsText = Text(master,state="disabled")
		self.resultsText.grid(column=0,row=3,columnspan=2)

		master.grid_columnconfigure(0,weight=1)

	#	master.resizable(False,True)
		master.update()
		#master.geometry(self.geometry())
		#self.entry.focus_set()
		self.entry.focus()
		#self.entry.selection_range(0, Tkinter.END)

		#self.entryVariable.trace("w", validateFields)
		#self.giflist = []
		#self.giflist.append(PhotoImage('loadingdot1.gif'))
		#self.giflist.append(PhotoImage('loadingdot2.gif'))
		#self.giflist.append(PhotoImage('loadingdot3.gif'))

		self.timer_id = None

	def draw_one_frame(self,picNbr=0):
		giflist = []
		giflist.append(PhotoImage(file='loadingdot1.gif'))
		giflist.append(PhotoImage(file='loadingdot2.gif'))
		giflist.append(PhotoImage(file='loadingdot3.gif'))
		#picNum = picNbr % (len(giflist))
		gif = giflist[picNbr]
		self.canvas.create_image(gif.width()//2, gif.height()//2, image=gif)

	def start_loading(self,currFrame):
		if currFrame > 2: currFrame = 0
		self.draw_one_frame(currFrame)
		currFrame = currFrame + 1
		root.update_idletasks()
		self.stop_id = root.after(100, self.start_loading(currFrame))

	def stop_loading(self):
			root.after_cancel(self.stop_id)
			self.canvas.delete(ALL)

	#def CheckLetterEntry(self, d, i, P, s, S, v, V, W):
	def CheckLetterEntry(self, new_text):
		if not new_text:
			self.entryVariable.set("Enter Letters Here.")
			return True
			
		if not(new_text.isalpha()):
			#print "Invalid Input Detected"
			self.entry.config(bg='red',fg='white')
			self.entry.focus_set()
			return False
		else:
			#print "Valid Input Detected"
			self.entry.config(bg='white',fg='black')
			return True

	def CheckWordLenEntry(self, new_text):
		if not new_text:
			self.wordLenVariable.set("0")
			return True
			
		if not(new_text.isdigit()):
			#print "WL Invalid Input Detected"
			self.wordLenEntry.config(bg='red',fg='white')
			self.wordLenEntry.focus_set()
			return False
		else:
			#print "WL Valid Input Detected"
			self.wordLenEntry.config(bg='white',fg='black')
			return True

	def OnButtonClick(self):
		self.resultsText['state'] = "normal"
		self.resultsText.delete(1.0, END)
		self.resultsText.insert(1.0, "Finding Words. Please Wait. . .")
		#self.resultsText['state'] = "disabled"
		self.master.update()
		# Check the Letters Entry and Word Len Entry
		if (self.entryVariable.get().isalpha()) and (self.wordLenEntry.get().isdigit()):
			self.entry.config(bg='white',fg='black')
			self.wordLenEntry.config(bg='white',fg='black')
			
			#self.resultsText['state'] = "normal"
			#self.resultsText.delete(1.0, END)
			#self.resultsText['state'] = "disabled"

			#Get the letters to use
			letterArr = str(self.entry.get())

			#Get the word length
			if self.wordLenEntry.get() == "":
				wordLen = 0
			else:
				wordLen = int(self.wordLenEntry.get())

	#### Build a list of possible words by running Permute on String[0-1] to String[0-length]
	#### read in the american-english list into an array.
	#### for each possible word, check it against american-english array if it exists add it to answer array if not already an answer
	#### only display answers that match the given wordLen
	#
			# compare fullWordList against dict and return matches
			# if wordLen given is 0 or blank, return ALL matching english words
			# if wordLen is not blank or 0, return only matches whose length = wordLen
			
			#convert all letters to lowercase
			letterArr = letterArr.lower()
			fullWordList = []
			a = time.clock()
			if wordLen == 0:
				#PermWordList = itertools.permutations(letterArr,len(letterArr))
				#for l in range(3,len(letterArr)+1):
				for l in range(2,len(letterArr)+1):
					PermWordList = list(itertools.permutations(letterArr, l))
					for permWord in PermWordList:
						combinedWord = ""
						for w in range(0,len(permWord)):
							combinedWord += permWord[w]
						fullWordList.append(combinedWord)
				#	PermWordList = PermWordList + TempList

			else:
				PermWordList = itertools.permutations(letterArr,wordLen)
				PermWordList = list(PermWordList)
				for permWord in PermWordList:
					combinedWord = ""
					for w in range(0,len(permWord)):
						combinedWord += permWord[w]
					fullWordList.append(combinedWord)

			b = time.clock()
			exec_time_perm = (b - a)

			#fullWordList = sorted(set(fullWordList),key=len)
			fullWordList = sorted(set(fullWordList),key=lambda item:(-len(item),item),reverse=True)
			#fullWordList = fullWordList.sort(key=lambda item:(-len(item),item))

			#print "Full Word List: ", fullWordList

			numWordsFound = 0
			a = time.clock()
			# Enable the Results field and clear it
			self.resultsText['state'] = "normal"
			self.resultsText.delete(1.0, END)
			#self.start_loading(0)
			for checkWord in fullWordList:
				if (len(checkWord) > 1):
					#if checkWord in dictList and (wordLen == 0 or wordLen == ""):
				#		self.resultsText.insert(Tkinter.INSERT,checkWord)
				#		self.resultsText.insert(Tkinter.INSERT,'\n')
				#	elif checkWord in dictList and wordLen == len(checkWord):
					if checkWord in dictList:
						self.resultsText.insert(INSERT,checkWord)
						self.resultsText.insert(INSERT,'\n')
						numWordsFound += 1
			#self.stop_loading()
			b = time.clock()

			exec_time_search = (b - a)

			total_time = exec_time_perm + exec_time_search
			
			if numWordsFound == 0:
				self.resultsText.insert(1.0, "No Words Found.")
			else:
				headerStr = "     %d Words Found in %.2f seconds\n----------------------------------------\n\n" % (numWordsFound,total_time)
				self.resultsText.insert(1.0,headerStr)

			#self.resultsText['state'] = "disabled"
			
		else:
			self.resultsText['state'] = "normal"
			self.resultsText.delete(1.0, END)
			if not(self.entryVariable.get().isalpha()):
				self.resultsText.insert(1.0, "Letters field can only contain letters.")
				self.entry.config(bg='red',fg='white')
				self.entry.focus_set()
			elif not(self.wordLenEntry.get().isdigit()):
				self.resultsText.insert(1.0, "Word length field can only contain digits.")
				self.wordLenEntry.config(bg='red',fg='white')
				self.wordLenEntry.focus_set()
			self.resultsText['state'] = "disabled"

root = Tk()
root.geometry("300x550")
my_gui = Words(root)
root.mainloop()
