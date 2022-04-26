
import sys
import logging
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror, showwarning, showinfo
from typing import List
from PIL import Image, ImageTk
import speech_recognition as sr
import pyttsx3
import threading

LOG_LEVEL = logging.DEBUG
logging.basicConfig(format='%(levelname)s: %(message)s', level=LOG_LEVEL)
log = logging

recognizer: sr.Recognizer = sr.Recognizer()
microphone: sr.Microphone = sr.Microphone()

# Game 1 data
GAME_1_DATA = {
    1: {
        'position': (1, 2),
        'neighbors': set([3])
    },
    2: {
        'position': (0, 1),
        'neighbors': set([3]),
        'event': {
            'type': 'box'
        }
    },
    3: {
        'position': (1, 1),
        'neighbors': set([1, 2, 4, 5]),
        'event': {
            'type': 'battle'
        }
    },
    4: {
        'position': (2, 1),
        'neighbors': set([3]),
        'event': {
            'type': 'battle'
        }
    },
    5: {
        'position': (1, 0),
        'neighbors': set([3]),
        'event': {
            'type': 'restore_health'
        }
    }
}

"""Position Class

This class is used to store x/y coordinate values for the Node position and also for the
grid positioning.

See Node class for grid positioning info.

"""
class Position:
    """properties"""
    x: int
    y: int

    """constructor"""
    def __init__(self, x: int = None, y: int = None):
        self.x = x  # set the x value
        self.y = y  # set the y value

    """Position class object to string.
    This method returns the (x,y) data as a string.
    """
    def __str__(self):
        return f"({self.x}, {self.y})"

"""Node Class

This class is used to represent each of the locations on the game board map that the robot can visit.

Properties:

- position:         instance of the Position class, stores the (x,y) coordinates of the nodes location.
- grid_position:    stores the grid column/row information for the node widget location on the game board.
- nieghbors:        this is a dictionary of the nodes neighors. The dictionary keys are the neighbor node's number (num)

"""
class Node:
    """properties"""
    num: int                # Node's number
    position: Position      # Node's position relative to all other nodes on a x-y coordinate plane
    grid_position: Position # Grid position of the node's widget (the widget is the tkinter label that is display on the app)
    neighbors: dict         # A dictionary of neighboring nodes where the keys are the neighboring node's number
    label: ttk.Label        # the tkinter widget
    visited: bool           # True is the robot has previously been here
    event: dict             # stores data about the event (what happens when the robot encounters this node)

    """constructor"""
    def __init__(self, num: int, position: Position, event: dict):
        self.num = num                  # set the node's number
        self.position = position        # set the node's position
        self.grid_position = Position() # initialize the grid_position (this will be set later when the x/y range of all the nodes is calculated, see GameApp:loadGame())
        self.neighbors = dict()         # initialize the neighbor dictionary
        self.visited = False            # New nodes have not been visited yet, so initialize to False
        self.event = event              # set the Node's event details

    """Position X Getter
    returns the node's position 'x' value
    """
    @property
    def pX(self) -> int:
        return self.position.x

    """Position Y Getter
    returns the node's position 'y' value
    """
    @property
    def pY(self) -> int:
        return self.position.y

    """Grid Position X Getter
    returns the node's grid position 'x' value
    """
    @property
    def gX(self) -> int:
        return self.grid_position.x

    """Grid Position Y Getter
    returns the node's grid position 'y' value
    """
    @property
    def gY(self) -> int:
        return self.grid_position.y

    """Position X Setter"""
    @pX.setter
    def pX(self, x: int):
        self.position.x = x

    """Position Y Setter"""
    @pY.setter
    def pY(self, y: int):
        self.position.y = y

    """Grid Position X Setter"""
    @gX.setter
    def gX(self, x: int):
        self.grid_position.x = x

    """Grid Position Y Setter"""
    @gY.setter
    def gY(self, y: int):
        self.grid_position.y = y

    """Add (Node) Neighbor
    Add a node to the neighbor dictionary
    """
    def addNeighbor(self, node):
        node: Node = node
        self.neighbors[node.num] = node

    """Neighbor Directions
    Returns a dictionary of the neighboring node's direction

    Example:
    {
        'North': <node object>,
        'South': <node object>
    }

    This would indicate that there are neighboring nodes to the North and to the South.
    The value's are the instances of the neighboring nodes.

    """
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

