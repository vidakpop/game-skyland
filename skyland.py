import tkinter as tk
from tkinter import messagebox
from tkinter.font import Font

WIDTH = 600
HEIGHT = 400
START_Y = 200

class SkylandGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        # Set the title of the window
        self.title("Skyland")

        # Create a canvas
        self.canvas = tk.Canvas(self, width=WIDTH, height=HEIGHT, bg='lightblue')
        self.canvas.pack()

        # Create game objects
        self.avatar = None
        self.land = Land(self.canvas)
        self.trophy = None

        # Create a label for the score
        self.score_label = tk.Label(self, text="Score: 0", font=Font(family="Helvetica", size=15))
        self.score_label.pack()

        # Create a label for the time
        self.time_label = tk.Label(self, text="Time: 0", font=Font(family="Helvetica", size=15))
        self.time_label.pack()

        # Create a button to start the game
        self.start_button = tk.Button(self, text="Start", command=self.start_game)
        self.start_button.pack()

        # Create a button to stop the game
        self.stop_button = tk.Button(self, text="Stop", command=self.stop_game)
        self.stop_button.pack()

        # Create a button to resume the game
        self.resume_button = tk.Button(self, text="Resume", command=self.resume_game, state=tk.DISABLED)
        self.resume_button.pack()

        # Initialize the score to 0
        self.score = 0
        self.time = 0

        # Boolean flag to control game state
        self.is_game_running = False

    def start_game(self):
        # Create game objects
        self.avatar = Avatar(self.canvas)
        self.trophy = Trophy(self.canvas)

        # Start the game loop
        self.is_game_running = True
        self.game_loop()

    def game_loop(self):
        if not self.is_game_running:
            return

        # Update the score and the time
        self.score_label.config(text="Score: {}".format(self.score))
        self.time_label.config(text="Time: {}".format(self.time))

        # Update game objects
        self.avatar.update(self.land, self.trophy)
        self.land.update()

        # Check if the game is over
        if self.avatar.y >= HEIGHT:
            # Game over!
            self.is_game_running = False
            self.game_over()
            return

        # Increment the score and the time
        self.score += 1
        self.time += 1

        # Schedule the next update
        self.after(100, self.game_loop)

    def game_over(self):
        # Show a messagebox that displays the final score
        messagebox.showinfo("Game Over!", "Your final score was: {}!".format(self.score))

        # Enable the resume button
        self.resume_button.config(state=tk.NORMAL)

    def stop_game(self):
        # Stop the game loop
        self.is_game_running = False

    def resume_game(self):
        # Reset the score and time
        self.score = 0
        self.time = 0

        # Clear the canvas
        self.canvas.delete("all")

        # Disable the resume button
        self.resume_button.config(state=tk.DISABLED)

        # Restart the game
        self.start_game()


class Avatar:
    def __init__(self, canvas):
        self.canvas = canvas
        self.head = self.canvas.create_oval(0, 0, 10, 10, fill='sandybrown')
        self.torso = self.canvas.create_rectangle(0, 10, 10, 20, fill='lime')
        self.canvas.move(self.head, 20, START_Y+130)
        self.canvas.move(self.torso, 20, START_Y+130)
        self.canvas.bind_all('<KeyPress-Left>', self.move)
        self.canvas.bind_all('<KeyPress-Right>', self.move)
        self.canvas.bind_all('<KeyPress-Up>', self.move)
        self.canvas.bind_all('<KeyPress-Down>', self.move)
        self.x = 1
        self.y = 0

    def update(self, land, trophy):
        self.canvas.move(self.head, self.x, self.y)
        self.canvas.move(self.torso, self.x, self.y)
        self.hit_object(land)
        self.hit_object(trophy)
        self.find_trophy(trophy)

    def move(self, event=None):
        if event.keysym == 'Left':
            self.x = -1
        elif event.keysym == 'Right':
            self.x = 1
        elif event.keysym == 'Up':
            self.y = -2
        elif event.keysym == 'Down':
            self.y = 1

    def hit_object(self, obj):
        if self.canvas.coords(self.head) == self.canvas.coords(obj):
            # Collision occurred, handle accordingly
            pass

    def find_trophy(self, trophy):
        if self.canvas.coords(self.head) == self.canvas.coords(trophy):
            # Trophy collected, handle accordingly
            pass


