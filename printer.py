#--coding-- utf-8
import os
from tkinter import *
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import paramiko

HOST="0.0.0.0"
PORT=22
USERNAME='xxx'
PWD='123456'
remote_foler="/home/xxx/"


def get_source(self):
    """Clears the current entry box, then replaces it with
    the selected file path.
    """
    self.text_source.delete(0, 60)
    self.custom_source = filedialog.askopenfilename()
    self.text_source.insert(0, self.custom_source)


def safeclose(self):
    """Asks user if they would like to quit the application,
    and if so, kills the program.
    """
    if messagebox.askokcancel("Exit Program",
                              "Are you sure you want to close the application?"):
        self.master.destroy()
        os._exit(0)

def print_files(self,filename, checkval):
    ftp=FileTrans()
    ftp.run(filename)
    ftp.print(checkval)

class FileTrans(object):

    def __init__(self):
        self.host = HOST
        self.port = PORT
        self.username = USERNAME
        self.pwd = PWD

    def run(self,filename):
        self.connect()
        self.Upload(filename=filename)
        self.close()

    def connect(self):
        transport = paramiko.Transport((self.host, self.port))
        transport.connect(username=self.username, password=self.pwd)
        self.__transport = transport
    def close(self):
        self.__transport.close()

    def Upload(self,filename):
        basename=os.path.basename(filename)
        basename=basename.split('\\')[-1]
        #remeber to change the director here !!!
        self.remote_filename=remote_foler+basename
        sftp = paramiko.SFTPClient.from_transport(self.__transport)
        sftp.put(filename, self.remote_filename)

    def print(self,checkval):
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(self.host,self.port, self.username, self.pwd)

        if checkval==0:
           cmd="lp %s"%(self.remote_filename)
        else:
           cmd="lp -o sides=two-sided-long-edge %s"%(self.remote_filename)

        std_in, std_out, std_err = ssh_client.exec_command(cmd)


def load_gui(self):
    """ Populate the master Frame with the correct buttons
    and Tkinter widgets placed with grid geometry.
    """
    # create an entry text box for source button
    self.custom_source = StringVar()
    # set text box to a default string
    self.custom_source.set('select a file')
    # set the width to 60 characters
    self.text_source = tk.Entry(self.master, width=60, textvariable=self.custom_source)
    print(self.text_source)
    self.text_source.grid(row=0, column=0, rowspan=1, columnspan=2, padx=(5, 0),
                          pady=(10, 20))

    # create an entry text box for destination button
    #self.custom_dest = StringVar()
    ## set text box to a default string
    #self.custom_dest.set('Select a destination directory')
    ## set the width to 60 characters
    #self.text_dest = tk.Entry(self.master, width=60, textvariable=self.custom_dest)
    #self.text_dest.grid(row=1, column=0, rowspan=1, columnspan=1, padx=(5, 0), pady=(10, 20))

    # 
    self.CheckVar = IntVar()
    self.C1 = Checkbutton(self.master, text = r"double page", variable = self.CheckVar, height=5, onvalue= 1, width = 15)
                 #onvalue = 1, offvalue = 0, height=5, \
                 #width = 20)
    self.C1.grid(row=1, column=0, rowspan=1, columnspan=1, padx=(0, 0), pady=(10, 20))
    print(self.CheckVar.get())
    #self.C1.pack()
    # create and place a source button
    self.button_source = tk.Button(self.master, width=12, height=1, text="文件",
                                   command=lambda: get_source(self))
    self.button_source.grid(row=0, column=2, padx=(10, 0), pady=(10, 20))

    # create and place a destination button
    #self.button_dest = tk.Button(self.master, width=12, height=1, text="Destination",
    #                             command=lambda: file_xfer_func.get_dest(self))
    #self.button_dest.grid(row=1, column=2, padx=(10, 0), pady=(10, 20))
    
    # create and place a transfer button
    self.button_transfer = tk.Button(self.master, width=16, height=2, text="打印",
                                command=lambda: print_files(self, self.custom_source, self.CheckVar.get()))
                                
    self.button_transfer.grid(row=2, column=0, padx=(0, 0), pady=(10, 10))

    # create and place a done button
    self.button_done = tk.Button(self.master, width=16, height=2, text="退出",
                                 command=lambda: safeclose(self))
    self.button_done.grid(row=2, column=1, padx=(0, 0), pady=(10, 10))

class ParentWindow(Frame):
    def __init__(self, master, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)

        # define max and min size of frame
        self.master = master
        self.master.minsize(600, 230)
        self.master.maxsize(600, 230)
        # give the master frame a name
        self.master.title(u"私人订制打印机")
        # give it a background color
        self.master.configure(bg="#F0F0F0")

        load_gui(self)


if __name__ == "__main__":
    root = tk.Tk()
    App = ParentWindow(root)
    root.mainloop()
