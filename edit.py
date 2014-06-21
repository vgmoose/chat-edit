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

# [ and ] denote a system message
def msg(string):
    print "[" + string + "]"

def confirm(string):
    msg(string)
    sys.stdout.write("> ")
    response = raw_input()
    if response in yeswords:
        return True
    else:
        return False

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
        line = line[:self.pos-self.lpos] + "█" + line[self.pos-self.lpos+1:]
        msg("selection: " + self.contents[self.pos])
        return line
    
    # main interpret method that processes input
    def interpret(self, input):
        words = input.split(" ")
        command = words[0].lower()
        args = " ".join(words[1:])
        
        if command in openwords:
            if not os.path.isfile(args):
                if not confirm("create " + args + "?"):
                    msg("filesystem not touched")
                    return
            self.file = open(args, "rw+")
            self.contents = self.file.read()
            self.changes = False
            
            self.rpos = self.contents.find("\n")
            if self.rpos == -1:
                self.rpos = len(self.contents)
            
            msg(command + "ed " + self.file.name + " into memory")

        elif command in savewords:
            if self.file == "none":
                msg("no file is loaded")
            else:
                self.file.write(self.contents)
                self.changes = False
                msg(str(len(self.contents)) + " characters written to " + self.file.name)

        elif command in quitwords:
            if not self.changes:
                msg("now exiting")
                exit()
            else:
                if confirm("quit without saving?"):
                    self.changes = False
                    interpret(input)
                else:
                    msg("quit cancelled")

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
