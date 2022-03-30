#testing the client.py
from threading import Thread
import socket
import sys
import subprocess
import re
import urllib
import threading
#import requests
import time
#import pyglet
import Queue
import collections


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
        l = matcherl.search(out)
        #p = Ip.search(out)
        #print out #print to check ip
        #print "Average RTT from " + host + " is: " + l.group() #prints average rtt
    Ip = re.compile('(\d+.\d+.\d+.\d+)')
    p = Ip.search(out)
    return p.group(),l.group()

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

    #print "\nNumber of hops from " + IP + " is: " + str(count)    
    #print (str(Min) + " minutes" +" " + str(Sec) + " seconds\n")
    return count
    
#supportive function that connects client with server
def connection(IP,port):
    #Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connect the socket to the port where the server is listening
    server_address = (IP, int(port))
    print >>sys.stderr, '\nconnecting to %s port %s' % server_address
    sock.connect(server_address)
    #photo_adr=raw_input( "Insert the address of photo to be downloaded: ")
     

    try:
    
        retry = 'no'
        again = 'no'
        
        photo_adr=raw_input( "Insert the address of photo to be downloaded: ")
        if alias not in photo_adr:
            print "This server doesn't contain this file"
            
        else:
            while retry:
                while again:
                    # Send data
                    message = photo_adr
                    print >>sys.stderr, 'sending "%s"' % message
                    sock.sendall(message)

                    # Look for the response
                    amount_received = 0
                    amount_expected = len(message)
                    response = requests.get(message)
                    while amount_received < amount_expected:
                        if response.status_code == 200:
                            #filepath=raw_input("Insert the path that your photo/gif will be saved and the name of it : ")
                            filepath = '/home/lumoswitch/Desktop/arxidia.png'
                            with open(filepath, 'wb') as f:
                                f.write(response.content)
                            for y in range(21): #Loading progress bar
                                sys.stdout.write('\r')
                                sys.stdout.write("Loading:[%-20s] %d%%" % ('='*y, 5*y))
                                sys.stdout.flush()
                                time.sleep(0.10)
                            print "\nImage downloaded!"
                            #music = pyglet.resource.media('sound1.mp3')
                            #music.play()
                            #pyglet.app.run()
                            print "  _________\n /         \\\n |  /\\ /\\  |\n |    -    |\n |  \\___/  |\n \\_________/" #print a happy face when download is successful
                            #data = sock.recv(RECV_BUFFER_SIZE)
                            #amount_received += len(data)
                            #print >>sys.stderr, 'received "%s"' % data
                            again=raw_input("Do you want to download another file??...Type yes or no!") #Repeat proccess if user wants to
                            if again == 'yes':
                                photo_adr=raw_input( "Insert the address of photo to be downloaded: ")
                                if alias not in photo_adr:
                                    print "This server doesn't contain this file"
                                    again='no'
                                    break
                            retry= 'no'
                            
                        else:
                            print "Oups!...This address does not exist!...Parto alliws na mh ginei panikos!"
                            #music = pyglet.resource.media('sound2.mp3')
                            #music.play()
                            print "  _________\n /         \\\n |  #   #  |\n |    -    |\n |  ____   |\n \\_________/"
                            retry=raw_input("Do you want to try again??...Type yes or no! ") #repeat proccess if user gives wrong url
                            again = 'no'
                        break
                    if retry == 'no':
                        break
                if again == 'no':
                    break 

    finally:
        print >>sys.stderr, 'Connection is terminated!...Kisses! '
        sock.close() 
        print "End of program!"    

#supportive function:pings,traceroutes,prints the statistics using the criterion of user's choice and connects with server
def direct_mode(string,numofpings,criterion,q_direct):

    #print "Ping is executed for direct mode..."
    IP ,latency= ping(string,numofpings)
    #print "Ping done for direct mode."
    #print "Traceroute for direct mode is executed in..."
    trace = traceroute(IP)
    q_direct.put(trace)
    final_lat = latency.split("/")
    q_direct.put(final_lat[1])
    if criterion == 'hops':
        print "Number of hops of direct mode are: ",trace
        #print q_direct.get(0)
        print "\n"
    elif criterion == 'latency':
        print "Average RTT for direct mode is: ",final_lat[1]
        #print q_direct.get(1)

    direct_values = [float(final_lat[1]),trace]
    print "Direct array: ",direct_values
    return direct_values
    #print "Tracetoute for direct mode done."
    #print "Connection in direct mode stage in progress..."
    
    

