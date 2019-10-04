import requests
from bs4 import BeautifulSoup


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

#validates command syntax (strict verb object)
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

#show vocabulary definition
def cmd_show(parsed_command):
    if len(parsed_command) == 1:
        print(actions[parsed_command[0]]['objs'])
    elif len(parsed_command) == 2:
        print(vocabulary[parsed_command[1]])
    
    else:
        print(parsed_command)  

#modify vocabulary definition
def cmd_set(parsed_command):
    if len(parsed_command) > 1:
        if valid_object(parsed_command[1]):
            vocabulary[parsed_command[1]] = parsed_command[2]
        else:
            print("please enter a valid object.")
    else:
        print(actions[parsed_command[0]]["id"])

#clear runtime variable
def cmd_clear(parsed_command):
    if len(parsed_command) == 1:
        print("Please choose a definition to clear.")
    elif len(parsed_command) == 2:
        are_you_sure = verify_choice()
        if are_you_sure == True:
            vocabulary[parsed_command[1]] = ""
        else:
            pass
                
            
        
#verify user choice                
def verify_choice():
    choice = input("Are you sure? y/n \n")
    if choice == "y":
        return True
    elif choice == "n":
        return False
    else:
        print("Please enter y or n.\n")
        verify_choice()       

#request commands        
#dynamically builds request based on request state        
def request_processor(request_state):
    if request_state[0] == 0:
        print("Please set a url.")
    elif request_state == [1,0]:
        url = vocabulary["url"]
        raw_response = requests.get(url)
        return raw_response
    elif request_state == [1,1]:
        username = vocabulary["username"]
        password = vocabulary["password"]
        url = vocabulary["url"]
        raw_response = requests.get(url, auth=(username, password))
        return raw_response        
        
    
#request validator returns a state code to help the processor determine what to use in the request.
def request_state_generator():
    #url and auth bits
    request_state = [0,0]
    #flips url bit of vocabulary[request][state]
    if vocabulary["url"] == "":
        vocabulary["request"]["state"][0] = 0
        request_state[0] = 0
    else:
        vocabulary["request"]["state"][0] = 1
        request_state[0] = 1
    #flips auth bit for request_processor
    if  vocabulary["username"] == "" and vocabulary["password"] == "":
        vocabulary["request"]["state"][1] = 0
        request_state[1] = 0
    else:
        vocabulary["request"]["state"][1] = 1
        request_state[1] = 1
    #TODO: flip paramters and ssl bit, as needed
    return request_state
            
#returns parsed html object
def response_html_parser(raw_response):
    parsed_html = BeautifulSoup(raw_response.content, "lxml")
    return parsed_html 

#runs request builder and calls the request
def cmd_run(parsed_command):
    http_response = request_processor(request_state_generator())
    html_response = response_html_parser(http_response)
    print(html_response)
    return(html_response)        
    
    

#command list
actions = {
    "show" : {"id" : 1, "objs" : ["url", "username", "password"], "call alias" : cmd_show},
    "set" : {"id" : 2, "call alias" : cmd_set},
    "run" : {"id" : 3, "call alias" : cmd_run},
    "clear" : {"id" : 4, "call alias" :  cmd_clear}
}

#user can modify these variables during runtime
vocabulary = {
    "url" : "http://natas0.natas.labs.overthewire.org/",
    "username" : "",
    "password" : "",
    "response" : "",
    # state = [auth, paramaters, ssl] boolean
    "request" : {"state" : [0,0,0,0]}
}




#function for calling commands
def call_command(command_string):
    parsed_command = parse_command(command_string)
    if valid_syntax(parsed_command) == True:
        actions[parsed_command[0]]["call alias"](parsed_command)
    else:
        print("syntax error")
        


#main loop to continuously accept input.


def main():
    while 1:
        cmd = input("requester..>")
        if cmd == 'quit':
            break
        else:
            call_command(cmd)

main()                  
             

