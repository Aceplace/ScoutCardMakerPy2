import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from offensiveformation import adapters
from offensiveformation.formation import Formation
from offensiveformation.formationlibrary import FormationLibrary
from offensiveformation.formationvisualizer import FormationVisualizer
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
        tk.Label(formation_entry_frame, text='Composite Name:').pack()
        self.composite_name_entry = tk.Entry(formation_entry_frame)
        self.composite_name_entry.pack()
        self.load_composite_btn = tk.Button(formation_entry_frame, text='Load Composite', command=self.load_composite_formation)
        self.composite_name_entry.bind('<Return>', self.load_composite_formation)
        self.load_composite_btn.pack()

        # Widgets to indicate which players are being overridden
        override_checkboxes_frame = tk.Frame(self)
        override_checkboxes_frame.grid(row=0, column=1, stick='w')
        tk.Label(override_checkboxes_frame, text='Affected Players').pack(anchor='w')
        self.affected_players_cb_values = {}
        for player_tag in ['t','h','x','y','z','q']:
            self.affected_players_cb_values[player_tag] = tk.BooleanVar()
            tk.Checkbutton(override_checkboxes_frame,
                           text=player_tag.upper(),
                           variable=self.affected_players_cb_values[player_tag]).pack(anchor='w')


        # Widget for library
        formation_library_frame = tk.Frame(self)
        formation_library_frame.grid(row=1, column=0, stick='NS')
        tk.Label(formation_library_frame, text='Formations').pack()
        self.delete_selected_btn = tk.Button(formation_library_frame, text='Delete Selected Formation', command=self.delete_selected_formation)
        self.delete_selected_btn.pack()
        library_scrollbar = tk.Scrollbar(formation_library_frame, orient=tk.VERTICAL)
        self.library_lb = tk.Listbox(formation_library_frame, yscrollcommand=library_scrollbar.set)
        library_scrollbar.config(command=self.library_lb.yview)
        library_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, expand=True)
        self.library_lb.pack(side=tk.LEFT, fill=tk.Y, expand=True)
        self.library_lb.bind('<<ListboxSelect>>', lambda e:self.library_on_select(e))

        #Widget for formation visualization
        visualizer_nb = ttk.Notebook(self)
        visualizer_nb.grid(row=1, column=1, sticky='NSEW')

        self.visual_editors = {}
        for variation in ['mof', 'field', 'boundary']:
            visualizer_formation = adapters.variation_to_visualizer(self.current_formation,
                                                                    self.current_formation.variations[variation])
            self.visual_editors[variation] = FormationVisualizer(visualizer_nb,
                                                            visualizer_formation,
                                                            lambda t, x, y, v=variation: self.update_player_position(v, t, x, y)
                                                            )
            self.visual_editors[variation].pack(fill=tk.BOTH, expand=True)
            visualizer_nb.add(self.visual_editors[variation], text=variation.upper())

        visualizer_formation = adapters.variation_to_visualizer(self.current_formation,
                                                                self.current_formation.variations['mof'])
        self.composite_visualizer = FormationVisualizer(visualizer_nb, visualizer_formation, lambda t, x, y: None)
        self.composite_visualizer.pack(fill=tk.BOTH, expand=True)
        visualizer_nb.add(self.composite_visualizer, text='COMPOSITE')

        self.refresh_library_listbox()

    def library_on_select(self, event):
        listbox = event.widget
        if listbox.curselection():
            index = listbox.curselection()[0]
            self.formation_name_entry.delete(0,tk.END)
            self.formation_name_entry.insert(0,listbox.get(index))
            self.current_formation = self.library.get_formation(listbox.get(index))
            for tag, cb_value in self.affected_players_cb_values.items():
                cb_value.set(True if tag in self.current_formation.affected_player_tags else False)

            for variation in ['mof', 'field', 'boundary']:
                visualizer_formation = adapters.variation_to_visualizer(self.current_formation,
                                                                        self.current_formation.variations[variation])
                self.visual_editors[variation].visualize_formation(visualizer_formation)

    def save_formation(self, *args):
        try:
            affected_player_tags = [tag for tag, cb_value in self.affected_players_cb_values.items() if cb_value.get()]

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


    def load_composite_formation(self, *args):
        try:
            variation = self.library.get_composite_formation_variation(self.composite_name_entry.get(), 'm')
            visualizer_formation = adapters.variation_to_visualizer(self.current_formation,
                                                                    variation)
            self.composite_visualizer.visualize_formation(visualizer_formation)
        except LibraryException as e:
            messagebox.showerror('Load Composite Error', e)


    def refresh_library_listbox(self):
        formations = self.library.get_sorted_formation_names()
        self.library_lb.delete(0, tk.END)
        for formation in formations:
            self.library_lb.insert(tk.END, formation)


    def refresh_library(self):
        self.refresh_library_listbox()


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

