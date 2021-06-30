# What is PyText?

PyText is a simple and a free TXT editor and Notepad replacement that supports natural languages. PyText allows you to quickly and easily write information without any problems. Running in the MS Windows and Linux environment, its use is governed by [GPL License](/LICENSE).

See the [PyText official presentation](/misc/docs/pres.pptx) (Russian) for more information.

## Dependencies
PyText depends by
- **Python 3.4** and above;
- **/tkinter** – graphical user interface (GUI);
- **/Pil** works with images;
- **/os** manage files.
- **/re** builds pattern for line args
- **/optparse** parses line arguments

To install the necessary libraries:
```pip3 install -r requirements.txt```
or
```pip3 install Pillow```

Download the latest version of the Python [there](https://www.python.org/downloads/).

## Supported OS
The latest Windows and Linux systems are supported by PyText.

## Screenshots
![Main Window (white theme)](/misc/pics/Screen1.png)
![Main Window (dark theme)](/misc/pics/Screen2.png)

## Getting Started
For end users, the latest Windows and Linux version of PyText is available from this repository. More information for interested users is available from the [PyText official presentation](/misc/pres.pptx) (Russian).

## Using command line
PyText supports (Unix and Linux) command line arguments with several options:

Usage: 1)main.py [options] args 2)main.py arg1(-f) arg2(-o)

-h, --help to — to get help message
-f, -F, --file_in — opens file.txt(if using only -f opt) or (with -o) opens file.txt, copies all and puts to the new file
-o, -O, --file_out — opens new/existed file(rewrites all)  
=======
