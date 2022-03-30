#testing the client.py
import socket
import sys
import subprocess
import re
import urllib
import requests
import time
#import pyglet



RECV_BUFFER_SIZE = 32768



#supportive function to calculate the number of pings
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
        
    print (str(Min) + " mins" +" " + str(Sec) + " sec")
        
    #print "Number of hops:",count
    return count

    
#supportive function that connects client with server
def connection(IP,port):
    #Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connect the socket to the port where the server is listening
    server_address = (IP, int(port))
    print >>sys.stderr, 'connecting to %s port %s' % server_address
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
def server_functions(string,numofpings,criterion):

    print "Ping is executed..."
    IP ,latency= ping(string,numofpings)
    print "Ping done"
    print "Traceroute is executed in..."
    trace = traceroute(IP)
    if criterion == 'hops':
        print "Number of hops: ",trace
    elif criterion == 'latency':
        print "Average RTT is: ",latency
    print "Tracetoute done"
    print "Connection stage in progress..."
    connection(IP,80)

    

#main body: reads the end server txt file with parsing argument -e
if len(sys.argv) >= 2:
    endserver = sys.argv[2]
if sys.argv[1] == '-e':
    file= open(endserver, 'r')
    text = file.read()
    file.close()
    serverlist = text.split()
    #print serverlist
else:
    print "Error! Wrong parameter!"

server_array = []
print "The available domains are:\n" #prints the available domains
for string in serverlist:
    print string           

#asks for the alias and number of pings
alias, numofpings ,criterion= raw_input("\nPlease enter an alias,number of pings and the optimum route criterion of your choice(hops or latency): ").split(' ')
alias=alias.split("-").pop(0) #works when there is a - in the alias name

print alias,numofpings,criterion

#searching the correct server
for string in serverlist:
    if "www." in string:
        server_array.append(string[:-1]) #saving the domains without , in array

if string in serverlist:
    for string in server_array:       
        if "www."+alias+"." in string:
            print string
            server_functions(string,numofpings,criterion)
            break
else:   
    print "Error!...This server does not exists in list!"
    print "End of program!"