def relay_mode(IP,domain2,q_relay_rtt,q_relay_hops,criterion):

   
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    relaynode_address = (IP,1028)
    print >>sys.stderr, 'connecting to %s port %s' % relaynode_address
    sock.connect(relaynode_address)
    print "\n"
    
    message1 = numofpings
    print >>sys.stderr, 'sending number of pings ' + message1 + ' to relay ' + IP
    sock.sendall(message1)

    message2 = domain2
    print >>sys.stderr, 'sending the IP of the end server ' + message2 + ' to relay ' + IP 
    sock.sendall(message2)
    
    ip,rtt1 = ping(IP,numofpings)
    rtt1_data = rtt1.split('/')
    rtt1_data = float(rtt1_data[1])
    hops1 = traceroute(IP)
    hops1 = int(hops1)
    print >>sys.stderr, '\nCalculating the latency and hops from client to relay node ' + IP
    print >>sys.stderr, 'Average RTT from ' + IP + ' is: ' + str(rtt1_data)
    print >>sys.stderr, 'Number of hops from ' + IP + ' is: ' + str(hops1) + '\n'


    try:

        # Look for the response
        amount_received = 0
        amount_expected = len(message1+message2)
    
        while amount_received < amount_expected:

            rtt2= sock.recv(RECV_BUFFER_SIZE)
            amount_received += len(rtt2)
            print >>sys.stderr, '\nreceived from relay '+ IP + ' average RTT: ' + rtt2
            
            rtt2 = float(rtt2[0:])  

            sum_rtt = float(rtt2 + rtt1_data)
            print >>sys.stderr,'The sum of rtts for this path is "%.3f"' % sum_rtt
            q_relay_rtt.put(sum_rtt)

            hops2 = sock.recv(RECV_BUFFER_SIZE)
            amount_received += len(hops2)
            print >>sys.stderr, 'received from relay '+ IP + ' number of hops: ' + hops2
            hops2 = int(hops2[0:]) 
            sum_hops = int(hops2 + hops1)
            print >>sys.stderr,'The sum of hops for this path is "%d"' % sum_hops
            q_relay_hops.put(sum_hops)


            
            break
        
        len_relay_array = len(relay_array)  #oura gia epe3ergasia sum_rtt & sum_hops

        for i in range(len_relay_array):

            while not q_relay_rtt.empty():

                index = q_relay_rtt.get(i)
                arr_rtt.append(index)
                #q_relay_rtt.join()
        print "rtt array",arr_rtt
        print "minimum rtt",min(arr_rtt)

        #for z in range(len(arr_rtt)-1):
            #if arr_rtt[z] == arr_rtt[z+1]:
                #print "same indexes rtt are: ",arr_rtt[z],arr_rtt[z+1]

        for j in range(len_relay_array):

            while not q_relay_hops.empty():

                index = q_relay_hops.get(j)
                arr_hops.append(index)
                #q_relay_hops.join()
        print "hops array",arr_hops
        print "minimum hops",min(arr_hops)

        
   
        if criterion == "hops":

            print "min path for criterion hops is:",min(arr_hops)

            dup = [item for item, count in collections.Counter(arr_hops).items() if count > 1]
            print dup
            if dup == min(arr_hops):
                #return dup
                for dup in arr_hops:
                    pos=arr_hops.index(dup)
                    q2.put(pos)
                    while not q2.empty():
                        w = q2.get(dup)
                        hops_compare.append(w)
                    break
                print "criterion hops test",hops_compare


        elif criterion == "latency":
            #counter=0
            print "min path for criterion latency is:",min(arr_rtt)
            #print "position of min is :",
            return min(arr_rtt)
            #return arr_rtt.index(min(arr_rtt))
         
        sock.setblocking(0)
       
    finally:
        print"finally"


        
