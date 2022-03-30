#testing the client.py
from Tkinter import *
from PIL import Image, ImageTk
import Tkinter as tk
import Tkinter, Tkconstants, tkFileDialog
import ttk
#from resizeimage import resizeimage
from threading import Thread
import socket
import sys
import subprocess
import re
import urllib
import threading
import requests
import time
import pyglet
import Queue
import collections
import os
import subprocess as sub
from threading import Timer
#import Tkinter.scrolledtext as tkst

RECV_BUFFER_SIZE = 32768



#supportive function to calculate the number of pings
def ping(host,numofpings):
    
    ping = subprocess.Popen(["ping6","-c",numofpings, host],stdout = subprocess.PIPE,stderr = subprocess.PIPE)#check if there is ipv6
    
    packet_loss = re.compile(', 100% packet loss,')
    out, error = ping.communicate()
    k = packet_loss.search(out)
    flag=0

    if error:
        print "This server does not have an IPv6"
        print "Using IPv4 to calculate..."
        ping = subprocess.Popen(["ping","-c",numofpings, host],stdout = subprocess.PIPE,stderr = subprocess.PIPE)
        out, error = ping.communicate()
        p_ipv4 = re.compile('(\d+.\d+.\d+.\d+)')
        Ip = p_ipv4.search(out)
        print Ip.group()
        k = packet_loss.search(out)
        if k : #tmp solution 
            flag=1
            print "100% packet loss.\nNo further information available.Please wait for download option."
            lat = "None"
            return Ip.group(),lat,out,flag
        else:
            flag=1
            matcherl = re.compile('/(\d+.\d+)')
            l = matcherl.search(out)
            print out #print to check ip
            print "Average RTT is:",l.group() #prints average rtt.
            return Ip.group(),l.group(),out,flag
    else:
        print "This server has an IPv6."
        print "Using IPv6 to calculate"
        server = re.compile(r'\((.*)\)')
        server_name = server.search(out)
        print server_name.group(1)
        if k : #tmp solution 
            print "100% packet loss.\nNo further information available.Please wait for download option."
            lat = "None"
            flag=0
            return server_name.group(1),lat,out,flag
        else:
            flag=0
            matcherl = re.compile('/(\d+.\d+)')
            l = matcherl.search(out)
            #print out #print to check ip
            print "Average RTT is:",l.group() #prints average rtt.
            return server_name.group(1),l.group(),out,flag



#supportive function to calculate the number of hops
def traceroute(domain,win,flag):

    count=0
    Sec = 0
    Min = 0
    quote = ""
    
    #text2.insert(END,'\nTraceroute results\n','color')
    traceroute = subprocess.Popen(["traceroute", '-w','10',domain],stdout=subprocess.PIPE, stderr=subprocess.PIPE) #traceroutes
    out, error = traceroute.communicate()
    p_ipv4 = re.compile('(\d+.\d+.\d+.\d+)')
    Ip = p_ipv4.search(out)
    print Ip.group()
    IP = re.compile(r'\((.*)\)')
    IP = IP.search(out)
    print IP.group(1)
    if Ip.group() == IP.group(1):
        print "trolll"
        flag=1
    timeloop=True
    while timeloop:
        for line in out:
            count+=count  
        timeloop = False  
    return IP.group(1),out,count,flag


def download_again(IP,string,flag):

    w=Tk()
    w.title("Try again?")
    Label(w, text="Do you want to download another file??", fg="#6699ff", bg="#00001a", font=18)
    ok_button = Button(w, text='Yes', width=20, command=download(IP,string,w,flag), fg= "#6699ff", bg = "#00001a",font=18)
    retry_button = Button(w, text='No', width=20, command=close, fg= "#6699ff", bg = "#00001a",font=18)

