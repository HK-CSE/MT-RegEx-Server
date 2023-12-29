from socket import *      # import sockets
import time, re           # import time and regex libraries
import _thread as thread  # import thread support

##Regex code https://docs.python.org/3/library/re.html
##https://www.educative.io/edpresso/how-to-implement-wildcards-in-python


##Opens the server to listen for one client on port 1500, prints ready status
serverPort = 15000                         # set server port to 15000
serverSocket = socket(AF_INET, SOCK_STREAM) # create a TCP socket object
serverSocket.bind(("", serverPort))         # bind on "":15000 (localhost:15000)
serverSocket.listen(5)                      # listen for 5 connections

print("Server ready for connections")       # post to console that we're ready for connecitons

wordfile = open('wordlist.txt', 'r')    # Open our wordlist
words = wordfile.readlines()            # Read all lines from wordlist
wordfile.close()


def ClientHandler(connection):   # method for all spawned threads to start handling clients
    time.sleep(5)                # simulate a socket block
    while True:                     # establish a listen loop
        data = connection.recv(1024)
        matches = []                # establish a matches array to store our matched words
        term = data.decode()        # decode the search term from the client

        if not data:                # if we receive an EOF on the socket, we close it
            break
        elif term == 'exit':        # if we receive an 'exit' term from our client, we close the server entirely
            print("Server exiting.")
            exit()
        elif term == 'quit':        # if we quit, we wait for another client
            connection.close()
            continue
        elif not term or term == '\n':    # if our term is simply a newline or nothing, we relay that info to the client
            msg = "You must input a term."
            connection.send(msg.encode())

        else:
            term = term.replace('?', '.')   # we substitue our '?' wildcard with the regex equivalent '.'
            regex = re.compile(term)        # construct a regex term to match with

            for word in words:                                      # iterate over the word list to find matches using regex
                if re.match(regex, word):
                    matches.append(word.strip('\n'))                 # add matches to the array, strip the newline from the words
                    msg = ', '.join([str(word) for word in matches])  # construct a comma seperated string to send back to the client
            if len(matches) == 0:             # if matches is empty, we have no matches, relay info to client
                msg = 'No queries found'
            connection.sendall(msg.encode())
    connection.close()

def ClientRouter():   # listener and thread spawning method
    while True:
        connection, clientaddr = serverSocket.accept()                                  # accepts a client
        print('Server received client from', clientaddr, 'at', time.ctime(time.time()))  # posts to console that we received a client
        thread.start_new_thread(ClientHandler, (connection,))                            # we spawn a new thread to handle the client

ClientRouter()   # on startup, start the listner and thread spawner method

