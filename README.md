chat-edit
=========

Fairly functional text editing through chat confined messages

## Goal 
Provide interactive editing functionality that can happen via a series of "commands". This is desirable in situations where you cannot "see" the editor, such as a chat conversation or if you want to edit via audio-only. Every command is designed to respond with feedback about the current line, which can then be returned in a chat message or piped into a text-to-speech program.

## Example Conversation
$ cat file.txt 
```
To whomever it may concern,

We nee to send the package to Mr. Lolliford. 
It's very important that it arrive on time, and not be early.

Thanks,
Carlton
```
$ python edit.py 
```
==================
welcome to [chat-edit]
to open a file try 'open [path to file]'
==================
```
\> open file.txt
```
[loaded file.txt into memory]
```
\> print
```
[selection: T]
█o whomever it may concern,
```
\> down 2
```
[selection: W]
█e nee to send the package to Mr. Lolliford. 
```
\> l 5
```
[selection: e]
We ne█ to send the package to Mr. Lolliford. 
```
\> l
```
[selection:  ]
We nee█to send the package to Mr. Lolliford. 
```
\> i d
```
[selection: d]
We nee█ to send the package to Mr. Lolliford. 
```
\> find early
```
[early found on line 3]
[selection: e]
It's very important that it arrive on time, and not be █arly.
```
\> v 4 
```
[selection: early]
It's very important that it arrive on time, and not be █████.
```
\> x
```
[selection: .]
It's very important that it arrive on time, and not be █
```
\> type late
```
[selection: e]
It's very important that it arrive on time, and not be lat█.
```
\> :wq
```
[147 characters written to file.txt]
[now exiting]
```
$ cat file.txt 
```
To whomever it may concern,

We need to send the package to Mr. Lolliford. 
It's very important that it arrive on time, and not be late.

Thanks,
Carlton
```
