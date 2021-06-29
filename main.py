#!/usr/bin/env python3
#! -*- coding: UTF-8 -*-
"""
Docs of PyText editor
Editing lang: any(but shortcuts available only for EN)

"""
from sys import exit
from tkinter import *
from tkinter.font import Font, ITALIC, ROMAN, families
from tkinter.ttk import *
from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog import askopenfilename, asksaveasfilename #open, save file
from tkinter.messagebox import askquestion, showerror, showinfo, showwarning, askyesno #Query and messages
from tkinter.simpledialog import askstring
from PIL import Image
import PIL.ImageTk
import os
from os.path import basename, normpath, exists, join


class app(Tk):
    def __init__(self, parent=None):
        Tk.__init__(self, parent)
        self.init_UI()

    def init_UI(self):
        self.file_status = 'UNSAVED'    #file status
        self.get_file = ''  #actual file name
        self.title(f'{self.get_file} PyText editor')

        windowWidth = self.winfo_reqwidth()                                     #get window properties
        windowHeight = self.winfo_reqheight()                                   #
        self.positionRight = int(self.winfo_screenwidth()/2.5 - windowWidth/2)  #calc pos
        self.positionDown = int(self.winfo_screenheight()/3 - windowHeight/2)   #
        self.geometry(f'640x480+{self.positionRight}+{self.positionDown}')      #set pos
        self.resizable(True, True)                                              #

        self.protocol('WM_DELETE_WINDOW', self.on_exit)
        try:
            self.iconbitmap(normpath('.\misc\pics\pytext_icon.ico'))
        except:
            pass

        #font constants
        self.defaultfont = Font(family='Curier', weight='normal', size=12, slant=ROMAN, underline=False, overstrike=False)
        self.deffont = StringVar()
        self.deffont.set(self.defaultfont.cget('family'))
        self.deftype = StringVar()
        self.deftype.set(self.defaultfont.cget('weight'))
        self.defsize = StringVar()
        self.defsize.set(self.defaultfont.cget('size'))
        self.defslant = StringVar()
        self.defslant.set(self.defaultfont.cget('slant'))
        self.defundln = StringVar()
        self.defundln.set(self.defaultfont.cget('underline'))
        self.deffonts = [fam for fam in list(families())]
        self.deftypes = ['bold', 'normal']
        self.defsizes = [i for i in range(10, 50, 2)]
        self.defslants = [ROMAN, ITALIC]
        self.defundlns = [1, 0]
        #font constants

        #main tk grid set
        self.grid()
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        #main tk grid set

        #main frame grid set
        self.mainFrame = Frame(master=self)
        self.mainFrame.grid(column=0, row=0, sticky=NSEW)
        self.mainFrame.grid_columnconfigure(0, weight=1)
        self.mainFrame.grid_rowconfigure(0, weight=1)
        #main frame grid set

        #pop out menu #all functions moved to showPopOut because of bug with touchpad
        self.PopOutMenu = Menu(master=self, tearoff=0)
        self.grid()
        #pop out menu

        #menu bar
        self.mainMenu = Menu(self, tearoff=0)
        self.config(menu=self.mainMenu)
        self.toolsMenu = Menu(self.mainMenu, tearoff=0)
        self.toolsMenu.add_command(label='Replace', command=self.Replace)        
        self.toolsMenu.add_command(label='Search', command=self.Search)
        self.FileMenu = Menu(self.mainMenu, tearoff=0)
        self.FileMenu.add_command(label='Open file', command=self.file_open)
        self.FileMenu.add_command(label='Save file as', command=self.file_save_as)
        self.FileMenu.add_command(label='Save', command=self.Save)
        self.mainMenu.add_cascade(label='File', menu=self.FileMenu)
        self.mainMenu.add_separator()
        self.mainMenu.add_command(label='Settings', command=self.Settings)
        self.mainMenu.add_separator()
        self.mainMenu.add_cascade(label='Tools', menu=self.toolsMenu)
        self.mainMenu.add_separator()
        self.mainMenu.add_command(label='About', command=self.About)
        self.var_th = IntVar()
        self.var_th.set(0)
        self.mainMenu.add_checkbutton(label='theme', variable=self.var_th, command=self.theme_ch)
        #menu bar

        #text frame grid set
        self.text = ScrolledText(master=self.mainFrame)
        self.text.grid(row=0, column=0, sticky=NSEW)
        self.text.grid_columnconfigure(0, weight=1)
        self.text.grid_rowconfigure(0, weight=1)
        self.text.configure(font=self.defaultfont)
        #text frame grid set

        self.cur_text = self.text.get('1.0', END)   #for check the status
        self.copiedtxt = ''

        #global shorcuts bind en
        self.bind('<Button-3>', self.showPopOut)    #do not change
        self.bind('<Control-Key-f>', self.Search)
        self.bind('<Control-Shift-H>', self.Replace)
        self.bind('<Control-Key-a>', self.select_all)
        self.bind('<Control-Key-l>', self.select_line)
        self.bind('<Control-Key-x>', self.Cut)
        self.bind('<<Copy>>', self.Copy)    ###
        self.bind('<<Paste>>', self.Paste)  ###double paste issue
        self.bind('<Control-Shift-V>', self.Paste)  #added temporarily
        self.bind('<Control-KeyPress-s>', self.Save)
        self.bind('<Control-Key-o>', self.file_open)
        self.bind('<Control-Shift-S>', self.file_save_as)
        self.bind('<KeyPress>', self.on_key_press)
        self.bind_all('<Control-equal>', self.incFont)
        self.bind_all('<Control-minus>', self.decFont)
        self.bind('<Insert>', self.Paste)
        self.bind('<Delete>', self.Cut)
        self.text.bind('<Button-1>', self.on_tap)
        #repeat for big letters
        self.bind('<Control-Key-F>', self.Search)
        self.bind('<Control-Key-A>', self.select_all)
        self.bind('<Control-Key-L>', self.select_line)
        self.bind('<Control-Key-X>', self.Cut)
        self.bind('<Control-Key-C>', self.Copy)
        self.bind('<Control-Key-V>', self.Paste)
        self.bind('<Control-KeyPress-S>', self.Save)
        self.bind('<Control-Key-O>', self.file_open)
        self.bind('<Control-Shift-S>', self.file_save_as)

        #global binds (any lang) doesnt work/no support from tk
        self.__check_parse()

    def __check_parse(self):
        self.get_file_path = os.path.join(os.getcwd(), out_file_name)
        self.title('{} PyText editor'.format(basename(self.get_file_path)))
        self.get_file = basename(self.get_file_path)
        if in_file_name != '' and os.path.exists(os.path.join(os.getcwd(), in_file_name)) and self.get_file != '':

            with open(self.get_file_path, 'w', encoding='utf-8') as f:
                    f.close()
            with open(in_file_name, 'r', encoding='utf-8') as f:
                ftext = f.readlines()
                on_out_ext = ''.join(ftext)
            self.text.delete('1.0', END)
            self.text.insert(END, on_out_ext)
            self.cur_text = self.text.get('1.0', END)
            self.text.mark_set(INSERT, '1.0') # set cursor at start
            self.text.focus() #instead of click
            with open(self.get_file_path, 'w', encoding='utf-8') as f:
                    to_write_text = self.text.get('1.0', END).split('\n')
                    for (ids, line) in enumerate(to_write_text):
                        to_write_text[ids] += '\n'
                    f.writelines(to_write_text)
            self.cur_text = self.text.get('1.0', END)
            self.file_status = 'SAVED'
            self.get_file_path = os.path.join(os.getcwd(), out_file_name)
            self.get_file = basename(self.get_file_path)
            self.title('{} PyText editor'.format(basename(self.get_file_path)))
        if in_file_name != '' and os.path.exists(os.path.join(os.getcwd(), in_file_name)) and out_file_name == '':
            with open(in_file_name, 'r', encoding='utf-8') as f:
                ftext = f.readlines()
                on_out_ext = ''.join(ftext)
            self.text.delete('1.0', END)
            self.text.insert(END, on_out_ext)
            self.cur_text = self.text.get('1.0', END)
            self.text.mark_set(INSERT, '1.0') # set cursor at start
            self.text.focus() #instead of click
            self.file_status = 'SAVED'
            self.get_file_path = os.path.join(os.getcwd(), in_file_name)
            self.get_file = basename(self.get_file_path)
            self.title('{} PyText editor'.format(basename(self.get_file_path)))

        if out_file_name != '' and os.path.exists(os.path.join(os.getcwd(), out_file_name)) and in_file_name == '':
            self.file_status = 'UNSAVED'
            self.get_file_path = os.path.join(os.getcwd(), out_file_name)
            self.get_file = basename(self.get_file_path)
            self.title('{} PyText editor'.format(basename(self.get_file_path)))
            with open(out_file_name, 'w', encoding='utf-8') as f:
                f.write('')
            self.text.delete('1.0', END)
            self.cur_text = self.text.get('1.0', END)
            self.text.mark_set(INSERT, '1.0') # set cursor at start
            self.text.focus() #instead of click

            

    def theme_ch(self, *event):
        if self.var_th.get() == 0:
            self.text.config(insertbackground='#000')
            self.mainMenu.config(bg='#ffffff', fg='#c3d9e5')
            self.PopOutMenu.config(bg='#2d333b', fg='#adbac7')
            self.text.config(bg='#ffffff', fg='#000000')
            
        elif self.var_th.get() == 1:
            self.text.config(insertbackground='#fff')
            self.mainMenu.config(bg='#2d333b', fg='#c3d9e5')
            self.PopOutMenu.config(bg='#2d333b', fg='#adbac7')
            self.text.config(bg='#1e2228', fg='#adbac7')

    def showPopOut(self, event):
        self.PopOutMenu.delete(0, END)
        self.PopOutMenu.add_command(label='Select all', command=self.select_all)
        self.PopOutMenu.add_command(label='Copy', command=self.Copy)
        self.PopOutMenu.add_command(label='Paste', command=self.Paste)
        self.PopOutMenu.add_command(label='Cut', command=self.Cut)
        self.PopOutMenu.add_command(label='Seacrh', command=self.Search)
        self.PopOutMenu.post(event.x_root, event.y_root)
    #needs for pop out menu
    def on_tap(self, event=None):
        """implemented for linux system to avoid a bug with pop out menu"""
        self.PopOutMenu.delete(0, END)

    def on_key_press(self, event=None):
        """tracks file status and put '*' if file wasn\'t saved"""
        if '*' not in self.title():
            if self.cur_text != self.text.get('1.0', END):
                self.title(f'*{self.get_file} PyText editor')
        else:
            if self.cur_text == self.text.get('1.0', END):
                self.title(f'{self.get_file} PyText editor')

    def incFont(self, event=None):
        self.defaultfont['size'] += 2

    def decFont(self, event=None):
        if int(self.defaultfont.cget('size')) > 12:
            self.defaultfont['size'] -= 2

    def select_all(self, event=None):
        self.text.tag_add(SEL, '1.0', END)
        self.text.mark_set(INSERT, END)
        self.text.see(INSERT)
        self.text.focus()
    
    def select_line(self, event=None):
        self.text.tag_add(SEL, 'insert linestart', 'insert lineend')
        self.text.mark_set(INSERT, 'insert lineend')
        self.text.see(INSERT)
        self.text.focus()

    def Copy(self, event=None):
        self.copiedtxt = self.text.selection_get()#(SEL_FIRST, SEL_LAST)
        self.clipboard_clear()
        self.clipboard_append(self.copiedtxt)
        self.text.tag_remove(SEL, SEL_FIRST, SEL_LAST)

    def Paste(self, event=None):
        try:    #if clipboard is empty
            # ToInsert = self.clipboard_get()
            self.text.insert(INSERT, self.copiedtxt)
        except TclError:
            pass

    def Search(self, event=None):
        target = askstring(title='Search', prompt='Find')
        if target:
            targets = []
            pos = '1.0'
            while self.text.search(target, pos, END) != '':
                tgst = self.text.search(target, pos, END)   #tgst - target start
                tgstpast = tgst + ('+%dc' % len(target))
                targets.append((tgst, tgstpast))
                pos = tgstpast

            self.curind = 0

            if len(targets) != 0:
                self.text.tag_add(SEL, targets[0][0], targets[0][1])

            def on_exit():
                searchWindow.destroy()
                self.text.focus()
            
            #ressx is a copy of targets
            def on_prev(ressx=targets):
                if ressx[self.curind] != ressx[0]:
                    self.text.tag_remove(SEL, '1.0', END)
                    self.curind -= 1
                    curpos = ressx[self.curind]
                    self.text.tag_add(SEL, curpos[0], curpos[1])
                    self.text.mark_set(INSERT, curpos[1])
                    self.text.see(INSERT)
                    self.text.focus()
                else:
                    pass

            def on_next(ressx=targets):
                if ressx[self.curind] != ressx[-1]:
                    self.text.tag_remove(SEL, '1.0', END)
                    self.curind += 1
                    curpos = ressx[self.curind]
                    self.text.tag_add(SEL, curpos[0], curpos[1])
                    self.text.mark_set(INSERT, curpos[1])
                    self.text.see(INSERT)
                    self.text.focus()
                else:
                    pass

            searchWindow = Toplevel(master=None)
            searchWindow.geometry(f'220x40+{int(self.positionRight/2)}+{int(self.positionDown)}')
            searchWindow.resizable(False, False)
            Button(master=searchWindow, text='Prev', command=on_prev).pack(side=LEFT, fill=BOTH)
            Button(master=searchWindow, text='Next', command=on_next).pack(side=RIGHT, fill=BOTH)
            searchWindow.protocol('WM_DELETE_WINDOW', on_exit)

        else:
            pass
            # showwarning(title='Failed', message='Wrong input')

    def Replace(self, event=None):
        target_old = askstring(title='Replace', prompt='What to replace:')
        if target_old:
            target_new = askstring(title='Replace', prompt='Enter the replace:')
            cp_text = self.text.get('1.0', END)
            if target_old in cp_text:
                cp_text = cp_text.replace(target_old, target_new)
                self.text.delete('1.0', END)
                self.text.insert(END, cp_text)
            else:
                showerror(title='error', message='Nothing to replace/wrong target')

    def Cut(self, event=None):
        try:    #if nothing was selected
            ToCut = self.text.get(SEL_FIRST, SEL_LAST)
            self.text.delete(SEL_FIRST, SEL_LAST)
            self.clipboard_clear()
            self.clipboard_append(ToCut)
        except:
            pass

    def file_open(self, event=None):
        self.get_file_path = askopenfilename()
        if self.get_file_path != '':                  #checks for void src
            self.title('{} PyText editor'.format(basename(self.get_file_path)))
            with open(self.get_file_path, 'r', encoding='utf-8') as f:
                ftext = f.readlines()
                on_out_ext = ''.join(ftext)
            self.text.delete('1.0', END)
            self.text.insert(END, on_out_ext)
            self.text.mark_set(INSERT, '1.0') # set cursor at start
            self.text.focus() #instead of click
            self.file_status = 'OPENED'
            self.get_file = basename(self.get_file_path)
        else:
            # showwarning(title='Empty path', message='No file was chosen')
            pass

    def file_save_as(self, event=None):
        file_types = [('Text Document', '*.txt'), ('File', '*.*')]   #allowed file types
        self.get_file_path = asksaveasfilename(filetypes = file_types, defaultextension = file_types, ) #get new file path

        if self.get_file_path != '':                        #checks for void src
                self.title('{} PyText editor'.format(basename(self.get_file_path)))
                with open(self.get_file_path, 'w', encoding='utf-8') as f:
                    to_write_text = self.text.get('1.0', END).split('\n')
                    for (ids, line) in enumerate(to_write_text):
                        to_write_text[ids] += '\n'
                    f.writelines(to_write_text)
                self.file_status = 'SAVED'                                      #file status
                self.title(f'{self.get_file} PyText editor')
                showinfo(title='Message', message='File was successfully saved')
        else:
            self.file_status = 'UNSAVED'
            # showwarning(title='Empty path', message='No file was set')

    def Save(self, event=None):
        if self.file_status == 'UNSAVED' or self.get_file == '':
            self.file_save_as()

        elif self.cur_text != self.text.get('1.0', END):
            with open(self.get_file_path, 'w', encoding='utf-8') as f:
                    to_write_text = self.text.get('1.0', END).split('\n')
                    for (ids, line) in enumerate(to_write_text):
                        to_write_text[ids] += '\n'
                    f.writelines(to_write_text)
            self.cur_text = self.text.get('1.0', END)
            self.file_status = 'SAVED'
            self.title(f'{self.get_file} PyText editor')
        else:
            pass
        
    def Settings(self, event=None):
        def on_quit():
            settingsFrame.grab_release()
            settingsFrame.destroy()
        ####
        settingsFrame = Toplevel(master=None)
        settingsFrame.title('Settings')
        # settingsFrame.geometry(f'10x10+{self.positionRight}+{self.positionDown}')
        settingsFrame.resizable(False, False)
        settingsFrame.grid()
        settingsFrame.columnconfigure(0, pad=20, weight=1)
        settingsFrame.columnconfigure(1, pad=20, weight=1)
        settingsFrame.columnconfigure(2, pad=20, weight=1)
        settingsFrame.columnconfigure(3, pad=20, weight=1)
        settingsFrame.columnconfigure(4, pad=20, weight=1)
        settingsFrame.rowconfigure(0, pad=20, weight=1)
        settingsFrame.rowconfigure(1, pad=20, weight=1)

        def font(*event):
            self.defaultfont['family'] = self.deffont.get()

        def types(*event):
            self.defaultfont['weight'] = self.deftype.get()

        def size(*event):
            self.defaultfont['size'] = int(self.defsize.get())

        def slant(*event):
            self.defaultfont['slant'] = self.defslant.get()

        def underline(*event):
            self.defaultfont['underline'] = self.defundln.get()

        ####
        ####
        #Font
        Label(master=settingsFrame, text='Font').grid(row=0, column=0, sticky=EW)
        lbFontSt = OptionMenu(settingsFrame, self.deffont, self.deffont.get(), *self.deffonts, command=font)    #master, def, def init,...
        lbFontSt.grid(row=1, column=0, sticky=NSEW)
        #Font-style
        Label(master=settingsFrame, text='Font style').grid(row=0, column=1, sticky=EW)
        lbFontTp = OptionMenu(settingsFrame, self.deftype, self.deftype.get(), *self.deftypes, command=types)
        lbFontTp.grid(row=1, column=1, sticky=NSEW)
        #Font-size
        Label(master=settingsFrame, text='Size').grid(row=0, column=2, sticky=EW)
        lbFontSz = OptionMenu(settingsFrame, self.defsize, self.defsize.get(), *self.defsizes, command=size)
        lbFontSz.grid(row=1, column=2, sticky=NSEW)
        #Slant
        Label(master=settingsFrame, text='Slant').grid(row=0, column=3, sticky=EW)
        lbFontSz = OptionMenu(settingsFrame, self.defslant, self.defslant.get(), *self.defslants, command=slant)
        lbFontSz.grid(row=1, column=3, sticky=NSEW)
        #UnderLine
        Label(master=settingsFrame, text='Underline').grid(row=0, column=4, sticky=EW)
        lbFontSz = OptionMenu(settingsFrame, self.defundln, self.defundln.get(), *self.defundlns, command=underline)
        lbFontSz.grid(row=1, column=4, sticky=NSEW)

        Button(master=settingsFrame, text='Close', command=on_quit).grid(row=2, column=2, columnspan=2, sticky=NSEW)
        ####
        
        #on exit
        settingsFrame.protocol('WM_DELETE_WINDOW', on_quit)
        settingsFrame.focus_set()
        settingsFrame.grab_set()
        #

    def About(self, event=None):
        def on_quit():
            aboutFrame.grab_release()
            aboutFrame.destroy()
            # self.deiconify()  #reveal editor

        # self.iconify()  #hide editor
        aboutFrame = Toplevel()
        aboutFrame.geometry(f'400x450+{self.positionRight}+{self.positionDown}')
        aboutFrame.resizable(False, False)

        # path = askopenfilename()#need to find a file
        ####do not change!!!
        try:
            img = PIL.ImageTk.PhotoImage(Image.open(normpath('.\misc\pics\qrcode_github.com.png')))
            pic = Label(aboutFrame, image=img)
            pic.image = img
            pic.pack(expand=False)
        except:
            pass
            # print('missing qr code pic/cannot find')
        ####
        Label(master=aboutFrame, text='Project: PyText editor\nCreated on 2021').pack(expand=False)
        Button(master=aboutFrame, text='Close', command=on_quit).pack(expand=False)
        # aboutFrame.protocol('WM_ICONIFY_WINDOW', aboutFrame.iconify) #no support
        aboutFrame.protocol('WM_DELETE_WINDOW', on_quit)
        aboutFrame.focus_set()
        aboutFrame.grab_set()


    def on_exit(self, event=None):
        if self.file_status == 'UNSAVED' or '*' in self.title():
            if self.get_file == '':
                if self.cur_text != self.text.get('1.0', END):
                    if askyesno(title='Confirm', message='Do you want to save a file?'):
                        self.Save()
                        exit()
                    else:
                        exit()
                else:
                    exit()
            elif askyesno(title='Confirm', message='Do you want to save a file?'):
                self.Save()
                exit()
            else:
                exit()
        else:
            exit()


