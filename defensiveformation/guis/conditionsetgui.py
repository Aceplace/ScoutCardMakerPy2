import tkinter as tk
import defensiveformation.conditions as Conditions

class ConditionSetGui(tk.Frame):
    def __init__(self, root, defender, condition_set, update_callback):
        super(ConditionSetGui, self).__init__(root)
        self.defender = defender
        self.condition_set = condition_set
        self.update_callback = update_callback

        # Widgets for condition options
        condition_set_options_frame = tk.Frame(self)
        condition_set_options_frame.pack()

        tk.Button(condition_set_options_frame, text='<--', command=self.raise_priority).pack(side=tk.LEFT)
        tk.Button(condition_set_options_frame, text=' + ', command=self.add_condition_set).pack(side=tk.LEFT)
        tk.Button(condition_set_options_frame, text=' - ', command=self.delete_condition_set).pack(side=tk.LEFT)
        tk.Button(condition_set_options_frame, text='-->', command=self.lower_priority).pack(side=tk.LEFT)

        # Widgets for modifying conditions
        self.conditions_frame = tk.Frame(self)
        self.conditions_frame.pack()

        num_conditions_range = list(range(len(condition_set.conditions)))
        conditions = self.condition_set.conditions
        connectors = self.condition_set.connectors
        connector_options = ['and','or']
        self.connector_om_values = [None]
        self.condition_menu_values = []
        for i, condition, connector in zip(num_conditions_range, conditions, connectors):
            if i != 0:
                connector_value = tk.StringVar()
                connector_value.set(connectors[i])
                connector_om = tk.OptionMenu(self.conditions_frame, connector_value, *connector_options,
                                             command=self.condition_change)
                connector_om.grid(row=i, column=0, sticky='WE')
                self.connector_om_values.append(connector_value)
                
            self.create_and_add_conditions_menu(i, condition)




    def create_and_add_conditions_menu(self, index, condition):
        self.condition_menu_values.append(tk.StringVar())
        condition_menu_value = self.condition_menu_values[index]
        condition_menu_value.set(condition)
        menu_button = tk.Menubutton(self.conditions_frame, textvariable=condition_menu_value, indicatoron=True,
                                    borderwidth=1, relief='raised')
        root_menu = tk.Menu(menu_button, tearoff=False)
        menu_button.configure(menu=root_menu)

        sub_menu_directory = {'root':{'menu':root_menu, 'sub_menus':{}}}
        for condition_name in Conditions.condition_implementations.keys():
            current_sub_menu_directory = sub_menu_directory['root']
            split_condition_name = condition_name.split('/', 1)

            while len(split_condition_name) == 2:
                parent_category = split_condition_name[0]
                remaining = split_condition_name[1]

                if parent_category not in current_sub_menu_directory['sub_menus'].keys():
                    sub_menu = tk.Menu(current_sub_menu_directory['menu'], tearoff=False)
                    current_sub_menu_directory['menu'].add_cascade(label=parent_category, menu=sub_menu)
                    current_sub_menu_directory['sub_menus'][parent_category] = {'menu':sub_menu, 'sub_menus':{}}

                current_sub_menu_directory = current_sub_menu_directory['sub_menus'][parent_category]
                split_condition_name = remaining.split('/',1)

            remaining = split_condition_name[0]
            current_sub_menu_directory['menu'].add_radiobutton(value=condition_name, label=remaining,
                                                               variable=self.condition_menu_values[index],
                                                               command=self.condition_change)

        root_menu.add_radiobutton(value='Delete Condition', label='Delete Condition',
                                  variable=self.condition_menu_values[index],
                                  command=self.condition_change)
        menu_button.grid(row=index, column=1, sticky='WE')


    def condition_change(self, *args):
        pass

    def add_condition_set(self, *args):
        pass

    def raise_priority(self, *args):
        pass

    def lower_priority(self, *args):
        pass

    def delete_condition_set(self, *args):
        pass




if __name__=='__main__':
    from defensiveformation.defense import Defender, ConditionSet
    defender = Defender('t','T')
    defender.condition_sets.append(ConditionSet())

    defender.condition_sets[0].conditions = ['Default', 'Default', 'Default']
    defender.condition_sets[0].connectors = ['first', 'or', 'and']

    root = tk.Tk()
    ConditionSetGui(root, defender, defender.condition_sets[0], None).pack(fill=tk.BOTH, expand=True)
    root.mainloop()