import requests
from bs4 import BeautifulSoup



#tags = {
#    "aa" : "action",
#    "obj" : "data object: name and value",
#    "val" : "object value",
#    "nam" : "object name"
#} 

#functions for validating commands:
#validates a word as a proper command
def valid_action(command_word):
    if command_word in actions.keys():
        return True
    else:
        return False

#validates an object
def valid_object(command_word):
    if command_word in vocabulary.keys():
        return True
    else:
        return False

#validates command syntax
def valid_syntax(parsed_command):
    if len(parsed_command) == 1:
        if valid_action(parsed_command[0]):
            return True
        else:
            return False
    elif len(parsed_command) >= 2:
        if valid_action(parsed_command[0]) and valid_object(parsed_command[1]):
            return True
        else:
            return False
    else:
        return False


#returns a list of commands parsed from user input
def parse_command(command_string):
    parsed_command_list = command_string.split(" ")
    return parsed_command_list

#command definitions: environment commands

#show
def cmd_show(parsed_command):
    if len(parsed_command) == 1:
        print(actions[parsed_command[0]]['objs'])
    elif len(parsed_command) == 2:
        print(vocabulary[parsed_command[1]])
    
    else:
        print(parsed_command)  

def cmd_set(parsed_command):
    if len(parsed_command) > 1:
        if valid_object(parsed_command[1]):
            vocabulary[parsed_command[1]] = parsed_command[2]
        else:
            print("please enter a valid object.")
    else:
        print(actions[parsed_command[0]]["id"])
        
def request_call():
    url = vocabulary["url"]
    params = 0
    req = requests.get(url)   
    return req

def request_format(req):
    parsed_request = BeautifulSoup(req.content, "lxml")
    return parsed_request 

def cmd_run(parsed_command):
    req = request_call()
    response = request_format(req)
    print(response)
    return(response)
    
    
    
     

#command list
actions = {
    "show" : {"id" : 1, "objs" : ["url", "username", "password"], "call alias" : cmd_show},
    "set" : {"id" : 2, "call alias" : cmd_set},
    "run" : {"id" : 3, "call alias" : cmd_run}
}

#user can modify these variables during runtime
vocabulary = {
    "url" : "http://natas0.natas.labs.overthewire.org/",
    "username" : "",
    "password" : "",
    "response" : ""
}


#function for calling commands
def call_command(command_string):
    parsed_command = parse_command(command_string)
    if valid_syntax(parsed_command) == True:
        actions[parsed_command[0]]["call alias"](parsed_command)
    else:
        print("syntax error")
        


#main loop to continuously accept input.
#TODO: implement an interface to validate and run commands and reply back with results.


def main():
    while 1:
        cmd = input("requester..>")
        if cmd == 'quit':
            break
        else:
            call_command(cmd)

main()                  
             

