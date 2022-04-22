
import sys
import logging
import tkinter as tk
from tkinter import ttk
from typing import List
from PIL import Image, ImageTk


LOG_LEVEL = logging.DEBUG
logging.basicConfig(format='%(levelname)s: %(message)s', level=LOG_LEVEL)
log = logging

GAME_1_DATA = {
    1: {
        'position': (1, 2),
        'neighbors': set([3])
    },
    2: {
        'position': (0, 1),
        'neighbors': set([3])
    },
    3: {
        'position': (1, 1),
        'neighbors': set([1, 2, 4, 5])
    },
    4: {
        'position': (2, 1),
        'neighbors': set([3])
    },
    5: {
        'position': (1, 0),
        'neighbors': set([3])
    }
}

GAME_2_DATA = {
    1: {
        'position': (1, 2),
    },
    2: {
        'position': (0, 1),
    },
    3: {
        'position': (1, 1),
    },
    4: {
        'position': (2, 1),
    },
    5: {
        'position': (1, 0),
    }
}

class Position:
    x: int
    y: int
    # constructor
    def __init__(self, x: int = None, y: int = None):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

class Node:
    num: int
    position: Position
    grid_position: Position
    neighbors: dict
    widget: ttk.Frame
    label: ttk.Label

    # constructor
    def __init__(self, num: int, position: Position):
        self.num = num
        self.position = position
        self.grid_position = Position()
        self.neighbors = dict()

    @property
    def pX(self) -> int:
        return self.position.x

    @property
    def pY(self) -> int:
        return self.position.y

    @property
    def gX(self) -> int:
        return self.grid_position.x

    @property
    def gY(self) -> int:
        return self.grid_position.y

    @pX.setter
    def pX(self, x: int):
        self.position.x = x

    @pY.setter
    def pY(self, y: int):
        self.position.y = y

    @gX.setter
    def gX(self, x: int):
        self.grid_position.x = x

    @gY.setter
    def gY(self, y: int):
        self.grid_position.y = y

    def addNeighbor(self, node):
        node: Node = node
        self.neighbors[node.num] = node


    def neighborDirections(self):
        directions_dict = dict()
        for num, neighbor in self.neighbors.items():
            neighbor: Node = neighbor
            if neighbor.position.x == self.position.x:
                if neighbor.position.y > self.position.y:
                    directions_dict['North'] = neighbor
                    # dirs.append('North')
                elif neighbor.position.y < self.position.y:
                    directions_dict['South'] = neighbor
                    # dirs.append('South')
            elif neighbor.position.y == self.position.y:
                if neighbor.position.x > self.position.x:
                    directions_dict['West'] = neighbor
                elif neighbor.position.x < self.position.x:
                    directions_dict['East'] = neighbor

        return directions_dict


