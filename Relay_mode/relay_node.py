import socket
import sys
import time
import subprocess
import re
import threading


RECV_BUFFER_SIZE = 2048 



def ping(host,numofpings):
    
    ping = subprocess.Popen(["ping","-c",numofpings, host],stdout = subprocess.PIPE,stderr = subprocess.PIPE)
    
    packet_loss = re.compile(', 100% packet loss,')
    out, error = ping.communicate()
    k = packet_loss.search(out)
    
    if k : #tmp solution 
       print "100% packet loss.\nNo further information available.Please wait for download option."
    else:
        matcherl = re.compile('/(\d+.\d+)')
        #Ip = re.compile('(\d+.\d+.\d+.\d+)')
        #out, error = ping.communicate()
        l = matcherl.search(out)
        #p = Ip.search(out)
        #print out #print to check ip
        #print "Average RTT is:",l.group() #prints average rtt
    #Ip = re.compile('(\d+.\d+.\d+.\d+)')
    #p = Ip.search(out)
    return l.group()



#supportive function to calculate the number of hops
def traceroute(domain):

    count=0
    Sec = 0
    Min = 0
    traceroute = subprocess.Popen(["traceroute", '-w','10',domain],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # Begin Process
    timeLoop = True
    #calculating traceroute time
    while timeLoop:
        for line in iter(traceroute.stdout.readline,""):
            count=count+1
            Sec += 1
            if Sec == 60:
                Sec = 0
                Min += 1
        time.sleep(1)
        timeLoop = False
        
    print (str(Min) + " mins" +" " + str(Sec) + " sec")
        
    #print "Number of hops:",count
    return count


#Creating connection between client-relaynode
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port

#By setting the host name to the empty string, it tells the bind() method to fill in the address of the current machine.

server_address = ('', int(sys.argv[1]))
print >>sys.stderr, 'starting up on %sport %s' % server_address
sock.bind(server_address)

# Listen for incoming connections
sock.listen(3)

while True:
    # Wait for a connection
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()

    try:
        print >>sys.stderr, 'connection from', client_address

        # Receive the data in small chunks and retransmit it
        while True:
                       
            #Creating connection between relay-node and end-server
            pings = connection.recv(RECV_BUFFER_SIZE)
            print >>sys.stderr, 'received number of pings from client:', pings
            IP = connection.recv(RECV_BUFFER_SIZE)
            print >>sys.stderr, 'received end server IP from client:', IP
            sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server = (IP, 80)
            print >>sys.stderr, 'connecting to %s port %s' % server
            sock1.connect(server)

            rtt2= ping(IP,pings)
            rtt2 = rtt2.split('/')
            hops2 = traceroute(IP)

            if pings:
                print >>sys.stderr, 'sending latency back to the client:', rtt2[1]
                connection.sendall(str(rtt2[1]))
            else:
                print >>sys.stderr, 'no more data from', client_address
                break
            if IP:
                print >>sys.stderr, 'sending hops back to the client:', str(hops2)
                connection.sendall(str(hops2))
            else:
                print >>sys.stderr, 'no more data from', client_address
                break
            #break
    finally:
        # Clean up the connection
        connection.close()
    #break