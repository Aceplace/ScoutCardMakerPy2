import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from offensiveformation import adapters
from offensiveformation.formation import Formation
from offensiveformation.formationlibrary import FormationLibrary
from offensiveformation.formationvisualizer import FormationVisualizer
from misc.exceptions import LibraryException


class FormationEditor(tk.Frame):
    def __init__(self, root, library, current_formation):
        super(FormationEditor, self).__init__(root)
        self.current_formation = current_formation
        self.library = library

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Widgets to indicate which players are being overridden
        override_checkboxes_frame = tk.Frame(self)
        override_checkboxes_frame.grid(row=0, column=0, sticky='W')
        tk.Label(override_checkboxes_frame, text='Affected Players').pack(anchor='w')
        self.affected_players_cb_values = {}
        for player_tag in ['t','h','x','y','z','q']:
            self.affected_players_cb_values[player_tag] = tk.BooleanVar()
            tk.Checkbutton(override_checkboxes_frame,
                           text=player_tag.upper(),
                           variable=self.affected_players_cb_values[player_tag]).pack(anchor='w')

        #Widgets for composite formation entry
        composite_entry_frame = tk.Frame(self)
        composite_entry_frame.grid(row=0, column=1, sticky='W')
        tk.Label(composite_entry_frame, text='Composite Name:').pack()
        self.composite_name_entry = tk.Entry(composite_entry_frame)
        self.composite_name_entry.bind('<Return>', self.load_composite_formation)
        self.composite_name_entry.pack()
        tk.Button(composite_entry_frame, text='Load Composite', command=self.load_composite_formation).pack()

        #Widget for formation visualization
        visualizer_nb = ttk.Notebook(self)
        visualizer_nb.grid(row=1, column=0, columnspan=2, sticky='NSEW')

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

    def load_composite_formation(self, *args):
        try:
            variation = self.library.get_composite_formation_variation(self.composite_name_entry.get(), 'm')
            visualizer_formation = adapters.variation_to_visualizer(self.current_formation,
                                                                    variation)
            self.composite_visualizer.visualize_formation(visualizer_formation)
        except LibraryException as e:
            messagebox.showerror('Load Composite Error', e)

    def update_player_position(self, variation, tag, x, y):
        self.current_formation.variations[variation].players[tag]['x'] = x
        self.current_formation.variations[variation].players[tag]['y'] = y

    def load_formation(self, formation):
        self.current_formation = formation
        for tag, cb_value in self.affected_players_cb_values.items():
            cb_value.set(True if tag in self.current_formation.affected_player_tags else False)

        for variation in ['mof', 'field', 'boundary']:
            visualizer_formation = adapters.variation_to_visualizer(self.current_formation,
                                                                    self.current_formation.variations[variation])
            self.visual_editors[variation].visualize_formation(visualizer_formation)




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

