import tkinter as tk
from tkinter import messagebox

import adapters
from formation import Formation
from formationlibrary import FormationLibrary
from formationvisualizer import FormationVisualizer
from exceptions import LibraryException


class FormationLibraryEditor(tk.Frame):
    def __init__(self, root):
        super(FormationLibraryEditor, self).__init__(root)
        self.current_formation = Formation()
        self.library = FormationLibrary()

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
        tk.Label(override_checkboxes_frame, text='Affected Players').pack(anchor='w')
        self.t_cb_value = tk.BooleanVar()
        self.t_cb = tk.Checkbutton(override_checkboxes_frame, text='T', variable=self.t_cb_value)
        self.t_cb.pack(anchor='w')
        self.h_cb_value = tk.BooleanVar()
        self.h_cb = tk.Checkbutton(override_checkboxes_frame, text='H', variable=self.h_cb_value)
        self.h_cb.pack(anchor='w')
        self.x_cb_value = tk.BooleanVar()
        self.x_cb = tk.Checkbutton(override_checkboxes_frame, text='X', variable=self.x_cb_value)
        self.x_cb.pack(anchor='w')
        self.y_cb_value = tk.BooleanVar()
        self.y_cb = tk.Checkbutton(override_checkboxes_frame, text='Y', variable=self.y_cb_value)
        self.y_cb.pack(anchor='w')
        self.z_cb_value = tk.BooleanVar()
        self.z_cb = tk.Checkbutton(override_checkboxes_frame, text='Z', variable=self.z_cb_value)
        self.z_cb.pack(anchor='w')
        self.q_cb_value = tk.BooleanVar()
        self.q_cb = tk.Checkbutton(override_checkboxes_frame, text='Q', variable=self.q_cb_value)
        self.q_cb.pack(anchor='w')
        override_checkboxes_frame.grid(row=0, column=1, stick='w')

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
        visualizer_formation = adapters.variation_to_visualizer(self.current_formation,
                                                                self.current_formation.variations['mof'])
        self.formation_visual_editor = FormationVisualizer(self, visualizer_formation, self.update_player_position)
        self.formation_visual_editor.grid(row=1, column=1, stick='NSEW')

        self.refresh_library_listbox()

    def library_on_select(self, event):
        listbox = event.widget
        if listbox.curselection():
            index = listbox.curselection()[0]
            self.formation_name_entry.delete(0,tk.END)
            self.formation_name_entry.insert(0,listbox.get(index))
            self.current_formation = self.library.get_formation(listbox.get(index))
            self.t_cb_value.set(True if 't' in self.current_formation.affected_player_tags else False)
            self.h_cb_value.set(True if 'h' in self.current_formation.affected_player_tags else False)
            self.x_cb_value.set(True if 'x' in self.current_formation.affected_player_tags else False)
            self.y_cb_value.set(True if 'y' in self.current_formation.affected_player_tags else False)
            self.z_cb_value.set(True if 'z' in self.current_formation.affected_player_tags else False)
            self.q_cb_value.set(True if 'q' in self.current_formation.affected_player_tags else False)
            visualizer_formation = adapters.variation_to_visualizer(self.current_formation,
                                                                    self.current_formation.variations['mof'])
            self.formation_visual_editor.visualize_formation(visualizer_formation)

    def save_formation(self, *args):
        try:
            affected_player_tags = []
            if self.t_cb_value.get():
                affected_player_tags.append('t')
            if self.h_cb_value.get():
                affected_player_tags.append('h')
            if self.x_cb_value.get():
                affected_player_tags.append('x')
            if self.y_cb_value.get():
                affected_player_tags.append('y')
            if self.z_cb_value.get():
                affected_player_tags.append('z')
            if self.q_cb_value.get():
                affected_player_tags.append('q')

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
            self.load_composite_formation_from_library(self.composite_name_entry.get())
            self.formation_visual_editor.visualize_formation(self.current_formation)
        except LibraryException as e:
            messagebox.showerror('Load Composite Error', e)


    def refresh_library_listbox(self):
        formations = self.library.get_sorted_formation_names()
        self.library_lb.delete(0, tk.END)
        for formation in formations:
            self.library_lb.insert(tk.END, formation)

    def refresh_library(self):
        self.refresh_library_listbox()

    def update_player_position(self, tag, x, y):
        self.current_formation.variations['mof'].players[tag]['x'] = x
        self.current_formation.variations['mof'].players[tag]['y'] = y




if __name__ == '__main__':
    root = tk.Tk()

    FormationLibraryEditor(root).pack(fill=tk.BOTH, expand=True)

    root.mainloop()

