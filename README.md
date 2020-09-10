# WindowsPrinterGUI
Using the widows GUI to send file to remote linux printer, and print the file

![Printer](https://github.com/haidi-ustc/WindowsPrinterGUI/blob/master/printer.png)

### how to use

Install relative package on the windows

```
pip install PyInstaller
pip install pycrypto
pip install paramiko
```

Then convert python program to .exe 

```
pyinstaller -F -w printer.py 
```