"""GameApp
tkinter app for the game
"""
class GameApp(tk.Tk):
    """properties"""
    game_board: ttk.Frame           # container frame for the controls and map frames.
    map_grid: ttk.Frame             # a frame the holds all of the node widgets. The node widgets are what make up the paths on the game board.
    controls: ttk.Frame             # frame to house button controls (used to navigate the game board)
    status: ttk.Label               # A label used to send updates to the user
    buttons: dict                   # list of buttons on the controls frame
    nodes_dict: dict                # dictionary of available nodes within the game
    neighbor_bridges_dict: dict     # nodes have 1 space between them, this dictionary stores the widgets that make up the bridges the connect neightboring nodes
    active_node: Node               # reference to the current node that the robot is located at
    robot_image: ImageTk.PhotoImage # image used to show the robot's location on the game board map

    """constructor"""
    def __init__(self):
        super().__init__()

        self.buttons = dict()
        self.nodes_dict = dict()
        self.neighbor_bridges_dict = dict()
        self.active_node = None
        # get the robot image
        self.robot_image = fetchTkImage('./assets/robot.png', size=25)

        """tkinter app settings
        - title
        - add protocol (callback when close button is pressed)
        - set the window geomerty
        """
        # title
        self.title("TangoBot Game")
        self.config(bg='white')
        # override defaule protocol - make the top right close button
        self.protocol('WM_DELETE_WINDOW', self.stop)
        """set the window geometry"""
        # get the screen dimension
        window_width = int(self.screen_width / 4)
        window_height = int(self.screen_height / 2)
        # find the center point
        center_x = 0
        center_y = 0
        # set the position of the window to the center of the screen
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        """Ttk Style
        initialize the ttk styles used thoughout the app
        """
        self.style = ttk.Style(self)
        self.style.configure('.', font=('Helvetica', 12), background='white')
        self.style.configure('NodeWidget.TFrame', background='yellow')
        self.style.configure('NodeLabel.TLabel', background='yellow', foreground='black')

        """App Widgets
        there are three main content areas within the game window

        -----------------------
        | Status Bar          |
        ----------------------|
        | Controls | Game Map |
        -----------------------
        """
        # Status Bar
        # ------------------------------------------------------------
        self.status_bar = ttk.Frame(self)           # status bar frame
        self.status = ttk.Label(self.status_bar)    # status bar label
        self.status.config(text="Status...")        # set the default status label text

        self.health_bar = ttk.Progressbar(
            self.status_bar,
            orient='horizontal',
            mode='indeterminate',
            # length=280
        )

        # grid (pack) the status bar items
        self.status.grid(column=0, row=0)
        self.health_bar.grid(column=1, row=0, sticky=tk.EW)

        """Game Board
        The game board has two items; the controls and the map
        """
        self.game_board = ttk.Frame(self)

        # Controls
        # ------------------------------------------------------------
        self.controls = ttk.LabelFrame(self.game_board, text='Controls')
        self.controls.pack(side='left', fill='y', padx=10, pady=10, ipadx=10, ipady=10)
        # set the column weight for the controls frame
        for i in range(3): self.controls.columnconfigure(i, weight=1)
        # Button data
        btns_data = {
            'play': {
                'pos': (0, 0),
                'options': {
                    'columnspan': 3,
                    'pady': 5
                }
            },
            'stop': {
                'pos': (0, 0),
                'options': {
                    'columnspan': 3,
                    'pady': 5
                }
            },
            'up' : {
                'pos': (1, 1)
            },
            'down' : {
                'pos': (1, 3)
            },
            'left' : {
                'pos': (0, 2)
            },
            'right' : {
                'pos': (2, 2)
            },
        }
        # create each of the buttons on the controls
        for name, data in btns_data.items():
            btn = ttk.Button(self.controls, text=name)
            btn_options = {
                'column': data['pos'][0],
                'row': data['pos'][1],
                'sticky': tk.NSEW,
                'columnspan': 1,
                'rowspan': 1
            }
            if 'options' in data:
                btn_options = {**btn_options, **data['options']}
            btn.grid(**btn_options)
            self.buttons[name] = btn

        self.buttons['play'].config(command=lambda:self.playGame())
        self.buttons['play'].tkraise()

        # Map (Gameboard playing field)
        # ------------------------------------------------------------
        # Note: the game map node's are populated when the game data is loaded
        self.map_grid = ttk.Frame(self.game_board)
        self.map_grid.pack(expand=True, fill='both', side='left', padx=10, pady=10)

        # pack the status bar and the game board
        self.status_bar.pack(fill='x')
        self.game_board.pack(expand=True, fill='both')

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

    def speak(self, text):
        self.update_idletasks()
        self.update()
        engine: pyttsx3.Engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[10].id)
        engine.setProperty('rate', 200)
        engine.say(text)
        engine.runAndWait()
        engine.stop()
        del engine

    def recognize_speech_from_mic(self):
        # check that recognizer and microphone arguments are appropriate type
        if not isinstance(recognizer, sr.Recognizer):
            raise TypeError("`recognizer` must be `Recognizer` instance")

        if not isinstance(microphone, sr.Microphone):
            raise TypeError("`microphone` must be `Microphone` instance")
        # adjust the recognizer sensitivity to ambient noise and record audio
        # from the microphone
        try:
            with microphone as source:
                recognizer.adjust_for_ambient_noise(source, 0.5)
                # APP_INST.update_idletasks()
                # APP_INST.update()
                self.status.config(text="Listening...")
                self.update_idletasks()
                self.update()
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=2)
        except sr.WaitTimeoutError:
            return None
        # try recognizing the speech in the recording
        # if a RequestError or UnknownValueError exception is caught
        self.status.config(text="Transcribing input...")
        self.update_idletasks()
        self.update()
        transcription = None
        try:
            transcription = recognizer.recognize_google(audio)
            print(transcription)
        except sr.RequestError as err:
            # API was unreachable or unresponsive
            print("API was unreachable or unresponsive.\n", err)
        except sr.UnknownValueError as err:
            # speech was unintelligible
            print("Unknown word")
        return transcription

    def loadGame(self, DATA):

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
            node_event = None
            if 'event' in node_data:
                node_event = node_data['event']
            node = Node(num=node_num, position=node_position, event=node_event)
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
            node.label = ttk.Label(self.map_grid)
            node.label.config(text=node.num)
            node.label.config(style='NodeLabel.TLabel')
            node.label.config(justify=tk.CENTER)
            node.label.config(anchor=tk.CENTER)
            node.label.config(font=("Courier", 22))
            node.label.config(width=2)
            node.label.grid(column=node.gX, row=node.gY, sticky=tk.NSEW)

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
                bridge_frame = ttk.Frame(self.map_grid, style='NodeWidget.TFrame')
                bridge_frame.grid(column=position.x, row=position.y, sticky=tk.NSEW)

        # configure column/row weight for grame_board frame
        # ------------------------------------------------------------
        for i in range((max_x*2)+1): self.map_grid.columnconfigure(i, weight=1)
        for i in range((max_y*2)+1): self.map_grid.rowconfigure(i, weight=1)

        self.moveBotToNode(self.nodes_dict[1])

    def playGame(self):

        # make sure active node is available
        if self.active_node is None:
            self.moveBotToNode(self.nodes_dict[1])

        # update status
        self.status.config(text="Playing Game")
        self.update_idletasks()
        self.update()

        # disable play button and raise stop button
        self.buttons['stop'].tkraise()
        self.buttons['stop'].config(state='!DISABLED')
        self.buttons['play'].config(state=tk.DISABLED)

        directions = self.active_node.neighborDirections()

        # Build the text prompt for the robot to speak to the user
        # There are 2 options
        # - There is only one visible path forward (to which the user must say "yes" to continue)
        # - There is more than one visible path to move (to which the user must respond with the direction that they want to continue)
        prompt_text = ''
        direction_words = list(directions.keys())
        if len(direction_words) > 1:
            prompt_text = ', '.join(list(directions.keys())[:-1])
            prompt_text = f"I see a path to the {prompt_text}, and {direction_words[-1]}, which way do you want to go?"
        else:
            prompt_text = f"I see a path to the {direction_words[0]}, do you want to continue?"
        # print(prompt_text)
        self.speak(prompt_text)

        # get user input (speech)
        # while True:
        user_action = self.recognize_speech_from_mic()
        # no audio was picket up, transcription failed
        if not isinstance(user_action, str):
            log.debug('Audio transcription from mic failed.')
            self.status.config(text="Audio transcription from mic failed.")
            self.update_idletasks()
            self.update()
        else:
            # determine what the user said...
            # --------------------------------
            # if there is only one visible direction, then the user must
            # answer 'yes' to proceed'
            if len(direction_words) == 1 and user_action.lower() == 'yes':
                self.moveBotToNode(directions[direction_words[0]])
            else:
                # The user must provide a valid direction
                # either: North, South, East, or West, and the
                # direction must be visible for the robot (i.e. in the 'directions' variable)
                user_action = user_action.lower()
                if user_action == 'north' and 'North' in directions:
                    self.moveBotToNode(directions['North'])
                elif user_action == 'south' and 'South' in directions:
                    self.moveBotToNode(directions['South'])
                elif user_action == 'east' and 'East' in directions:
                    self.moveBotToNode(directions['East'])
                elif user_action == 'west' and 'West' in directions:
                    self.moveBotToNode(directions['West'])
            self.playGame()

        # disable stop button and raise play button
        self.buttons['play'].tkraise()
        self.buttons['play'].config(state='!DISABLED')
        self.buttons['stop'].config(state=tk.DISABLED)

    def moveBotToNode(self, node: Node):
        self.focus()
        if isinstance(self.active_node, Node):
            if isinstance(self.active_node.label, ttk.Label):
                self.active_node.label.config(image='')
        self.active_node = node
        # set robot image on active node
        self.active_node.label.config(image=self.robot_image)
        directions = self.active_node.neighborDirections()
        # disabled all buttons
        move_btns = ['up', 'down', 'left', 'right']
        for btn_name in move_btns:
            self.buttons[btn_name].config(state=tk.DISABLED)
        # Update the command bindings for the control buttons (Up, Down, Left, and Right)
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
        # make updates visible
        self.update_idletasks()
        self.update()

        # TODO - process event

        self.active_node.visited = True


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
    # app.playGame()
    app.run()
    sys.exit(0)

if __name__ == '__main__':
    runApp()
