from socket import *
import time


##Establishes connection to server on pre-programmed port
serverName = 'localhost'                   # set our server address to our loopback address since we run a local server
serverPort = 15000                         # set our server's port to the one the server listens on
clientSocket = socket(AF_INET, SOCK_STREAM)  # create a TCP socket object

clientSocket.connect((serverName,serverPort))  # establish a connection at localhost:15000


##Explains a cursory amount of regex utility to the user
print("---Welcome to the word finder client!---\nThis client supports regex operations and wildcards?\n")

print("Basics:\n$ - Terminte string with to search for explicitly\n? - Use in place of any character as a wildcard (will look for words with any character in its place)\n")
print("Ex: Searching 'hell?$' will search for the EXPLICIT string 'hell + (any character)', such as 'hello'.\n")
print("Visit: https://docs.python.org/3/library/re.html for more operators and info on regex usage.\n")

print("\nType 'quit' to close the connection")
##Uses standard input from python, originally restricted to only the '?' tag, but found input
##sanitization too cumbersome and a waste if the user wants to perform more complex searches


while True:                             #Create a loop that continually takes queries until 'quit' is entered
    sentence = input("Send a word: ")      
    
    if sentence == "quit" or sentence == 'exit':                # if the input is 'quit' or 'exit' the client shuts down
        clientSocket.sendall(sentence.encode())
        print("Client shutting down.")
        break
    elif sentence == '' or sentence == '\n':     # if the user inputs a newline or simply nothing, we go back to the input
        print("You need to input a search term!")
        continue

##Sends the sentence encoded in binary so that the server can receive and decode it
    clientSocket.sendall(sentence.encode())

##Waits for results from server, posts them to the console
    recieve = clientSocket.recv(4096)
    print("From Server:", recieve)




##Closes the socket connection and terminates the client.
clientSocket.close()
