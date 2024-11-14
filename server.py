import os
import socket
import sys
import time
import argparse 
import types




def analyze_data(data, host_ip):
    # splitting the data into spaces 
    my_data = data.split()
    final_str = "" 
    
    # for each ip 
    for i in range(len(my_data)) : 
        # i want to call the ping function and store the avg latency
        avg_latency = ping_server(my_data[i])
            
            
        # now i traceroute and keep number of hops and each ip from the path
        hops_path = traceroute_server(my_data[i])
        if avg_latency == "failed" or hops_path == "failed":
            return -1
            
        final_str += host_ip + "," + my_data[i] + " " + avg_latency + " " + hops_path
    
    return final_str
 
 

def ping_server(ip_add):
    # pinging an ip and storing the results in ping.txt file
    os.system("ping -c 5 {} > ping.txt".format(ip_add))
    
    # here i will store the result to return it  
    avg_latency = 0.00
    
    
    # opening the file
    with open("ping.txt", "r") as f:        
        for line in f:
            # buffer the file
            content = f.read()
            if "0 received" in content or "Unreachable" in content:
                print("Ping failed.")
            else: 
                print("Ping successfull")
            # if the line contains avg then it's the line with the avg latency
            if "avg" in line:
                # split the line into words
                words = line.split()
                # the 4th word is the avg latency
                latency = words[3].split("/")
                avg_latency = latency[1]
    # closing the file
    f.close()
    # delete the txt file
    os.system("rm ping.txt")
    
    return str(avg_latency)   

def traceroute_server(ip_add):
    # tracerouting an ip and storing the output in a trt.txt file
    os.system("traceroute {} > trt.txt".format(ip_add))
    # check if file created
    
    trtflag = 0
    hop_ctr = 0
    hop_path = ""
    # opening the file
    with open("trt.txt", "r") as f:
        lines = f.readlines()
        last = lines[-2]
        for line in lines:
            # split the line into words
            words = line.split()
                
            # if the first character of the line is a number then it's traceroute line
            if words[0].isdigit(): 
                # if im on the 30th hop and i find a star then the traceroute failed
                if words[0] == "30" and words[1] == "*" and words[2] == "*" and words[3] == "*":
                    trtflag = -1
                    break
                # for each line add 1 to the hops counter
                hop_ctr = words[0]
                # and i add the ip to the path
                hop_path += words[1] + ","   
            # else I am not in the traceroute lines 
            else : 
                continue
            
        # i remove the last char and put \n instead
        hop_path = hop_path[:-1]
        hop_path += "\n"
    # closing the file
    f.close()
    # delete the txt file
    os.system("rm trt.txt")
    if trtflag == -1: 
        return "failed"
    return str(hop_ctr) + " " + hop_path



def main():
    assert(len(sys.argv) == 4)
    TCP_IP = sys.argv[1]
    TCP_PORT = int(sys.argv[2])
    BUFFER_SIZE = int(sys.argv[3])
    
    # print the arguments
    print("TCP_IP: {}".format(TCP_IP))
    print("TCP_PORT: {}".format(TCP_PORT))
    print("BUFFER_SIZE: {}".format(BUFFER_SIZE))
    
    
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("starting connection...")
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)
    
    while 1:
        try:    
            # waiting to accept connection from client
            conn, address = s.accept()
            print("Connection established with {}.".format(address))
            
            buffer = ""
            
            # waiting to receive data from the client
            while 1:
                # data from client have the format of < str >  
                buffer = conn.recv(BUFFER_SIZE).decode()
                
                data = buffer
                
                break;
                
    
            print("received data:", data)
    
            # getting host_ip
            host_ip = sys.argv[1]
    
            # start to analyze and handling data
            data_back_string = analyze_data(data, host_ip)
            if data_back_string == -1:
                print("failed to analyze data")
        
    
            print(data_back_string)
    
            # send the data back to the client
            conn.sendall(data_back_string.encode())
                
        except s.error as e:
            print("Socket error: {}".format(e))
        finally:
            # clean up the connection
            conn.close()
            break
    print("Connection with {} closed.".format(address))
              



if __name__ == "__main__":
    main()