#
class Land:
    def __init__(self, canvas):
        self.canvas = canvas

        # sky
        self.canvas.create_rectangle(0, 0, WIDTH, START_Y-100, fill='lightblue')

        # valley
        self.canvas.create_rectangle(0, START_Y-120, WIDTH, START_Y, fill='limegreen')

        self.hills = [
            self.make_hill(50, 250, 150, 350),
            self.make_hill(150, 250, 250, 350),
            self.make_hill(250, 250, 350, 350),
            self.make_hill(350, 250, 450, 350)
        ]

        self.objects = [
            self.make_object(80, 320, 100, 340, fill='red'),
            self.make_object(180, 320, 200, 340, fill='blue'),
            self.make_object(280, 320, 300, 340, fill='green'),
            self.make_object(380, 320, 400, 340, fill='yellow')
        ]

        cloud1 = self.make_cloud(100, 120)
        cloud2 = self.make_cloud(200, 140)
        cloud3 = self.make_cloud(300, 80)
        self.clouds = [cloud1, cloud2, cloud3]

    def make_hill(self, x1, y1, x2, y2):
        return self.canvas.create_rectangle(x1, START_Y-y1, x2, START_Y-y2, fill='red', outline='red')

    def make_cloud(self, x, y):
        cloud = self.canvas.create_oval(x, START_Y-y, x+60, START_Y-y-40, fill='white', outline='white')
        return cloud

    def make_object(self, x1, y1, x2, y2, **kwargs):
        return self.canvas.create_rectangle(x1, START_Y-y1, x2, START_Y-y2, **kwargs)

    def update(self):
        for cloud in self.clouds:
            self.move_cloud(cloud)

    def move_cloud(self, cloud, delta=1):
        self.canvas.move(cloud, delta, 0)
        cloud_coords = self.canvas.coords(cloud)
        if cloud_coords[2] > WIDTH:
            # Move the cloud to the left side of the canvas
            self.canvas.move(cloud, -WIDTH - 60, 0)

        if cloud_coords[0] < -60:
            # Move the cloud to the right side of the canvas
            self.canvas.move(cloud, WIDTH + 60, 0)

class AI:

    def __init__(self, canvas, x, y):

        self.canvas = canvas
        self.spider = self.make_spider(x, y)
        self.thread = self.canvas.create_line(x+10, 0, x+10, y+5,
                                          fill='ivory2', width=3)
        self.x, self.y = 0, 0.5

    def make_spider(self,canvas, x, y):

        color1 = 'black'
        head = canvas.create_oval(5, 5, 15, 13, fill=color1)
        torso = canvas.create_oval(0, 10, 20, 40, fill=color1)
        legs = [canvas.create_line(-5-i*5, 10*i+5, 5, 10*i+15,  \
                fill=color1, width=4) for i in range(2) ] + \
               [canvas.create_line(15, 10*i+15, 25+i*5, 10*i+5, \
                fill=color1, width=4) for i in range(2) ] + \
               [canvas.create_line(-10+i*5, 10*i+35, 5, 10*i+25, \
                fill=color1, width=4) for i in range(2) ] + \
               [canvas.create_line(15, 10*i+25, 30-i*5, 10*i+35,\
                fill=color1, width=4) for i in range(2) ]     
                 
        spider = [head, torso] + legs
        for part in spider:
            self.canvas.move(part, x, y)
        return spider

    def update(self, eatable):
        pass

class Avatar:
    def __init__(self, canvas):
        self.canvas = canvas
        self.head = self.canvas.create_oval(0, 0, 10, 10, fill='sandybrown')
        self.torso = self.canvas.create_rectangle(0, 10, 10, 20, fill='lime')
        self.canvas.move(self.head, 20, START_Y+130)
        self.canvas.move(self.torso, 20, START_Y+130)
        self.canvas.bind_all('<KeyPress-Left>', self.move)
        self.canvas.bind_all('<KeyPress-Right>', self.move)
        self.canvas.bind_all('<KeyPress-Up>', self.move)
        self.canvas.bind_all('<KeyPress-Down>', self.move)
        self.x = 1
        self.y = 0
        self.is_game_over = False

    def update(self, land, trophy):
        if not self.is_game_over:
            self.canvas.move(self.head, self.x, self.y)
            self.canvas.move(self.torso, self.x, self.y)
            self.hit_objects(land.objects)
            self.hit_object(trophy)
            self.check_game_over()

    def move(self, event=None):
        if event.keysym == 'Left':
            self.x = -1
        elif event.keysym == 'Right':
            self.x = 1
        elif event.keysym == 'Up':
            self.y = -2
        elif event.keysym == 'Down':
            self.y = 1

    def hit_object(self, obj):
        if self.canvas.coords(self.head) == self.canvas.coords(obj):
            # Collision occurred, handle accordingly
            self.is_game_over = True

    def hit_objects(self, objects):
        for obj in objects:
            if self.canvas.coords(self.head) == self.canvas.coords(obj):
                # Collision occurred, handle accordingly
                self.is_game_over = True

    def check_game_over(self):
        if self.is_game_over:
            self.canvas.unbind_all('<KeyPress-Left>')
            self.canvas.unbind_all('<KeyPress-Right>')
            self.canvas.unbind_all('<KeyPress-Up>')
            self.canvas.unbind_all('<KeyPress-Down>')
            self.canvas.create_text(WIDTH // 2, HEIGHT // 2, text="Game Over", fill="red", font="Helvetica 24 bold")
            self.canvas.create_text(WIDTH // 2, HEIGHT // 2 + 30, text="Score: {}".format(self.canvas.score),
                                    fill="red", font="Helvetica 16")


class Trophy:
    def __init__(self, canvas):
        self.canvas = canvas
        self.trophy = self.canvas.create_oval(580, START_Y-40, 590, START_Y-30, fill='gold')

    def update(self):
        pass


if __name__ == "__main__":
    skyland_gui = SkylandGUI()
    skyland_gui.mainloop()

class Trophy:
    def __init__(self, canvas):
        self.canvas = canvas
        self.trophy = self.canvas.create_oval(580, START_Y-40, 590, START_Y-30, fill='gold')

    def update(self):
        pass


if __name__ == "__main__":
    skyland_gui = SkylandGUI()
    skyland_gui.mainloop()
