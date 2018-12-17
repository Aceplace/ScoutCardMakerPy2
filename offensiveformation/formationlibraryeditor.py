import tkinter as tk
from tkinter import messagebox

from offensiveformation.formation import Formation
from offensiveformation.formationeditor import FormationEditor
from misc.exceptions import LibraryException


class FormationLibraryEditor(tk.Frame):
    def __init__(self, root, library):
        super(FormationLibraryEditor, self).__init__(root)
        self.current_formation = Formation()
        self.library = library

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Widgets to enter formation info
        formation_entry_frame = tk.Frame(self)
        formation_entry_frame.grid(row=0, column=0)
        tk.Label(formation_entry_frame, text='Formation Name:').pack()
        self.formation_name_entry = tk.Entry(formation_entry_frame)
        self.formation_name_entry.pack()
        self.save_formation_btn = tk.Button(formation_entry_frame, text='Save Formation', command=self.save_formation)
        self.formation_name_entry.bind('<Return>', self.save_formation)
        self.save_formation_btn.pack()

        # Widget for library
        formation_library_frame = tk.Frame(self)
        formation_library_frame.grid(row=1, column=0, sticky='NS')
        tk.Label(formation_library_frame, text='Formations').pack()
        self.delete_selected_btn = tk.Button(formation_library_frame, text='Delete Selected Formation', command=self.delete_selected_formation)
        self.delete_selected_btn.pack()
        library_scrollbar = tk.Scrollbar(formation_library_frame, orient=tk.VERTICAL)
        self.library_lb = tk.Listbox(formation_library_frame, yscrollcommand=library_scrollbar.set)
        library_scrollbar.config(command=self.library_lb.yview)
        library_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, expand=True)
        self.library_lb.pack(side=tk.LEFT, fill=tk.Y, expand=True)
        self.library_lb.bind('<<ListboxSelect>>', lambda e:self.library_on_select(e))

        # Frame for formation editor
        self.formation_editor = FormationEditor(self, self.library, self.current_formation)
        self.formation_editor.grid(row=0, column=1, rowspan=2, sticky='NSEW')

        self.refresh_library_listbox()

    def library_on_select(self, event):
        listbox = event.widget
        if listbox.curselection():
            index = listbox.curselection()[0]
            self.formation_name_entry.delete(0,tk.END)
            self.formation_name_entry.insert(0,listbox.get(index))
            self.current_formation = self.library.get_formation(listbox.get(index))
            self.formation_editor.load_formation(self.current_formation)


    def save_formation(self, *args):
        try:
            affected_player_tags = [tag for tag, cb_value in self.formation_editor.affected_players_cb_values.items() if cb_value.get()]

            self.current_formation.affected_player_tags = affected_player_tags
            self.library.add_formation_to_library(self.formation_name_entry.get(), self.current_formation)
            self.refresh_library_listbox()

        except LibraryException as e:
            messagebox.showerror('Save Formation Error', e)

    def delete_selected_formation(self):
        if self.library_lb.curselection():
            try:
                index = self.library_lb.curselection()[0]
                self.library.delete_formation_from_library(self.library_lb.get(index))
                self.refresh_library_listbox()
            except LibraryException as e:
                messagebox.showerror('Delete Formation Error', e)


    def refresh_library_listbox(self):
        formations = self.library.get_sorted_formation_names()
        self.library_lb.delete(0, tk.END)
        for formation in formations:
            self.library_lb.insert(tk.END, formation)


    def update_player_position(self, variation, tag, x, y):
        self.current_formation.variations[variation].players[tag]['x'] = x
        self.current_formation.variations[variation].players[tag]['y'] = y




if __name__ == '__main__':
    root = tk.Tk()

    library_editor = FormationLibraryEditor(root)
    library_editor.pack(fill=tk.BOTH, expand=True)
    library_editor.library.load_library('temp.scml')
    library_editor.refresh_library_listbox()

    def on_close():
        library_editor.library.save_library('temp.scml')
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)

    root.mainloop()

