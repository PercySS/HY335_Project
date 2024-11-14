import socket
import sys
import time
import argparse 
import types



# declaring a global empty dictionary to fill in function that reads the configuration
config_dict = {}

def read_config():
    # opening config txt file
    with open("config_real.txt", "r") as f:
        for line in f:
            line2 = line
            # getting rid of the new line char
            line2.strip()
            # splitting the line in spaces and putting the words into a list
            list = line2.split()
            # putting the first word of each line as keys and the rest of the list as value
            config_dict[list[0]] = list[1:]
    # closing the file 
    f.close()
    
def translate_into_ips(argv2):
    # asserting argv2 as not empty
    # client: python script.py BOST-host,NEWY-host,BARC-host port-number
    # server: python script.py ip port-number buffer-size
    assert(argv2 != " ")

    # splitting the string into a list of words
    list = argv2
    
    list = list.split(",")    
    
    
    for i in range(len(list)):
        # if the word is in the dictionary, replace it with the value of the key
        if list[i] in config_dict.keys():
            list[i] = config_dict[list[i]][0]
        # else put " "
        else :
            list[i] = " "
        
            

    # returnin the argv list
    return list

def translate_into_names(data):
    # data will be sent back into a string server_from-server_to avg_latency No_of_hops hop1-hop2-...-hopn
    # we want to translate all the ips to names of hosts via the dictioanry
    
    # this is the string I will return
    fstring = " "
    
    # asserting data as not empty
    assert(data.strip() != "")

    string = data.strip()
    
    # split data on the new line char
    list = string.split("\n")
    
    # for each element in the list
    for i in range(len(list)):
        # split the element on the spaces
        list[i] = list[i].split(" ")
        
        # for each element in the list
        for j in range(len(list[i])):
            # if im on the first element
            if j == 0:
                # split the element on the dash
                list2 = list[i][j].split(",")

                # if the element is in the values of the dictionary, replace it with its key
                for key, value in config_dict.items():
                    if list2[0] in value:
                        fstring += key + "-"
                    if list2[1] in value:
                        fstring += key + " "
            elif j == 1:
                fstring += "    " + list[i][j] + "   "
            elif j == 2:
                fstring += "           " + list[i][j] + "      "
            elif j == 3:
                list3 = list[i][j].split(",")
                print(list3)
                for k in range(len(list3)):
                    for key, value in config_dict.items():
                        if list3[k] in value:
                            fstring += key + "-"
                fstring += "\n "
                
        
            
    # return the data to print 
    return fstring

def print_data(data) :
    print("|----- Hosts -----|---- Latency ----|---- No of hops -----|---- Path ----|")
    print(data)
    
        
def main():
    assert(len(sys.argv) == 3)
    
    TCP_PORT = int(sys.argv[2])
    
    # reading the config file and making my dictionary for ip-host/server mapping
    read_config()
    
    # list of ips given in cmd
    list_ips = translate_into_ips(sys.argv[1])

    # opning sockets for each server that waits to receive message 
    for i in range(len(list_ips)):
        MESSAGE = " "
        
        for j in range(len(list_ips)):
            # skip the ip if it's the same
            if i != j:
                MESSAGE += list_ips[j] + " "
        
        # debug printings
        print("TCP target IP: " + list_ips[i])
        print("TCP target PORT: " + str(TCP_PORT))
        print("message:" + str(MESSAGE))
        print(type(MESSAGE))
        
        # creating a socket object
        print("creating socket...")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # connect the socket to the IP address and port that the server listens to 
        print("connecting to ip: " + list_ips[i] + " ... ")
        s.connect((list_ips[i], int(sys.argv[2])))
        timeout = 1000
        #s.settimeout(timeout)
        
        
        
        # send the list of ips to the servers
        print("sending data...")
        s.sendall(MESSAGE.encode())

        print("waiting to receive data...")
        # receive data from the server
        data = s.recv(2048).decode()        
        print("received data = " + data)
        data1 = translate_into_names(data)
        
        # print the data received
        print_data(data1)
        
        # closing the socket
        print("closing socket ...")
        s.close()
        




if __name__ == "__main__":
    main()
