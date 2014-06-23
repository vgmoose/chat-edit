#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, signal, os

print "=================="
print "welcome to [chat-edit]"
print "to open a file try 'open [path to file]'"
print "=================="

# various vocabulary for editing files
openwords = ["open", "load"]
savewords = ["save", "write"]
quitwords = ["quit", "stop", "exit", "done"]
yeswords = ["yes", "y", "ya", "yeah", "okay", "sure", "ok"]
printwords = ["print", "show", "current", "line", "display", "where"]
movewords = ["go", "move"]
rightwords = ["right", "l"]
leftwords = ["left", "h"]
typewords = ["i", "type", "insert"]
appendwords = ["a", "append"]
delwords = ["delete", "x", "del"]
selwords = ["select", "v", "sel"]

resp_flag = ""

# [ and ] denote a system message
def msg(string):
    print "[" + string + "]"

def exit_editor():
    msg("now exiting")
    exit()

def confirm(string, cb):
    global resp_flag
    msg(string)
    resp_flag = cb

class ChatEdit:
    def __init__(self):
        self.changes = False
        self.file = "none"
        self.contents = []
        self.pos = 0
        self.vpos = 0
        self.selectrange = 1
    
    def getline(self, around):
        if self.contents == [] or self.contents[self.vpos] == "":
            return "█"
        line = self.contents[self.vpos][:-1]
        c = line[self.pos:self.pos+self.selectrange]
        if len(line) == self.pos:
            line = line + "█" 
        else:
            line = line[:self.pos] + "█"*self.selectrange + line[self.pos+self.selectrange:]
            msg("selection: " + c)
        return line

    def load_file(self, args):
        try:
            self.file = open(args, "r+")
            for line in self.file:
                self.contents.append(line)
            self.changes = False
        
        except:
            self.file = open(args, "w+")
        
        msg("loaded " + self.file.name + " into memory")

    # main interpret method that processes input
    def interpret(self, input):
        global resp_flag
        words = input.split(" ")
        command = words[0].lower()
        args = " ".join(words[1:])
        
        if resp_flag != "":
            if command in yeswords:
                resp_flag()

            resp_flag = ""
    
        elif command in openwords:
            if not os.path.isfile(args):
                confirm("create " + args + "?", lambda: self.load_file(args))
                return
            self.load_file(args);

        elif command in savewords:
            if self.file == "none":
                msg("no file is loaded")
            else:
            	counter = 0
                self.file.seek(0)
                for line in self.contents:
                    self.file.write(line)
                    counter += len(line)
                self.changes = False
                msg(str(counter) + " characters written to " + self.file.name)

        elif command in quitwords:
            if not self.changes:
                exit_editor()
            else:
                confirm("quit without saving?", lambda: exit_editor())

        elif command in printwords:
            try:
                around = int(args)
            except:
                around = 1
            print self.getline(around)

        elif command in movewords:
            if args == "$":
                self.pos = len(self.contents[self.vpos])-1
                print(self.getline(1))
            elif args == "^":
                self.pos = 0
                print(self.getline(1))
            else:
                self.interpret(args)
        
        elif command in rightwords or command in leftwords:
            try:
                around = int(args)
            except:
                around = 1
            
            if command in leftwords:
                around = -around

            self.pos += around
                
            print(self.getline(1))

	elif command in delwords:
	    self.changes = True
	    try:
	    	length = int(args)
	    except:
	    	length = self.selectrange
	    	self.selectrange = 1
	    self.contents[self.vpos] = self.contents[self.vpos][self.pos] + self.contents[self.vpos][self.pos+length]
	    print(self.getline(1))

	elif command in selwords:
		try:
			value = int(args)
		except:
			value = 1

		self.selectrange += value
		print(self.getline(1))

	elif command in appendwords:
	    self.pos += 1
	    self.interpret("i " + args)

        elif command in typewords:
            self.changes = True
            if (self.contents == []):
                self.contents.append("")
            self.contents[self.vpos] = self.contents[self.vpos][:self.pos] + args + self.contents[self.vpos][self.pos:]
            self.pos += len(args)
            print(self.getline(1))

        else:
            msg("invalid command")

main = ChatEdit()

def signal_handler(signal, frame):
    print ""
    main.interpret("exit")

signal.signal(signal.SIGINT, signal_handler)

# shell loop
while True:
    sys.stdout.write("> ")
    input = raw_input()
    main.interpret(input)
