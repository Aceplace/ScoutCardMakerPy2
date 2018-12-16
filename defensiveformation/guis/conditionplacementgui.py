import tkinter as tk

from defensiveformation.defense import ConditionSet
from defensiveformation.guis.conditionsetgui import ConditionSetGui
from defensiveformation.guis.placementrulegui import PlacementRuleGui
from defensiveformation.placementruleutils import get_default_placement_rule


class ConditionPlacementGui(tk.Frame):
    def __init__(self, root, defender, update_callback):
        super(ConditionPlacementGui,self).__init__(root)
        self.defender = defender
        self.update_callback = update_callback

        # Set up scrollbar to contain all sub guis
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        xscrollbar = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        xscrollbar.grid(row=1, column=0, sticky='EW')
        yscrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        yscrollbar.grid(row=0, column=1, sticky='NS')
        self.canvas = tk.Canvas(self, bd=0, xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set)
        self.canvas.grid(row=0, column=0, sticky='NSEW')
        xscrollbar.config(command=self.canvas.xview)
        yscrollbar.config(command=self.canvas.yview)

        self.condition_placement_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.condition_placement_frame, anchor='nw')
        self.condition_placement_frame.bind("<Configure>", self.on_frame_configure)

        # Initialize and add condition set and the sub guis
        tk.Button(self.condition_placement_frame, text='Add Condition Set', command=self.add_condition_set).grid(row=0, column=0)
        self.condition_placement_sub_guis = []
        for index, condition_set, placement_rule in zip(range(len(defender.condition_sets)),
                                                    defender.condition_sets, defender.placement_rules):
            self.create_condition_placement_sub_gui(index, condition_set, placement_rule)


    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


    def create_condition_placement_sub_gui(self, index, condition_set, placement_rule):
        condition_placement_sub_gui = tk.Frame(self.condition_placement_frame, padx=20, pady=10, bd=1, relief=tk.SOLID)

        condition_placement_sub_gui.columnconfigure(0, weight=1)
        condition_placement_sub_gui.columnconfigure(2, weight=1)

        tk.Button(condition_placement_sub_gui, text='<--',
                  command=lambda:self.raise_priority(condition_set)).grid(row=0, column=0, sticky='E')
        tk.Button(condition_placement_sub_gui, text=' x ',
                  command=lambda: self.delete_set(condition_set)).grid(row=0, column=1)
        tk.Button(condition_placement_sub_gui, text='-->',
                  command=lambda: self.lower_priority(condition_set)).grid(row=0, column=2, sticky='W')

        condition_set_placement_frame = tk.Frame(condition_placement_sub_gui)
        ConditionSetGui(condition_set_placement_frame, condition_set, self.update_callback).pack(side=tk.LEFT)
        PlacementRuleGui(condition_set_placement_frame, placement_rule, self.update_callback).pack(side=tk.RIGHT)
        condition_set_placement_frame.grid(row=1, column=0, columnspan=3, sticky='WE')

        condition_placement_sub_gui.grid(row=0, column=index+1, sticky='NS')
        self.condition_placement_sub_guis.append(condition_placement_sub_gui)

    def raise_priority(self, condition_set):
        for index in range(1, len(self.defender.condition_sets)):
            if self.defender.condition_sets[index] is condition_set:
                self.defender.condition_sets[index], self.defender.condition_sets[index - 1] = \
                                        self.defender.condition_sets[index - 1], self.defender.condition_sets[index]
                self.defender.placement_rules[index], self.defender.placement_rules[index - 1] = \
                    self.defender.placement_rules[index - 1], self.defender.placement_rules[index]
                self.condition_placement_sub_guis[index], self.condition_placement_sub_guis[index - 1] = \
                    self.condition_placement_sub_guis[index - 1], self.condition_placement_sub_guis[index]
                self.condition_placement_sub_guis[index].grid(row=0, column=index + 1)
                self.condition_placement_sub_guis[index - 1].grid(row=0, column=index)
                break

        if self.update_callback:
            self.update_callback()

    def lower_priority(self, condition_set):
        for index in range(len(self.defender.condition_sets) - 1):
            if self.defender.condition_sets[index] is condition_set:
                self.defender.condition_sets[index], self.defender.condition_sets[index + 1] = \
                                        self.defender.condition_sets[index + 1], self.defender.condition_sets[index]
                self.defender.placement_rules[index], self.defender.placement_rules[index + 1] = \
                    self.defender.placement_rules[index + 1], self.defender.placement_rules[index]
                self.condition_placement_sub_guis[index], self.condition_placement_sub_guis[index + 1] = \
                    self.condition_placement_sub_guis[index + 1], self.condition_placement_sub_guis[index]
                self.condition_placement_sub_guis[index].grid(row=0, column=index + 1)
                self.condition_placement_sub_guis[index + 1].grid(row=0, column=index + 2)
                break

        if self.update_callback:
            self.update_callback()

    def delete_set(self, condition_set):
        if len(self.defender.condition_sets) == 1:
            return

        for index in range(len(self.defender.condition_sets)):
            if self.defender.condition_sets[index] is condition_set:
                #delete this condition and its gui
                self.condition_placement_sub_guis[index].grid_forget()
                self.condition_placement_sub_guis[index].destroy()
                del self.condition_placement_sub_guis[index]
                del self.defender.condition_sets[index]
                del self.defender.placement_rules[index]
                #regrid all the items after the delete
                for inner_index in range(index, len(self.defender.condition_sets)):
                    self.condition_placement_sub_guis[inner_index].grid(row=0, column=inner_index+1)
                break

        self.canvas.yview_moveto(0)
        if self.update_callback:
            self.update_callback()

    def add_condition_set(self):
        new_condition_set = ConditionSet()
        new_placement_rule = get_default_placement_rule()
        self.defender.condition_sets.append(new_condition_set)
        self.defender.placement_rules.append(new_placement_rule)
        self.create_condition_placement_sub_gui(len(self.defender.condition_sets) - 1, new_condition_set, new_placement_rule)

        if self.update_callback:
            self.update_callback()


if __name__=='__main__':
    from defensiveformation.defense import Defender, ConditionSet
    import defensiveformation.placementrules.apexplacementrule
    import defensiveformation.placementrules.alignmentplacementrule
    import defensiveformation.placementrules.overplacementrule

    defender = Defender('t', 'T')

    root = tk.Tk()

    def callback():
        print('Update')

    ConditionPlacementGui(root, defender, callback).pack(fill=tk.BOTH, expand=True)

    root.mainloop()








