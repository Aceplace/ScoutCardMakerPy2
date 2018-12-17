import tkinter as tk
from tkinter import messagebox

from defensiveformation.defense import Defense
from defensiveformation.guis.defensiveeditor import DefensiveEditor
from misc.exceptions import LibraryException


class DefensiveLibraryEditor(tk.Frame):
    def __init__(self, root, library):
        super(DefensiveLibraryEditor, self).__init__(root)
        self.current_defense = Defense()
        self.library = library

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Widgets to enter defense info
        defense_entry_frame = tk.Frame(self)
        defense_entry_frame.grid(row=0, column=0)
        tk.Label(defense_entry_frame, text='Defense Name:').pack()
        self.defense_name_entry = tk.Entry(defense_entry_frame)
        self.defense_name_entry.pack()
        self.save_defense_btn = tk.Button(defense_entry_frame, text='Save Defense', command=self.save_defense)
        self.defense_name_entry.bind('<Return>', self.save_defense)
        self.save_defense_btn.pack()

        # Widget for library
        defense_library_frame = tk.Frame(self)
        defense_library_frame.grid(row=1, column=0, sticky='NS')
        tk.Label(defense_library_frame, text='Defenses').pack()
        self.delete_selected_btn = tk.Button(defense_library_frame, text='Delete Selected Defense', command=self.delete_selected_defense)
        self.delete_selected_btn.pack()
        library_scrollbar = tk.Scrollbar(defense_library_frame, orient=tk.VERTICAL)
        self.library_lb = tk.Listbox(defense_library_frame, yscrollcommand=library_scrollbar.set)
        library_scrollbar.config(command=self.library_lb.yview)
        library_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, expand=True)
        self.library_lb.pack(side=tk.LEFT, fill=tk.Y, expand=True)
        self.library_lb.bind('<<ListboxSelect>>', lambda e:self.library_on_select(e))

        # Frame for defense editor
        self.defensive_editor = DefensiveEditor(self, self.library, self.current_defense)
        self.defensive_editor.grid(row=0, column=1, rowspan=2, sticky='NSEW')

        self.refresh_library_listbox()

    def library_on_select(self, event):
        listbox = event.widget
        if listbox.curselection():
            index = listbox.curselection()[0]
            self.defense_name_entry.delete(0, tk.END)
            self.defense_name_entry.insert(0, listbox.get(index))
            self.current_defense = self.library.get_defense(listbox.get(index))
            self.defensive_editor.load_defense(self.current_defense)

    def save_defense(self, *args):
        try:
            affected_defender_tags = self.defensive_editor.get_affected_defenders()

            self.current_defense.affected_defender_tags = affected_defender_tags
            self.library.add_defense_to_library(self.defense_name_entry.get(), self.current_defense)
            self.refresh_library_listbox()

        except LibraryException as e:
            messagebox.showerror('Save Defense Error', e)

    def delete_selected_defense(self):
        if self.library_lb.curselection():
            try:
                index = self.library_lb.curselection()[0]
                self.library.delete_defense_from_library(self.library_lb.get(index))
                self.refresh_library_listbox()
            except LibraryException as e:
                messagebox.showerror('Delete Formation Error', e)

    def refresh_library_listbox(self):
        defenses = self.library.get_sorted_defense_names()
        self.library_lb.delete(0, tk.END)
        for defense in defenses:
            self.library_lb.insert(tk.END, defense)
