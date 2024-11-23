import random
from tkinter import *
from tkinter import ttk

from structures.bird import Bird
from structures.canvas import MainCanvas
from structures.pillar import Pillar
import json

# Load settings from file
try:
    with open("settings.json", 'r') as settings:
        base_settings = json.load(settings)
except FileNotFoundError:
    base_settings = {
        'BIRDS_COUNT': 5,
        'PILLARS_DURABILITY': 2,
        'PILLARS_REPAIR_INTERVAL': 5,
        'BIRD_SPAWN_INTERVAL': 2000,
        'PILLAR_SPAWN_INTERVAL': 20000,
    }
    with open('settings.json', 'w') as settings:
        json.dump(base_settings, settings)

class BirdPillarApp:
    def __init__(self, root):
        self.root = root
        self.root.maxsize(500, 600)
        self.root.minsize(500, 600)

        self.canvas = MainCanvas(root)
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        # Object lists and timers
        self.pillars = []
        self.birds = []
        self.bird_spawn_interval = base_settings['BIRD_SPAWN_INTERVAL']
        self.pillar_spawn_interval = base_settings['PILLAR_SPAWN_INTERVAL']
        self.bird_spawn_timer = None
        self.pillar_spawn_timer = None

        # Create interface
        self.create_controls()

        # Initialize objects
        self.initialize_pillars()
        self.initialize_birds()
        self.start_bird_spawning()
        self.start_pillar_spawning()

    def create_controls(self):
        control_frame = Frame(self.root)
        control_frame.pack(side=BOTTOM, fill=X, pady=10)

        # Pillar durability slider
        Label(control_frame, text="Pillar Durability:").pack(side=LEFT, padx=5)
        self.pillar_durability_slider = Scale(control_frame, from_=1, to=5, orient=HORIZONTAL)
        self.pillar_durability_slider.set(base_settings['PILLARS_DURABILITY'])
        self.pillar_durability_slider.pack(side=LEFT, padx=5)

        # Bird spawn interval
        Label(control_frame, text="Bird Spawn Interval (ms):").pack(side=LEFT, padx=5)
        self.bird_spawn_interval_box = Spinbox(control_frame, from_=500, to=20000, increment=100, width=3, command=self.update_bird_spawn_interval)
        self.bird_spawn_interval_box.pack(side=LEFT, padx=5)
        self.bird_spawn_interval_box.delete(0, END)
        self.bird_spawn_interval_box.insert(0, self.bird_spawn_interval)

        # Pillar spawn interval
        Label(control_frame, text="Pillar Spawn Interval (ms):").pack(side=LEFT, padx=5)
        self.pillar_spawn_interval_box = Spinbox(control_frame, from_=1000, to=10000, increment=500, width=3, command=self.update_pillar_spawn_interval)
        self.pillar_spawn_interval_box.pack(side=LEFT, padx=5)
        self.pillar_spawn_interval_box.delete(0, END)
        self.pillar_spawn_interval_box.insert(0, self.pillar_spawn_interval)

    def start_bird_spawning(self):
        """Start bird spawning timer."""
        if self.bird_spawn_timer:
            self.root.after_cancel(self.bird_spawn_timer)
        self.bird_spawn_timer = self.root.after(self.bird_spawn_interval, self.spawn_bird)

    def spawn_bird(self):
        """Spawn a new bird."""
        bird = Bird(self.canvas, random.randint(1, 6), self.pillars)
        self.birds.append(bird)
        bird.draw()
        bird.fly()
        self.start_bird_spawning()

    def update_bird_spawn_interval(self):
        """Update bird spawn interval."""
        try:
            self.bird_spawn_interval = int(self.bird_spawn_interval_box.get())
            self.start_bird_spawning()
        except ValueError:
            pass

    def start_pillar_spawning(self):
        """Start pillar spawning timer."""
        if self.pillar_spawn_timer:
            self.root.after_cancel(self.pillar_spawn_timer)
        self.pillar_spawn_timer = self.root.after(self.pillar_spawn_interval, self.spawn_pillar)

    def spawn_pillar(self):
        """Spawn a new pillar."""
        x = random.randint(50, 450)
        y = random.randint(250, 450)
        new_pillar = Pillar(self.canvas, self.pillar_durability_slider.get(), base_settings['PILLARS_REPAIR_INTERVAL'], x, y, 20, 10)
        self.pillars.append(new_pillar)
        new_pillar.draw()
        self.start_pillar_spawning()

    def update_pillar_spawn_interval(self):
        """Update pillar spawn interval."""
        try:
            self.pillar_spawn_interval = int(self.pillar_spawn_interval_box.get())
            self.start_pillar_spawning()
        except ValueError:
            pass

    def on_canvas_click(self, event):
        """Handle pillar placement or editing."""
        x, y = event.x, event.y
        for pillar in self.pillars:
            if pillar.contains(x, y):
                pillar.max_birds = self.pillar_durability_slider.get()
                return

        # Create a new pillar if none found nearby
        new_pillar = Pillar(self.canvas, self.pillar_durability_slider.get(), base_settings['PILLARS_REPAIR_INTERVAL'], x, y, 20, 10)
        self.pillars.append(new_pillar)
        new_pillar.draw()

    def initialize_pillars(self):
        """Initialize default pillars."""
        self.pillars.clear()
        for i in range(4):
            pillar = Pillar(self.canvas, base_settings['PILLARS_DURABILITY'], base_settings['PILLARS_REPAIR_INTERVAL'], 70 * i + 50, 300, 20, 10)
            self.pillars.append(pillar)
            pillar.draw()

    def initialize_birds(self):
        """Initialize default birds."""
        self.birds.clear()
        for _ in range(base_settings['BIRDS_COUNT']):
            bird = Bird(self.canvas, random.randint(1, 6), self.pillars)
            self.birds.append(bird)
            bird.draw()
            bird.fly()

def main():
    root = Tk()
    app = BirdPillarApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
