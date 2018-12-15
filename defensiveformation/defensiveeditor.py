import tkinter as tk
from tkinter import messagebox


from defensiveformation.defensiveutils import get_default_defense
from defensiveformation.placementrule import PlacementRule
from defensiveformation.parametergui import ParameterGui
from defensiveformation.placementrulegui import PlacementRuleGui
from misc.adapters import formation_to_visualizer, placed_defense_to_visualizer, \
    variation_to_defense_compatible_formation, variation_to_visualizer
from misc.alignmentvisualizer import AlignmentVisualizer
from misc.exceptions import LibraryException
from offensiveformation.formation import Formation, get_default_variation
from offensiveformation.formationlibrary import FormationLibrary


class DefensiveEditor(tk.Frame):
    def __init__(self, root, library):
        super(DefensiveEditor,self).__init__(root)
        self.library = library
        self.current_defense = get_default_defense()
        self.current_defender = self.current_defense.defenders['c']
        self.current_formation_variation = get_default_variation('mof')

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(3, weight=1)

        # Widgets to display and load a offensive formation
        offensive_formation_frame = tk.Frame(self)
        offensive_formation_frame.grid(row=0, column=0, sticky='W')
        tk.Label(offensive_formation_frame, text='Offensive Formation:').pack()
        self.offensive_formation_entry = tk.Entry(offensive_formation_frame)
        self.offensive_formation_entry.pack()
        self.get_offensive_formation_btn = tk.Button(offensive_formation_frame, text='Get Offensive Formation',
                                                     command=self.get_offensive_formation)
        self.offensive_formation_entry.bind('<Return>', self.get_offensive_formation)
        self.get_offensive_formation_btn.pack()

        # Widgets for modifying affected defenders
        affected_defenders_frame = tk.Frame(self)
        affected_defenders_frame.grid(row=0, column=1, sticky='W')
        tk.Label(affected_defenders_frame, text='Affected Defenders').grid(row=0, column=0, columnspan=3)
        self.affected_defender_cb_values = {}
        for i, defender_tag in zip(list(range(11)),['t','n','a','p','w','m', 'b', 's', 'c', 'f', 'q']):
            self.affected_defender_cb_values[defender_tag] = tk.BooleanVar()
            tk.Checkbutton(
                affected_defenders_frame,
                text=defender_tag.upper(),
                variable=self.affected_defender_cb_values[defender_tag],
                command=self.checked_affected_defenders_box
            ).grid(row = (i % 5) + 1, column = i // 5)

        self.set_affected_defender_checkboxes()

        defender_select_frame = tk.Frame(self)
        defender_select_frame.grid(row=0, column=2, sticky='E')

        # Widgets for selecting defender
        tk.Label(defender_select_frame, text='Current Defender :').grid(row=0, column=0, sticky='E')
        defender_names = ['T','N','A','P','W','M', 'B', 'S', 'C', 'F', 'Q']
        self.current_defender_value = tk.StringVar()
        self.current_defender_value.set(self.current_defender.label)
        self.current_defender_om = tk.OptionMenu(defender_select_frame, self.current_defender_value, *defender_names,
                                                 command=self.change_defender)
        self.current_defender_om.grid(row=0, column=1, sticky='WE')

        # Widgets to show the defense and formation
        formation = Formation()
        self.visualizer = AlignmentVisualizer(self, formation_to_visualizer(formation, 'mof'), None)
        self.visualizer.grid(row=1, column=0, columnspan=4, sticky='NSEW')

        # Widgets for placement rule
        self.placement_rule_frame = None
        self.change_placement_rule_gui()

        """placement_rule_frame = tk.Frame(self)
        placement_rule_frame.grid(row=0, column=3, sticky='W')

        tk.Label(placement_rule_frame, text='Placement Rule :').grid(row=0, column=0, sticky='E')
        placement_rule_names = PlacementRule.placement_rule_implementations.keys()
        self.placement_rule_name_value = tk.StringVar()
        self.placement_rule_name_value.set(self.current_defender.placement_rules[0].name)
        self.placement_rule_om = tk.OptionMenu(placement_rule_frame, self.placement_rule_name_value, *placement_rule_names,
                                               command=self.change_placement_rule)
        self.placement_rule_om.grid(row=1, column=1, sticky='WE')

        formation = Formation()
        self.visualizer = AlignmentVisualizer(self, formation_to_visualizer(formation, 'mof'), None)
        self.visualizer.grid(row = 1, column = 0, columnspan = 4, sticky='NSEW')

        self.placement_rule_frame = None
        self.change_placement_rule_gui()"""



    def change_defender(self, *args):
        self.current_defender = self.current_defense.defenders[(self.current_defender_value.get().lower())]
        #self.placement_rule_name_value.set(self.current_defender.placement_rules[0].name)
        self.change_placement_rule_gui()

    def change_placement_rule(self, *args):
        self.current_defender.placement_rules[0] = PlacementRule(self.placement_rule_name_value.get())
        self.change_placement_rule_gui()

    def change_placement_rule_gui(self):
        if self.placement_rule_frame:
            self.placement_rule_frame.grid_forget()
            self.placement_rule_frame.destroy()

        self.placement_rule_frame = PlacementRuleGui(self, self.current_defender,
                                                     self.current_defender.placement_rules[0], self.update_view)
        self.placement_rule_frame.grid(row = 0, column = 3, sticky='WE')
        #placement_rule = self.current_defender.placement_rules[0]
        #self.placement_rule_frame = ParameterGui(self, placement_rule, placement_rule.name, self.update_view)
        #self.placement_rule_frame.grid(row = 0, column = 3, sticky = 'WE')
        self.update_view()

    def update_view(self):
        defense_compatible_formation = variation_to_defense_compatible_formation(self.current_formation_variation)
        placed_defense = self.current_defense.get_placed_defenders(defense_compatible_formation)
        affected_defender_tags = self.current_defense.affected_defender_tags
        self.visualizer.visualize_formation_and_defense(variation_to_visualizer(self.current_formation_variation),
                                                        placed_defense_to_visualizer(placed_defense, affected_defender_tags))

    def get_affected_defenders(self):
        affected_defender_tags = [tag for tag, cb_value in self.affected_defender_cb_values.items() if cb_value.get()]
        return affected_defender_tags

    def set_affected_defender_checkboxes(self):
        for tag, cb_value in self.affected_defender_cb_values.items():
            cb_value.set(True if tag in self.current_defense.affected_defender_tags else False)

    def get_offensive_formation(self, *args):
        try:
            self.current_formation_variation = self.library.get_composite_formation_variation(self.offensive_formation_entry.get(), 'm')
            self.update_view()
        except LibraryException as e:
            messagebox.showerror('Load Formation Error', e)

    def checked_affected_defenders_box(self):
        self.current_defense.affected_defender_tags = self.get_affected_defenders()
        self.update_view()




if __name__=='__main__':
    import defensiveformation.placementrules.alignmentplacementrule
    import defensiveformation.placementrules.overplacementrule
    import defensiveformation.placementrules.apexplacementrule
    root = tk.Tk()
    library = FormationLibrary()
    library.load_library('temp.scml')
    DefensiveEditor(root, library).pack(fill=tk.BOTH, expand=True)

    root.mainloop()

