import random
from tkinter import *
from tkinter import simpledialog

from structures.bird import Bird
from structures.canvas import MainCanvas
from structures.pillar import Pillar
import json

try:
    with open("settings.json", 'r') as settings:
        base_settings = json.load(settings)
except FileNotFoundError:
    base_settings = {
        'BIRDS_COUNT': 5,
        'PILLARS_DURABILITY': 2,
        'PILLARS_REPAIR_INTERVAL': 5,
        'BIRD_INTERVAL': 1000,  # интервал появления птиц в миллисекундах
        'PILLAR_INTERVAL': 2000  # интервал появления столбов в миллисекундах
    }
    with open('settings.json', 'w') as settings:
        json.dump(base_settings, settings)


class App:
    def __init__(self, root):
        self.root = root
        self.root.maxsize(500, 500)
        self.root.minsize(500, 500)

        self.canvas = MainCanvas(root)
        self.pillars = []
        self.birds = []
        
        self.bird_interval = base_settings['BIRD_INTERVAL']
        self.pillar_interval = base_settings['PILLAR_INTERVAL']

        # Настройка интерфейса для управления параметрами
        self.setup_ui()

        self.create_initial_pillars()

        self.bird_creation()

    def setup_ui(self):
        frame = Frame(self.root)
        frame.pack(side=TOP)

        Label(frame, text="Частота появления птиц (мс)").grid(row=0, column=0)
        self.bird_speed_slider = Scale(frame, from_=500, to=3000, orient=HORIZONTAL, command=self.update_bird_speed)
        self.bird_speed_slider.set(self.bird_interval)
        self.bird_speed_slider.grid(row=0, column=1)

        Label(frame, text="Частота появления столбов (мс)").grid(row=1, column=0)
        self.pillar_speed_slider = Scale(frame, from_=500, to=3000, orient=HORIZONTAL, command=self.update_pillar_speed)
        self.pillar_speed_slider.set(self.pillar_interval)
        self.pillar_speed_slider.grid(row=1, column=1)

    def create_initial_pillars(self):
        for i in range(1, 5):
            pillar = Pillar(self.canvas, base_settings['PILLARS_DURABILITY'], base_settings['PILLARS_REPAIR_INTERVAL'],
                            70 * i + (50 * (i - 1)), 300, 10, 20)
            self.pillars.append(pillar)
            pillar.draw()

        self.canvas.bind("<Button-1>", self.add_or_edit_pillar)

    def add_or_edit_pillar(self, event):
        for pillar in self.pillars:
            if pillar.contains(event.x, event.y):  # Проверить, попадает ли клик на столб
                new_durability = simpledialog.askinteger("Изменить прочность", "Введите новую прочность столба:", initialvalue=pillar.durability)
                if new_durability is not None:
                    pillar.durability = new_durability
                    pillar.update()  # Обновить отображение столба
                return

        # Если клик не попал на столб, добавим новый
        new_durability = simpledialog.askinteger("Добавить столб", "Введите прочность нового столба:", initialvalue=base_settings['PILLARS_DURABILITY'])
        if new_durability is not None:
            new_pillar = Pillar(self.canvas, new_durability, base_settings['PILLARS_REPAIR_INTERVAL'], event.x, 300, 10, 20)
            self.pillars.append(new_pillar)
            new_pillar.draw()

    def bird_creation(self):
        if len(self.birds) < base_settings['BIRDS_COUNT']:
            bird = Bird(self.canvas, random.randint(1, 6), self.pillars)
            self.birds.append(bird)
            bird.draw()
            bird.fly()
        self.root.after(self.bird_interval, self.bird_creation)

    def update_bird_speed(self, value):
        self.bird_interval = int(value)

    def update_pillar_speed(self, value):
        self.pillar_interval = int(value)


def main():
    root = Tk()
    app = App(root)
    root.mainloop()


if __name__ == '__main__':
    main()