if __name__ == '__main__':
    from optparse import OptionParser
    import re

    parser = OptionParser('usage: %prog [options] args or %prog arg(-f) arg(-o)')
    parser.add_option('-f', '-F', '--file_in', dest='file_in', type='string', help='Type a name of txt input file to open/create with editor/opens file if it exists or creates a new one/can be combined with -o')
    parser.add_option('-o', '-O', '--file_out', dest='file_out', type='string', help='Type a name of txt output file to create a file with the name you specified/can be combined with -f')
    (opts, args) = parser.parse_args()
    print(opts, args, len(args))

    if opts.file_in != None and opts.file_out != None and len(args) > 0:
        parser.error('Cannot use all together')
    #first check existance, then correct
    # needs diffrent templates?
    fname_template = re.compile(r'^[.\w\d\s-]+([.]txt){1}$')
    in_file_name, out_file_name = '', ''

    if opts.file_in != None:
        if not fname_template.fullmatch(opts.file_in):
            parser.error('Wrong input file name')
        else:
            in_file_name = opts.file_in

    if opts.file_out != None:
        if not fname_template.fullmatch(opts.file_out):
            parser.error('Wrong output file name')
        else:
            out_file_name = opts.file_out

    if len(args) > 2:
        parser.error('You gave too much args')
    if len(args) > 0:
        if len(args) == 1:
            if not fname_template.fullmatch(args[0]):
                parser.error('Wrong first argument')
            else:
                in_file_name = args[0]
        if len(args) == 2:
            if not fname_template.fullmatch(args[0]):
                parser.error('Wrong first argument')
            else:
                in_file_name = args[0]
            if not fname_template.fullmatch(args[1]):
                parser.error('Wrong second argument')
            else:
                out_file_name = args[1]

    test_app = app()
    test_app.mainloop()