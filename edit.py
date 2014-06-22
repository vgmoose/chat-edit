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
        self.contents = ""
        self.y = 0
        self.x = 0
        self.pos = 0
        self.lpos = 0
        self.rpos = 0
    
    def getline(self, around):
        if self.contents == "":
            return "█"
        line = self.contents[self.lpos:self.rpos]
	if self.rpos == self.pos:
	    line = line[:self.pos-self.lpos] + "█" 
	else:
            line = line[:self.pos-self.lpos] + "█" + line[self.pos-self.lpos+1:]
            msg("selection: " + self.contents[self.pos])
        return line

    def load_file(self, args):
        try:
            self.file = open(args, "r+")
        except:
            self.file = open(args, "w+")
        self.contents = self.file.read()
        self.changes = False
        
        self.rpos = self.contents.find("\n")
        if self.rpos == -1:
            self.rpos = len(self.contents)
        
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
                self.file.seek(0)
                self.file.write(self.contents)
                self.changes = False
                msg(str(len(self.contents)) + " characters written to " + self.file.name)

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
	    try:
	    	length = int(args)
	    except:
		length = 1
	    self.contents = self.contents[:self.pos] + self.contents[self.pos+length:]
	    self.rpos -= length
	    print(self.getline(1))

	elif command in appendwords:
	    self.pos += 1
	    self.interpret("i " + args)

        elif command in typewords:
            self.changes = True
            self.contents = self.contents[:self.pos] + args + self.contents[self.pos:]
            self.rpos += len(args)
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
