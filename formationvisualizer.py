import tkinter as tk

#Constant Values
CENTER_X_POS = 600
CENTER_Y_POS = 400
HORIZONTAL_COORDINATE_SIZE = 10
VERTICAL_COORDINATE_SIZE = 25
PLAYER_WIDTH = 26
PLAYER_HEIGHT = 20
LABEL_FONT = "Times 12"
HASH_SIZE = 5
#Derived Constant Values
LEFT_SIDELINE = CENTER_X_POS - HORIZONTAL_COORDINATE_SIZE * 53
RIGHT_SIDELINE = CENTER_X_POS + HORIZONTAL_COORDINATE_SIZE * 53
LEFT_HASH = CENTER_X_POS - HORIZONTAL_COORDINATE_SIZE * 18
RIGHT_HASH = CENTER_X_POS + HORIZONTAL_COORDINATE_SIZE * 18
LEFT_TOP_OF_NUMBERS = CENTER_X_POS - HORIZONTAL_COORDINATE_SIZE * 35
LEFT_BOTTOM_OF_NUMBERS = CENTER_X_POS - HORIZONTAL_COORDINATE_SIZE * 39
RIGHT_TUP_OF_NUMBERS = CENTER_X_POS + HORIZONTAL_COORDINATE_SIZE * 35
RIGHT_BOTTOM_OF_NUMBERS = CENTER_X_POS + HORIZONTAL_COORDINATE_SIZE * 39
FIVE_YARDS = VERTICAL_COORDINATE_SIZE * 5


def player_coordinates_to_canvas(player_x, player_y):
    return (CENTER_X_POS + player_x * HORIZONTAL_COORDINATE_SIZE, CENTER_Y_POS + player_y * VERTICAL_COORDINATE_SIZE)

def canvas_coordinates_to_player(player_x, player_y):
    return (int((player_x - CENTER_X_POS) / HORIZONTAL_COORDINATE_SIZE), int((player_y - CENTER_Y_POS) / VERTICAL_COORDINATE_SIZE))