class ThreadWithReturnValue(Thread):

    def __init__(self, group=None, target=None, name=None,
                args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs, Verbose)
        self._return = None

    def run(self):
        if self._Thread__target is not None:
            self._return = self._Thread__target(*self._Thread__args,
                                               **self._Thread__kwargs)
    def join(self):
        Thread.join(self)
        return self._return

def bestPath(direct_values,final_relay_values):

    while direct_values and final_relay_values:

            if direct_values[0] < final_relay_values[0]:
                
                print "direct array best path",direct_values[0]

            elif direct_values[0] > final_relay_values[0]:
                
                print "relay array best path",final_relay_values[0]
        
    

#main body: reads the end server txt file with parsing argument -e
if len(sys.argv) >= 2:
    endserver = sys.argv[2]
    relay = sys.argv[4]
if sys.argv[1] == '-e' and sys.argv[3] == '-r':
    file1= open(endserver, 'r')
    file2 = open(relay, 'r')
    text1 = file1.read()
    text2 = file2.read()
    file1.close()
    file2.close()
    serverlist = text1.split()
    relaylist = text2.split()
    #print serverlist
else:
    print "Error! Wrong parameter!"

server_array = []
print "The available domains are:\n" #prints the available domains
for string in serverlist:
    print string   

relay_array = []
print "The available relay nodes are:\n" #prints the available domains
for relay in relaylist:
    print relay         

#asks for the alias and number of pings

alias, numofpings ,criterion= raw_input("\nPlease enter an alias,number of pings and the optimum route criterion of your choice (hops or latency): ").split(' ')
alias=alias.split("-").pop(0) #works when there is a - in the alias name

print alias,numofpings,criterion

#searching the correct server
for string in serverlist:
    if "www." in string:
        server_array.append(string[:-1]) #saving the domains without , in array
        #print "print serverarray",server_array

for relay in relaylist:

    if  re.search('\d+.\d+.\d+.\d+', relay):
        relay_array.append(relay[:-1])
        #print relay

arr=[]
arr_rtt = []
arr_hops = []
threads = []
final_relay_values = []
direct_values = []
last_direct_value = []
hops_compare=[]
q_relay_rtt = Queue.Queue()
q_relay_hops = Queue.Queue()
q_direct = Queue.Queue()
q = Queue.Queue()
q1 = Queue.Queue()
q2 = Queue.Queue()

for string1 in server_array:   
    #print string1    
    if "www."+alias+"." in string1:
        domain2 = string1
        #print "domain2",domain2
        t1 = ThreadWithReturnValue(target=direct_mode,args =(string,numofpings,criterion,q_direct))
        t1.start()
        print "The domain of the given alias is: " + domain2 + "\n"
        for relay in relay_array:
            IP=relay     
            twrv = ThreadWithReturnValue(target=relay_mode, args=(IP,domain2,q_relay_rtt,q_relay_hops,criterion))
            threads.append(twrv)
            threads.append(t1)
            twrv.start()
            #if len(threads) == len(relay_array):
               
            #print "deuterh print",t1.join()
            #for t in threads:
           
            for t in threads:
                q1.put(t1.join())
                while not q1.empty():
                    b=q1.get(t)
                    c,d =b
                    last_direct_value.append(c)
                    #print "final array direct",last_direct_value
                    #print "position of min rtt:",arr_rtt.index(min(arr_rtt))
                break
            #print "final direct last :",last_direct_value[0]
               
            for t in threads:
                q.put(twrv.join())
                while not q.empty():
                    a=q.get(t)
                    final_relay_values.append(a)
                    print "final array",final_relay_values
                    print "position of min rtt:",arr_rtt.index(min(arr_rtt))
                break
            #print "final relay last :",final_relay_values[-1]
            
        if last_direct_value[0] < final_relay_values[-1] :
            print "best path is direct path"
                
        else:
            print "best path is relay path",arr_rtt.index(min(arr_rtt))
                
                
                
                    
        break
        
if  "www."+alias+"." not in string1:   
    #else:
    print "Error!...This server does not exists in list!"
    print "End of program!"
        #break







