import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os

from misc.exceptions import LibraryException
from offensiveformation.formationlibrary import FormationLibrary
from offensiveformation.formationlibraryeditor import FormationLibraryEditor


class App(tk.Tk):
    def __init__(self, prefs, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)
        self.library = FormationLibrary()

        #menu setup
        menubar = tk.Menu(self)

        filemenu = tk.Menu(menubar, tearoff = 0)
        filemenu.add_command(label='New Formation Library', command=self.new_formation_library)
        filemenu.add_separator()
        filemenu.add_command(label='Open Formation Library', command=self.open_formation_library)
        filemenu.add_separator()
        filemenu.add_command(label='Save Formation Library', command=self.save_formation_library)
        filemenu.add_command(label='Save Formation Library As...', command=self.save_formation_library_as)
        filemenu.add_separator()
        filemenu.add_command(label='Exit', command=self.on_close)
        menubar.add_cascade(label='File', menu=filemenu)

        viewmenu = tk.Menu(menubar, tearoff = 0)
        self.viewmenu_option = tk.IntVar()
        viewmenu.add_radiobutton(label='Formation Library', value=1, variable=self.viewmenu_option, command=self.change_view)
        self.viewmenu_option.set(1)
        menubar.add_cascade(label='View', menu=viewmenu)

        createcardsmenu = tk.Menu(menubar, tearoff=0)
        createcardsmenu.add_command(label='Create Scout Cards for Script', command=self.create_scout_cards)
        menubar.add_cascade(label='Create Scout Cards', menu=createcardsmenu)
        self.config(menu=menubar)

        #frame set ups
        mainframe = tk.Frame(self)
        mainframe.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        mainframe.grid_rowconfigure(0, weight=1)
        mainframe.grid_columnconfigure(0, weight=1)

        self.current_formation_library_filename = prefs['mainframe']['current_formation_library_filename']
        if self.current_formation_library_filename:
            try:
                self.library.load_library(self.current_formation_library_filename)
            except LibraryException as e:
                messagebox.showerror('Open Library Error', e)
                self.current_formation_library_filename = None

        self.frames = {}

        self.frames[FormationLibraryEditor] = FormationLibraryEditor(mainframe, self.library)
        self.frames[FormationLibraryEditor].grid(row=0, column=0, stick='NSEW')

        self.current_frame = self.frames[FormationLibraryEditor]
        self.current_frame.tkraise()

        self.last_import_script_location = prefs['mainframe']['last_import_script_location']
        self.last_export_powerpoint_location = prefs['mainframe']['last_export_powerpoint_location']


    def new_formation_library(self):
        self.library = FormationLibrary()
        self.frames[FormationLibraryEditor].library = self.library
        self.frames[FormationLibraryEditor].refresh_library_listbox()

    def open_formation_library(self):
        try:
            library_filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select formation library", filetypes=(("Formation Library", "*.scml"),))
            if library_filename:
                self.library.load_library(library_filename)
                self.frames[FormationLibraryEditor].refresh_library_listbox()
                self.current_formation_library_filename = library_filename
        except LibraryException as e:
                messagebox.showerror('Open Library Error', e)

    def save_formation_library(self):
        try:
            if self.current_formation_library_filename and os.path.isfile(self.current_formation_library_filename):
                library_filename = self.current_formation_library_filename
            else:
                self.current_formation_library_filename = None
                self.save_formation_library_as()
                return

            if library_filename:
                self.library.save_library(library_filename)
                self.current_formation_library_filename = library_filename
        except LibraryException as e:
                messagebox.showerror('Save Library Error', e)


    def save_formation_library_as(self):
        try:
            library_filename = filedialog.asksaveasfilename(initialdir=os.getcwd(),
                                                            title='Save formation library',
                                                            filetypes=(('Formation Library', '*.scml'),),
                                                            defaultextension='.scml')
            if library_filename:
                self.library.save_library(library_filename)
                self.current_formation_library_filename = library_filename
        except LibraryException as e:
                messagebox.showerror('Save Library Error', e)

    def create_scout_cards(self):
        pass

    def change_view(self):
        if self.viewmenu_option.get() == 1:
            self.current_frame = self.frames[FormationLibraryEditor]
        self.current_frame.tkraise()

    def get_prefs_as_dict(self):
        prefs_dict = {'current_formation_library_filename':self.current_formation_library_filename,
                      'last_import_script_location':self.last_import_script_location,
                      'last_export_powerpoint_location':self.last_export_powerpoint_location}
        return prefs_dict

    def on_close(self):
        preferences = {'mainframe': self.get_prefs_as_dict()}
        with open('preferences.json', 'w') as file:
            json.dump(preferences, file, indent=2)
        self.destroy()


if __name__=='__main__':
    import json
    try:
        with open('preferences.json', 'r') as file:
            preferences = json.load(file)
    except (IOError, json.JSONDecodeError):
        preferences =   {"mainframe":
                            {
                                "current_formation_library_filename":None,
                                "last_import_script_location":None,
                                "last_export_powerpoint_location":None
                            }
                        }

    root = App(preferences)
    root.state('zoomed')

    root.protocol('WM_DELETE_WINDOW', root.on_close)
    root.mainloop()