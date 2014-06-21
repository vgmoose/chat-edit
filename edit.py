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
            self.file = open(args, "w+")
            self.contents = self.file.read()
            self.changes = False
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