#supportive function that connects client with server
def connection(IP,port,alias,e,win,flag):


    if flag == 0:
        sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    elif flag == 1:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    else:  
        print "oops!"
    # Connect the socket to the port where the server is listening
    server_address = (IP, int(port))
    print >>sys.stderr, 'connecting to %s port %s' % server_address
    sock.connect(server_address)
    #photo_adr=raw_input( "Insert the address of photo to be downloaded: ")
    photo_adr = e.get()
    print alias
    try:
    
        retry = 'no'
        again = 'no'
        
        #photo_adr=raw_input( "Insert the address of photo to be downloaded: ")
        
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
                            #filepath = '/home/lumoswitch/Desktop/arxidia.png'

                            win.filename = tkFileDialog.asksaveasfilename(initialdir = "/",title = "Select file",filetypes = (("png files","*.png"),("jpg files","*.jpg"),("gif files","*.gif"),("all files","*.*")))
                            print (win.filename)
                            with open(win.filename, 'wb') as f:
                                f.write(response.content)
                            for y in range(21): #Loading progress bar
                                sys.stdout.write('\r')
                                sys.stdout.write("Loading:[%-20s] %d%%" % ('='*y, 5*y))
                                sys.stdout.flush()
                            #time.sleep(0.10)
                            
                            '''
                            pb = ttk.Progressbar(progress_win, orient="horizontal", length=200, mode="determinate")
                            pb.pack()
                            pb.start()
                            '''
                            print "\nImage downloaded!"
                            positive_win = Tk()
                            positive_win.title("Downloading success!")
                            positive_win.geometry("500x500")
                            Label(positive_win, text="Image downloaded!", fg="#6699ff", bg="#00001a", font=18)
                            
                            ok_button = Button(positive_win, text='Ok', width=20, command=download_again(IP,alias), fg= "#6699ff", bg = "#00001a",font=18)
                            retry_button = Button(positive_win, text='No', width=20, command=close, fg= "#6699ff", bg = "#00001a",font=19)
                            #pb.after(1, pb.stop())
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
                            negative_win = Tk()
                            negative_win.title("Oups!Something went wrong!")
                            Label(negative_win, text="Oups!...This address does not exist!...Parto alliws na mh ginei panikos!", fg="#6699ff", bg="black", font=18).pack()
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



def results_win(output,quote):

    window1 = Tk()
    window1.title("Results")
    window1.configure(background='black')
    #window1.pack()
    #window1.geometry("500x500")
    #window1.configure(background='black')
    text2 = Text(window1, height=28, width=110)
    scroll = Scrollbar(window1, command=text2.yview)
    text2.configure(yscrollcommand=scroll.set)
    text2.tag_configure('bold_italics', font=('Arial', 10, 'bold', 'italic'))
    text2.tag_configure('big', font=('Verdana', 10))
    text2.tag_configure('color', foreground='#476042', 
                        font=('Tempus Sans ITC', 12))
    text2.insert(END,'\nPing results\n','color')
    q = str(output)
    text2.insert(END, q)
    text2.insert(END, '--------------------------------------------------------------------------------------------------------------\n')
    text2.insert(END,'\nTraceroutes results\n','color')
    text2.insert(END,quote)
    text2.pack(side=LEFT)
    scroll.pack(side=RIGHT, fill=Y)


def download(IP,string,win,flag):
    
    
    Label(win, text="\nInsert the address of photo to be downloaded: ", fg="white", bg="#00001a", font=18).grid(row=15)
    e5 = Entry(win)
    e5.grid(row=15,column=1)
    b3 = Button(win, text="Download", command=lambda: connection(IP,80,string,e5,win,flag), bg="#00001a", fg="white",font=18).grid(row=18)
    