class FormationVisualizer(tk.Frame):
    def __init__(self, root, formation, drag_player_callback):
        super(FormationVisualizer, self).__init__(root)
        self.drag_player_callback = drag_player_callback

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        #Frame and canvas set up
        xscrollbar = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        xscrollbar.grid(row=1, column=0, sticky='EW')
        yscrollbar = tk.Scrollbar(self)
        yscrollbar.grid(row=0, column=1, sticky='NS')

        self.canvas = tk.Canvas(self, bd=0, xscrollcommand=xscrollbar.set, background='white',
                             yscrollcommand=yscrollbar.set, scrollregion=(0,0,1200,800))
        self.canvas.grid(row=0, column=0, sticky='NSEW')
        xscrollbar.config(command=self.canvas.xview)
        yscrollbar.config(command=self.canvas.yview)

        # draw field lines
        self.canvas.create_line(LEFT_SIDELINE, CENTER_Y_POS - FIVE_YARDS * 3, LEFT_SIDELINE,
                                CENTER_Y_POS + FIVE_YARDS * 2)
        self.canvas.create_line(RIGHT_SIDELINE, CENTER_Y_POS - FIVE_YARDS * 3, RIGHT_SIDELINE,
                                CENTER_Y_POS + FIVE_YARDS * 2)

        for num in range(-3, 3):
            self.canvas.create_line(LEFT_SIDELINE, CENTER_Y_POS + FIVE_YARDS * num, RIGHT_SIDELINE,
                                    CENTER_Y_POS + FIVE_YARDS * num)
            self.canvas.create_line(LEFT_HASH, CENTER_Y_POS + num * FIVE_YARDS - HASH_SIZE, LEFT_HASH,
                                    CENTER_Y_POS + num * FIVE_YARDS + HASH_SIZE)
            self.canvas.create_line(RIGHT_HASH, CENTER_Y_POS + num * FIVE_YARDS - HASH_SIZE, RIGHT_HASH,
                                    CENTER_Y_POS + num * FIVE_YARDS + HASH_SIZE)
            self.canvas.create_line(LEFT_BOTTOM_OF_NUMBERS, CENTER_Y_POS + num * FIVE_YARDS - HASH_SIZE,
                                    LEFT_BOTTOM_OF_NUMBERS, CENTER_Y_POS + num * FIVE_YARDS + HASH_SIZE)
            self.canvas.create_line(LEFT_TOP_OF_NUMBERS, CENTER_Y_POS + num * FIVE_YARDS - HASH_SIZE,
                                    LEFT_TOP_OF_NUMBERS, CENTER_Y_POS + num * FIVE_YARDS + HASH_SIZE)
            self.canvas.create_line(RIGHT_BOTTOM_OF_NUMBERS, CENTER_Y_POS + num * FIVE_YARDS - HASH_SIZE,
                                    RIGHT_BOTTOM_OF_NUMBERS, CENTER_Y_POS + num * FIVE_YARDS + HASH_SIZE)
            self.canvas.create_line(RIGHT_TUP_OF_NUMBERS, CENTER_Y_POS + num * FIVE_YARDS - HASH_SIZE,
                                    RIGHT_TUP_OF_NUMBERS, CENTER_Y_POS + num * FIVE_YARDS + HASH_SIZE)

        # Create player shapes for visualization
        self.player_shapes = {}# create default formation to place players around in
        for player in formation.players:
            x, y = player_coordinates_to_canvas(player.x, player.y)
            self.player_shapes[player.tag] = {
                "oval": self.canvas.create_oval(x - PLAYER_WIDTH / 2, y - PLAYER_HEIGHT / 2,
                                                x + PLAYER_WIDTH / 2, y + PLAYER_HEIGHT / 2,
                                                fill="white"),
                "text": self.canvas.create_text(x, y, text=player.label, font=LABEL_FONT),
                "tag": player.tag}

        # Set up canvas to allow items to be dragged
        self.drag_data = {"x": 0, "y": 0, "item": None}
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.canvas.bind("<B1-Motion>", self.on_move)

    def visualize_formation(self, formation):
        for player in formation.players:
            x, y = player_coordinates_to_canvas(player.x, player.y)
            self.canvas.coords(self.player_shapes[player.tag]["oval"],
                               x - PLAYER_WIDTH / 2, y - PLAYER_HEIGHT / 2,
                               x + PLAYER_WIDTH / 2, y + PLAYER_HEIGHT / 2)
            self.canvas.coords(self.player_shapes[player.tag]["text"], x, y)

    def on_press(self, event): #get initial location of object to be moved
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        drag_items = self.canvas.find_overlapping(x-1, y-1, x+1, y+1)
        if drag_items:
            player_drag_item = self.select_player_to_drag(drag_items)
            self.drag_data["item"] = player_drag_item
            self.drag_data["x"] = x
            self.drag_data["y"] = y
        else:
            self.drag_data["item"] = None
            self.drag_data["x"] = 0
            self.drag_data["y"] = 0

    def on_release(self, event): #reset data on release
        self.drag_data["item"] = None
        self.drag_data["x"] = 0
        self.drag_data["y"] = 0

    def on_move(self, event):
        if self.drag_data["item"]:
            x = self.canvas.canvasx(event.x)
            y = self.canvas.canvasy(event.y)
            delta_x = x - self.drag_data["x"]
            delta_y = y - self.drag_data["y"]
            # move the object the appropriate amount
            if abs(delta_x) > HORIZONTAL_COORDINATE_SIZE:
                move_x = int(delta_x / HORIZONTAL_COORDINATE_SIZE) * HORIZONTAL_COORDINATE_SIZE
                self.canvas.move(self.drag_data["item"]["oval"], move_x, 0)
                self.canvas.move(self.drag_data["item"]["text"], move_x, 0)
                self.drag_data["x"] = self.drag_data["x"] + move_x
                self.call_drag_player_callback()
            if abs(delta_y) > VERTICAL_COORDINATE_SIZE:
                move_y = int(delta_y / VERTICAL_COORDINATE_SIZE) * VERTICAL_COORDINATE_SIZE
                self.canvas.move(self.drag_data["item"]["oval"], 0, move_y)
                self.canvas.move(self.drag_data["item"]["text"], 0, move_y)
                self.drag_data["y"] = self.drag_data["y"] + move_y
                self.call_drag_player_callback()

    def select_player_to_drag(self, drag_items):
        for drag_item in drag_items:
            for player in self.player_shapes.values():
                if (drag_item is player["oval"] or drag_item is player["text"]) and player['tag'] not in ['lt', 'lg', 'c', 'rg', 'rt']:
                    return player
        return None

    def call_drag_player_callback(self):
        tag = self.drag_data["item"]["tag"]
        x, y = self.canvas.coords(self.drag_data["item"]["text"])
        x, y = canvas_coordinates_to_player(x, y)
        self.drag_player_callback(tag, x, y)


if __name__ == '__main__':
    import formation
    import adapters
    formation = formation.Formation()
    visualizer_formation = adapters.formation_variation_to_visualizer_formation(
        formation,
        formation.variations['boundary']
    )
    def callback(tag, x, y):
        print(f'{tag}: {x}, {y}')

    root = tk.Tk()

    visualizer = FormationVisualizer(root, visualizer_formation, callback)
    visualizer.pack(fill=tk.BOTH, expand=True)
    root.mainloop()