class GameApp(tk.Tk):

    game_board: ttk.Frame
    controls: ttk.Frame
    buttons: dict
    nodes_dict: dict
    neighbor_bridges_dict: dict
    active_node: Node
    robot_image: ImageTk.PhotoImage

    # constructor
    def __init__(self):
        super().__init__()

        self.buttons = dict()
        self.nodes_dict = dict()
        self.neighbor_bridges_dict = dict()
        self.active_node = None

        self.robot_image = fetchTkImage('./assets/robot.png', size=20)

        # title
        self.title("TangoBot Game")
        self.config(bg='white')

        # make the top right close button
        self.protocol('WM_DELETE_WINDOW', self.stop)

        # get the screen dimension
        window_width = int(self.screen_width / 4)
        window_height = int(self.screen_height / 2)
        # find the center point
        center_x = 0
        center_y = 0
        # set the position of the window to the center of the screen
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        self.style = ttk.Style(self)
        # self.style.configure('.', font=('Helvetica', 12), background='white') # Helvetica
        self.style.configure('NodeWidget.TFrame', background='yellow')
        self.style.configure('NodeLabel.TLabel', background='yellow', foreground='black')

        self.game_board = ttk.Frame(self)
        self.controls = ttk.Frame(self)

        btns_data = {
            'up' : {
                'pos': (1, 0)
            },
            'down' : {
                'pos': (1, 2)
            },
            'left' : {
                'pos': (0, 1)
            },
            'right' : {
                'pos': (2, 1)
            },
        }
        for name, data in btns_data.items():
            self.buttons[name] = ttk.Button(self.controls, text=name)
            self.buttons[name].grid(column=data['pos'][0], row=data['pos'][1])

    @property
    def screen_width(self):
        return self.winfo_screenwidth()

    @property
    def screen_height(self):
        return self.winfo_screenheight()


    def run(self):
        self.update_idletasks()
        self.update()
        self.mainloop()

    def stop(self, event: tk.Event = None):
        try:
            self.destroy()
        except tk.TclError as err:
            log.error(err)

    def loadGame(self, DATA):
        # Remove existing data
        if isinstance(self.game_board, ttk.Frame):
            self.game_board.destroy()
        self.game_board = ttk.Frame(self)

        self.nodes_dict = dict()
        max_x = 0
        max_y = 0

        # Create Nodes based on data
        # ------------------------------------------------------------
        self.nodes_dict = dict()
        for node_num, node_data in DATA.items():
            # node (x,y) position
            node_x = node_data['position'][0]
            node_y = node_data['position'][1]
            # update max x/y
            if node_x > max_x: max_x = node_x
            if node_y > max_y: max_y = node_y
            # create the node
            node_position = Position(x=node_x, y=node_y)
            node = Node(num=node_num, position=node_position)
            # add new node to the dictionary of nodes
            self.nodes_dict[node_num] = node


        # Set Node grid Positions
        # ------------------------------------------------------------
        for node_num, node in self.nodes_dict.items():
            node: Node = node
            # calculate node grid position
            y_diff = abs(max_y - node.pY) * 2
            node.gY = y_diff
            node.gX = node.pX * 2
            # create node widget
            node.widget = ttk.Frame(self.game_board, style='NodeWidget.TFrame')
            node.label = ttk.Label(node.widget, text=node.num, style='NodeLabel.TLabel', justify=tk.CENTER, anchor=tk.CENTER)
            node.label.pack(expand=True, padx=10, pady=10)
            node.widget.grid(column=node.gX, row=node.gY, sticky=tk.NSEW)

        # Set Node neighbors and bridge widgets between neightbors
        # ------------------------------------------------------------
        self.neighbor_bridges_dict = dict()
        for node_num, node in self.nodes_dict.items():
            node: Node = node
            node_data = DATA[node_num]
            node_neighbors = node_data['neighbors']
            # loop through node neightbors
            for node_neighbor_num in node_neighbors:
                # get neighbor node
                neighbor_node: Node = self.nodes_dict[node_neighbor_num]
                # add neightbor to node
                node.addNeighbor(neighbor_node)
                # find the bridge (widget) coordinates between neighboring nodes
                bridge_coordinate = Position()
                if node.gX == neighbor_node.gX:
                    bridge_coordinate.x = node.gX
                    bridge_coordinate.y = max([node.gY, neighbor_node.gY]) - 1
                elif node.gY == neighbor_node.gY:
                    bridge_coordinate.x = max([node.gX, neighbor_node.gX]) - 1
                    bridge_coordinate.y = node.gY
                # check if bridge coordinate already exists
                if bridge_coordinate.x in self.neighbor_bridges_dict:
                    if bridge_coordinate.y not in self.neighbor_bridges_dict[bridge_coordinate.x]:
                        self.neighbor_bridges_dict[bridge_coordinate.x][bridge_coordinate.y] = bridge_coordinate
                else:
                    self.neighbor_bridges_dict[bridge_coordinate.x] = dict()
                    self.neighbor_bridges_dict[bridge_coordinate.x][bridge_coordinate.y] = bridge_coordinate

        # Add bridge widgets (empty frames between neighboring nodes)
        # ------------------------------------------------------------
        for coordinateX, xDict in self.neighbor_bridges_dict.items():
            for coordinateY, position in xDict.items():

                bridge_frame = ttk.Frame(self.game_board, style='NodeWidget.TFrame')
                bridge_frame.grid(column=position.x, row=position.y, sticky=tk.NSEW)

        # configure column/row weight for grame_board frame
        # ------------------------------------------------------------
        for i in range((max_x*2)+1): self.game_board.columnconfigure(i, weight=1)
        for i in range((max_y*2)+1): self.game_board.rowconfigure(i, weight=1)

    def playGame(self):
        # pack the controls (buttons)
        self.controls.pack()
        # pack the game_board
        self.game_board.pack(expand=True, fill='both')

        # make sure active node is available
        if self.active_node is None:
            self.active_node = self.nodes_dict[1]

        self.active_node.label.config(image=self.robot_image)

        directions = self.active_node.neighborDirections()
        # disabled all buttons
        for btn_name, btn in self.buttons.items():
            btn.config(state=tk.DISABLED)

        if 'North' in directions:
            self.buttons['up'].config(state='!DISABLED')
            self.buttons['up'].config(command=lambda n = directions['North'] : self.moveBotToNode(n))
        if 'South' in directions:
            self.buttons['down'].config(state='!DISABLED')
            self.buttons['down'].config(command=lambda n = directions['South'] : self.moveBotToNode(n))
        if 'East' in directions:
            self.buttons['left'].config(state='!DISABLED')
            self.buttons['left'].config(command=lambda n = directions['East'] : self.moveBotToNode(n))
        if 'West' in directions:
            self.buttons['right'].config(state='!DISABLED')
            self.buttons['right'].config(command=lambda n = directions['West'] : self.moveBotToNode(n))

    def moveBotToNode(self, node: Node):
        self.focus()
        self.active_node.label.config(image='')
        self.active_node = node
        self.playGame()




def fetchTkImage(file: str, size: int = 20, rotate: float = None, transpose = None):
    img = Image.open(file)
    width, height = img.size
    img = img.resize((round(size/height*width) , round(size)))
    if rotate is not None:
        img = img.rotate(angle=rotate)
    if transpose is not None:
        img = img.transpose(transpose)
    return ImageTk.PhotoImage(img)


def runApp():
    app = GameApp()
    app.loadGame(GAME_1_DATA)
    app.playGame()
    app.run()
    sys.exit(0)

if __name__ == '__main__':
    runApp()