#supportive function:pings,traceroutes,prints the statistics using the criterion of user's choice and connects with server
def direct_mode(string,numofpings,criterion,win,alias):

    #Label(win, text="\nCalculations in progress...", fg="white", bg="#00001a", font=18).grid(row=10)
      

    #print "Ping is executed for direct mode..."
    IP ,latency, output, flag = ping(string,numofpings)
    
    #print "Traceroute for direct mode is executed in..."
    trace, quote, hops, flag= traceroute(IP,win,flag)
    
    if latency == "None":
        lat=0;
    else:
        final_lat = latency.split("/") #saves value without /
        print alias
        lat = float(final_lat[1])
    direct_values = [lat,trace]
    
    if flag == 0:
        print "Ip is IPv6"
    elif flag == 1:
        print "Ip is IPv4"
    Label(win, text="\nThe best path according to your" + " choice of criterion is the direct path " + "\n", fg="white", bg="#00001a", font=18).grid(row=12)
    Label(win, text="Average RTT for direct mode is: " + str(lat) + "\n", fg="white", bg="#00001a", font=18).grid(row=13)
    Label(win, text="Number of hops of direct mode are: " + str(hops) + "\n", fg="white", bg="#00001a", font=18).grid(row=13, column=1)
    b1 = Button(win, text="Show results", command=lambda: results_win(output,quote), bg="#00001a", fg="white",font=18).grid(row=14)
    b2 = Button(win, text="Proceed to download", command=lambda: download(trace,alias,win,flag), bg="#00001a", fg="white",font=18).grid(row=14, column=1)
    #print "Direct array: ",direct_values
    #return output,quote

    




"""
Function name: close
Purpose: makes the closes windows of the program
Arguments given: None
Values returned: None
"""
def close():

    window = Toplevel()
    window.title("Exit")
    l= Label(window, text="Leaving us so soon?", bg="black", fg="blue").pack()
    by = Button( window, text="Yes. I am done!", command=quit).pack()
    bn = Button(window, text="Of course not", command=window.destroy).pack()
    window.geometry("150x100")

"""
Function name: create_menu
Purpose: makes the menu window of the program
Arguments given: None
Values returned: None
"""
def create_menu(window):

    menubar = Menu(window)
    filemenu = Menu(menubar, tearoff=0)
    helpmenu = Menu(menubar, tearoff=0)

    filemenu.add_command(label="Exit", command=close)
    menubar.add_cascade(label="File", menu=filemenu)


    helpmenu.add_command(label="Program manual", command=create_manwindow)
    helpmenu.add_command(label="About us", command=create_infowindow)
    menubar.add_cascade(label="About", menu=helpmenu)

    return menubar


"""
Function name: create_manwindow
Purpose: makes the manual window of the program
Arguments given: None
Values returned: None
"""
def create_manwindow():

    window = Toplevel()
    window.title("Manual")
    window.geometry("500x500")
    #window.configure(background='black')

    path = "photo1.jpg"
    img = ImageTk.PhotoImage(Image.open(path)) #Creates a Tkinter-compatible photo image, which can be used everywhere Tkinter expects an image object.
    #img = img.resize((250, 250), Image.ANTIALIAS)
    panel = Label(root, image = img, bg="black") #The Label widget is a standard Tkinter widget used to display a text or image on the screen.
    #panel.config(background='black')
    panel.place(relwidth=0, relheight=0, width=0, height=0)
    panel.pack(fill = BOTH, expand = "1")


"""
Function name: create_infowindow
Purpose: makes the information window of the program
Arguments given: None
Values returned: None
"""
def create_infowindow():

    window = Tk()
    window.title("Know us better")
    window.geometry("500x500")
    window.configure(background='black')


    var1 = StringVar()
    label2 = Label( window, textvariable=var1, fg="black", bg="blue" )
    label2.config(text=str(var))
    var1.set("Coming soon")
    label2.pack()



"""
Function name: checker_function
Purpose: takes values from user
Arguments given: None
Values returned: None
"""
def checker_function(e1,e2,e3,win,serverlist,server_array,relaylist,relay_array,string):
    
    alias = e1.get()
    numofpings = e2.get()
    criterion = e3.get()
    d_values = []
    
    for string in server_array:    
        if "www."+alias+"." in string:
            domain2 = string
            print "The domain of the given alias is: " + string + "\n"
            Label(win, text="Alright then.You chose to download from " + alias + "\n server with " + numofpings +
                " number of iterations and using " + criterion + "\n as your choice criterion", fg="white", bg="#00001a", font=18).grid(row=8)
            Label(win, text="\nLet us find the best path according to your choice of criterion", fg="white", bg="#00001a", font=18).grid(row=9)
            b4 = Button(win, text="Ok! Start calculations!", command=lambda: direct_mode(domain2,numofpings,criterion,win,alias), bg="#00001a", fg="white",font=18).grid(row=9, column=1)
            break
    if "www."+alias+"." not in string:   
        print "Error!...This server does not exists in list!"
        print "End of program!"
        Label(win, text="We are sorry but this server does not exist in our list", fg="#6699ff", bg="black", font=18).grid(row=20)
   

    
