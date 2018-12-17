import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os

from defensiveformation.guis.defensivelibraryeditor import DefensiveLibraryEditor
from library.alignmentlibrary import AlignmentLibrary
from misc.excelscriptparser import get_script_from_excel_file
from misc.exceptions import LibraryException, ExportException
from misc.powerpointexporter import export_to_powerpoint
from offensiveformation.formationlibraryeditor import FormationLibraryEditor


class App(tk.Tk):
    def __init__(self, prefs, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)
        self.library = AlignmentLibrary()

        #menu setup
        menubar = tk.Menu(self)

        filemenu = tk.Menu(menubar, tearoff = 0)
        filemenu.add_command(label='New Library', command=self.new_library)
        filemenu.add_separator()
        filemenu.add_command(label='Open Library', command=self.open_library)
        filemenu.add_separator()
        filemenu.add_command(label='Save Library', command=self.save_library)
        filemenu.add_command(label='Save Library As...', command=self.save_library_as)
        filemenu.add_separator()
        filemenu.add_command(label='Exit', command=self.on_close)
        menubar.add_cascade(label='File', menu=filemenu)

        viewmenu = tk.Menu(menubar, tearoff = 0)
        self.viewmenu_option = tk.IntVar()
        viewmenu.add_radiobutton(label='Formation Editor', value=1, variable=self.viewmenu_option, command=self.change_view)
        viewmenu.add_radiobutton(label='Defense Editor', value=2, variable=self.viewmenu_option, command=self.change_view)
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

        self.current_library_filename = prefs['mainframe']['current_library_filename']
        if self.current_library_filename:
            try:
                self.library.load_library(self.current_library_filename)
            except LibraryException as e:
                messagebox.showerror('Open Library Error', e)
                self.current_library_filename = None

        self.frames = {}

        self.frames[FormationLibraryEditor] = FormationLibraryEditor(mainframe, self.library)
        self.frames[FormationLibraryEditor].grid(row=0, column=0, stick='NSEW')

        self.frames[DefensiveLibraryEditor] = DefensiveLibraryEditor(mainframe, self.library)
        self.frames[DefensiveLibraryEditor].grid(row=0, column=0, stick='NSEW')

        self.current_frame = self.frames[FormationLibraryEditor]
        self.current_frame.tkraise()

        self.last_import_script_location = prefs['mainframe']['last_import_script_location']
        self.last_export_powerpoint_location = prefs['mainframe']['last_export_powerpoint_location']


    def new_library(self):
        self.library = AlignmentLibrary()
        self.frames[FormationLibraryEditor].library = self.library
        self.frames[DefensiveLibraryEditor].library = self.library
        self.frames[FormationLibraryEditor].refresh_library_listbox()
        self.frames[DefensiveLibraryEditor].refresh_library_listbox()

    def open_library(self):
        try:
            library_filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select alignment library", filetypes=(("Formation Library", "*.scml"),))
            if library_filename:
                self.library.load_library(library_filename)
                self.frames[FormationLibraryEditor].refresh_library_listbox()
                self.frames[DefensiveLibraryEditor].refresh_library_listbox()
                self.current_library_filename = library_filename
        except LibraryException as e:
                messagebox.showerror('Open Library Error', e)

    def save_library(self):
        try:
            if self.current_library_filename and os.path.isfile(self.current_library_filename):
                library_filename = self.current_library_filename
            else:
                self.current_library_filename = None
                self.save_library_as()
                return

            if library_filename:
                self.library.save_library(library_filename)
                self.current_library_filename = library_filename
        except LibraryException as e:
                messagebox.showerror('Save Library Error', e)


    def save_library_as(self):
        try:
            library_filename = filedialog.asksaveasfilename(initialdir=os.getcwd(),
                                                            title='Save alignment library',
                                                            filetypes=(('Alignment Library', '*.scml'),),
                                                            defaultextension='.scml')
            if library_filename:
                self.library.save_library(library_filename)
                self.current_library_filename = library_filename
        except LibraryException as e:
                messagebox.showerror('Save Library Error', e)

    def create_scout_cards(self):
        try:
            if self.last_import_script_location and os.path.isdir(self.last_import_script_location):
                initial_dir = self.last_import_script_location
            else:
                initial_dir = os.getcwd()
            script_filename = filedialog.askopenfilename(initialdir=initial_dir, title="Select Script",
                                                         filetypes=(("Excel", "*.xlsx"),))
            if script_filename:
                self.last_import_script_location = os.path.dirname(script_filename)
                excel_play_script = get_script_from_excel_file(self, script_filename)

                if self.last_export_powerpoint_location and os.path.isdir(self.last_export_powerpoint_location):
                    initial_dir = self.last_export_powerpoint_location
                else:
                    initial_dir = os.getcwd()

                cards_filename = filedialog.asksaveasfilename(initialdir=initial_dir,
                                                              title='Create Scout Cards',
                                                              filetypes=(('Powerpoint', '*.pptx'),),
                                                              defaultextension='.pptx')

                if cards_filename:
                    self.last_export_powerpoint_location = os.path.dirname(cards_filename)
                    export_to_powerpoint(cards_filename, excel_play_script, self.library)
        except ExportException as e:
            messagebox.showerror('Create Scout Cards Error', e)

    def change_view(self):
        if self.viewmenu_option.get() == 1:
            self.current_frame = self.frames[FormationLibraryEditor]
        else:
            self.current_frame = self.frames[DefensiveLibraryEditor]
        self.current_frame.tkraise()

    def get_prefs_as_dict(self):
        prefs_dict = {'current_library_filename':self.current_library_filename,
                      'last_import_script_location':self.last_import_script_location,
                      'last_export_powerpoint_location':self.last_export_powerpoint_location}
        return prefs_dict

    def on_close(self):
        preferences = {'mainframe': self.get_prefs_as_dict()}
        with open('preferences.json', 'w') as file:
            json.dump(preferences, file, indent=2)
        self.destroy()


if __name__=='__main__':
    import defensiveformation.placementrules.apexplacementrule
    import defensiveformation.placementrules.alignmentplacementrule
    import defensiveformation.placementrules.overplacementrule
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