"""
Function name: create_main_window
Purpose: makes the main window of the program
Arguments given: None
Values returned: None
"""
def create_main_window():

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

    #searching the correct server
    server_array = []
    print "The available domains are:\n" #prints the available domains
    for string in serverlist:
        print string
        if "www." not in string:
            alias=server_array.append(string[:-4])#saves only the alias

    relay_array = []
    for string in serverlist:
        if "www." in string:
            server_array.append(string[:-1]) #saving the domains without , in array

    for string in serverlist:
        if "www." in string:
            server_array.append(string[:-1]) #saving the domains without , in array

    for relay in relaylist:
        if re.search('\d+.\d+.\d+.\d+', relay):
            relay_array.append(relay[:-1])
            #print relay


    window = Toplevel()
    window.title("Anomwork")
    window.configure(background='#00001a')
    

    #Printing a txt file in a window
    Label(window, text="Welcome to our main page. Here you will be able to download easily any image of your choice. Just follow the instructions", fg="white",font=18, bg="#00001a").grid(row=1)
    Label(window, text="Let's start! Please fill in the following information:\n", fg="white", bg="#00001a",font=18).grid(row=2)
    
    e1 = Entry(window)
    e2 = Entry(window)
    e3 = Entry(window)
    Label(window, text="Enter an alias:", fg="white", bg="#00001a",font=18).grid(row=3)
    e1.grid(row=3 , column=1)
    Label(window, text="The number of iterations:",fg="white", bg="#00001a",font=18).grid(row=4)#.pack(side=TOP,anchor=W)
    e2.grid(row=4, column=1)
    Label(window, text="The optimum route criterion of your choice(hops or latency):",fg="white", bg="#00001a",font=18).grid(row=5)#.pack(side=TOP,anchor=W)
    e3.grid(row=5, column=1)


    
   
    b = Button(window,text="Enter", command=lambda: checker_function(e1,e2,e3,window,serverlist,server_array,relaylist,relay_array,string), bg='#00001a', fg="white",font=18).grid(row=6, column=1)#.pack()
    
    menubar = create_menu(window)
    window.config(menu=menubar)
    window.geometry("1500x1500")



    


root = Tk()
root.title("Anomwork") #naming the window
root.configure(background='black')

#Display welcome message
var = StringVar()
label1 = Label( root, textvariable=var, fg="black" )
label1.config(text=str(var))

#label1.config(width=200)
var.set("Welcome to our platform!\nThis project was designed to make image downloading more efficient.\nWe hope you will find it useful.\nEnjoy!\n---The Creators---")
label1.config(font=(var, 18));
label1.pack(side=TOP)
label1.config(background= 'black',fg='#FFF2D9')

#Display welcome photo
path = "photo1.jpg"
img = ImageTk.PhotoImage(Image.open(path)) #Creates a Tkinter-compatible photo image, which can be used everywhere Tkinter expects an image object.
#img = img.resize((250, 250), Image.ANTIALIAS)
panel = Label(root, image = img, bg="black") #The Label widget is a standard Tkinter widget used to display a text or image on the screen.
#panel.config(background='black')
panel.place(relwidth=0, relheight=0, width=0, height=0)
panel.pack(fill = BOTH, expand = "1") #The Pack geometry manager packs widgets in rows or columns.


#Placing an enter button and exit button
enter_button = Button(root, text='Press to enter', width=20,command= create_main_window, fg= "#6699ff", bg = "black",font=18)
close_button = Button(root, text='Exit', width=20, command=close, fg= "#6699ff", bg = "black",font=18)

enter_button.place(x=5, y=0)
close_button.place(x=10,y=0)


enter_button.pack()
close_button.pack()
root.geometry("1500x1500")
root.mainloop()



