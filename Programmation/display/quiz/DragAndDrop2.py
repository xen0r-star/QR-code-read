from tkinter import *
from tkinter import font
from PIL import Image, ImageTk, ImageDraw
from pathlib import Path

from widgets.Button import custom_Button
from widgets.Image import custom_Image

paths = Path(__file__).parent.resolve()



class displayDragAndDrop2(Frame):
    def __init__(self, master, style=1, playerPoint=[0, 0], time=60, currentQuestion = 0, maxQuestion=20):
        super().__init__(master)
        
        self.style = style
        self.time = time
        self.playerPoint = playerPoint

        self.questionNumber = f"{currentQuestion}/{maxQuestion}"

        self.textQuestion = "Replace les éléments dans leurs bonnes catégories."
        self.textResponse = ["Vélo",
                             "Bateau", 
                             "Avion",
                             "Voiture"]
        self.textZones = ["moin de 50kg CO2/an", "plus de 50kg CO2/an"]
        self.correctResponse = [1, 2, 2, 1]
        self.response = [[0, 0] for _ in range(len(self.textResponse))]

        self.config(bg=self.master.color_background)
        self.grid(column=0, row=0, sticky="nsew")
        self.addComponents()

        self.grid_rowconfigure(0, weight=3)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=3)
        self.grid_columnconfigure(0, weight=1)

    def addComponents(self):
        if self.style == 2:
            background_source = paths / "../../assets/Background-red.png"
            self.master.color_background = "#CF6953"
        elif self.style == 3:
            background_source = paths / "../../assets/Background-blue.png"
            self.master.color_background = "#53B1CF"
        else:
            background_source = paths / "../../assets/Background.png"

        custom_Image(self, image=background_source, bg=self.master.color_background, 
                     width=700, height=700, 
                     column=0, row=0, rowspan=3)

        self.question = Frame(self, bg=self.master.color_background)
        self.question.grid(column=0, row=0)

        fontStyle = font.Font(size=15)
        custom_Image(self.question, image=paths / "../../assets/Frame5.png",
                     text=self.textQuestion, 
                     fg=self.master.color_text, font=fontStyle, wraplength=600,
                     bg=self.master.color_background, 
                     width=625, height=100, 
                     column=0, row=1)
        
        fontStyle = font.Font(size=15, weight="bold")
        
        self.header = Label(self.question, compound="center", font=fontStyle, fg=self.master.color_text, bg=self.master.color_background)
        self.header.grid(column=0, row=2, pady=(7, 0))
        

        self.body = Frame(self, bg=self.master.color_background, height=325, width=620)
        self.body.grid(column=0, row=1)

        self.canvas = Canvas(self.body, height=325, width=620, bg=self.master.color_background, bd=0, highlightthickness=0)
        self.canvas.grid(column=0, row=0)
        self.photo = ImageTk.PhotoImage(Image.open(paths / "../../assets/quiz/zone.png"))
        self.canvas.create_image(620 // 2, 97, anchor=CENTER, image=self.photo)
        self.canvas.create_text(134, 18, text=self.textZones[0], font=("Arial", 15), anchor=N, fill="white")
        self.canvas.create_text(486, 18, text=self.textZones[1], font=("Arial", 15), anchor=N, fill="white")

        self.rectangles = []
        for i in range(len(self.textResponse)):
            rect = self.canvas.create_rectangle(
                84 + (117 * i), 220, 84 + (117 * i) + 100, 220 + 100, 
                fill=self.master.color_fourth, outline="#FFFFFF", width=4
            )
            text_items = self.create_wrapped_text(84 + (117 * i) + 5, 220 + 3, self.textResponse[i], max_width=90)
            self.rectangles.append((rect, text_items))
            DragDrop(self.canvas, rect, text_items, i+1, self.response, self.callback) 



        custom_Button(self, 
                        command=self.validate, 
                        image=paths / "../../assets/quiz/Valider.png",
                        height=75, width=343,
                        bg=self.master.color_background,
                        column=0, row=2, ipadx=5, ipady=2)
        

        fontStyle = font.Font(size=25, weight="bold")
        self.numberQuestion = Label(self, text=self.questionNumber, compound="center", font=fontStyle, fg=self.master.color_text2, bg=self.master.color_background)
        self.numberQuestion.grid(column=0, row=2, sticky=SE, padx=20, pady=20)


        if self.style == 2 or self.style == 3:
            image = scoreApp().get()

            self.header.config(image=image)
            self.header.image = image

        else:
            photo = ImageTk.PhotoImage(
                Image.open(paths / "../../assets/Frame6.png").resize((250, 40), Image.LANCZOS)
            )
            self.header.config(image=photo)
            self.header.image = photo
            ChronoApp(self.master, self.header, self.time)
    

    def create_wrapped_text(self, x, y, text, max_width):
        words = text.split()
        lines = []
        line = ""
        text_items = []

        for word in words:
            test_line = f"{line} {word}".strip()
            temp_text_item = self.canvas.create_text(x, y, text=test_line, font=("Arial", 12), anchor=NW, fill="white")
            bbox = self.canvas.bbox(temp_text_item)
            self.canvas.delete(temp_text_item)

            if bbox[2] - bbox[0] <= max_width:
                line = test_line
            else:
                lines.append(line)
                line = word
        
        lines.append(line)
        for i, line in enumerate(lines):
            text_item = self.canvas.create_text(x, y + i * 15, text=line, fill="white", font=("Arial", 12), anchor=NW)
            text_items.append(text_item)

        return text_items

    def callback(self, responce):
        self.response = responce

    def validate(self):
        self.zones = {
            1: [76.0, 116.0],
            2: [193.0, 116.0],
            3: [427.0, 116.0],
            4: [544.0, 116.0]
        }

        a = 0
        for i in range(len(self.response)):
            if self.correctResponse[i] == 1:
                if self.response[i] == self.zones[1] or self.response[i] == self.zones[2]:
                    a += 1
            else:
                if self.response[i] == self.zones[3] or self.response[i] == self.zones[4]:
                    a += 1
            

        if a == len(self.response):
            print(1)
        else:
            print(0)
            



class DragDrop:
    def __init__(self, canvas, item, text_items, rect_id, response, callback):
        self.canvas = canvas
        self.item = item
        self.response = response
        self.text_items = text_items
        self.rect_id = rect_id
        self.callback = callback
        self.magnetZone = [
            [26, 66, 126, 166],
            [143, 66, 243, 166],
            [377, 66, 477, 166],
            [494, 66, 594, 166]
        ]

        self.canvas.tag_bind(self.item, '<ButtonPress-1>', self.on_press)
        self.canvas.tag_bind(self.item, '<B1-Motion>', self.on_drag)
        self.canvas.tag_bind(self.item, '<ButtonRelease-1>', self.on_release)
        for text_item in self.text_items:
            self.canvas.tag_bind(text_item, '<ButtonPress-1>', self.on_press)
            self.canvas.tag_bind(text_item, '<B1-Motion>', self.on_drag)
            self.canvas.tag_bind(text_item, '<ButtonRelease-1>', self.on_release)
        self.is_magnetized = False

    def on_press(self, event):
        self.x = event.x
        self.y = event.y

    def on_drag(self, event):
        dx = event.x - self.x
        dy = event.y - self.y

        x1, y1, x2, y2 = self.canvas.bbox(self.item)
        if x1 + dx < 0 or y1 + dy < 0 or x2 + dx > 620 or y2 + dy > 325:
            return

        self.canvas.move(self.item, dx, dy)
        for text_item in self.text_items:
            self.canvas.move(text_item, dx, dy)
        self.x = event.x
        self.y = event.y
        self.check_magnet()

    def on_release(self, event):
        self.x = event.x
        self.y = event.y
        self.check_magnet(release=True)
        self.update_position()

    def check_magnet(self, release=False):
        x1, y1, x2, y2 = self.canvas.bbox(self.item)
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2

        for zone in self.magnetZone:
            zx1, zy1, zx2, zy2 = zone
            zcx = (zx1 + zx2) / 2
            zcy = (zy1 + zy2) / 2

            if abs(cx - zcx) < 10 and abs(cy - zcy) < 10:
                if not release:
                    dx = zcx - cx
                    dy = zcy - cy

                    if x1 + dx < 0 or y1 + dy < 0 or x2 + dx > 620 or y2 + dy > 325:
                        return
                    
                    self.canvas.move(self.item, dx, dy)
                    for text_item in self.text_items:
                        self.canvas.move(text_item, dx, dy)
                    self.is_magnetized = True
                return

            if release:
                if abs(cx - zcx) > 30 or abs(cy - zcy) > 30:
                    self.is_magnetized = False
                return
    
    def update_position(self):
        x1, y1, x2, y2 = self.canvas.bbox(self.item)
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2

        self.response[self.rect_id - 1] = [cx, cy]
        self.callback(self.response)
            


class ChronoApp:
    def __init__(self, master, label, time):
        self.master = master
        self.label = label
        self.time_left = time
        self.update_timer()

    def format_time(self, seconds):
        mins, secs = divmod(seconds, 60)
        return f"{mins:02}:{secs:02}"

    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.label.config(text=self.format_time(self.time_left))
            self.master.after(1000, self.update_timer)



class scoreApp:
    def __init__(self, score = [0, 0]):
        self.rouge = (148, 3, 3)
        self.bleu = (3, 3, 148)

        self.width = 250
        self.height = 40
        self.rayon = 17
        
        if score[0] == 0 and score[1] == 0:
            self.percentageRed = 50
        else:
            redScore = score[0] / (score[0] + score[1]) * 100
            if redScore > 93:
                self.percentageRed = 93
            elif redScore < 7:
                self.percentageRed = 7
            else:
                self.percentageRed = int(redScore)
        
        self.image = self.create_image()

    def create_image(self):
        image = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))

        redImage = Image.new('RGB', (int(self.width * (self.percentageRed / 100)), self.height), self.rouge)
        redMask = Image.new('L', (int(self.width * (self.percentageRed / 100)), self.height), 0)
        draw = ImageDraw.Draw(redMask)
        draw.rectangle((self.rayon, 0, 
                        int(self.width * (self.percentageRed / 100)), self.height), 
                        fill=255)
        draw.rectangle((0, (self.height - (self.height / 2)) / 2, 
                        2 * self.rayon, (self.height + (self.height / 2)) / 2), 
                        fill=255)
        draw.pieslice((0, 0, 
                       2 * self.rayon, 2 * self.rayon), 
                       180, 270, fill=255)
        draw.pieslice((0, self.height - 2 * self.rayon, 
                       2 * self.rayon, self.height), 
                       90, 180, fill=255)
        redImage.putalpha(redMask)


        blueImage = Image.new('RGB', (int(self.width * (1 - (self.percentageRed / 100))), self.height), self.bleu)
        blueMask = Image.new('L', (int(self.width * (1 - (self.percentageRed / 100))), self.height), 0)
        draw = ImageDraw.Draw(blueMask)
        draw.rectangle((0, 0, 
                        int(self.width * (1 - (self.percentageRed / 100))) - self.rayon, self.height), 
                        fill=255)
        draw.rectangle((int(self.width * (1 - (self.percentageRed / 100))) - 2 * self.rayon, (self.height - (self.height / 2)) / 2, 
                        int(self.width * (1 - (self.percentageRed / 100))), (self.height + (self.height / 2)) / 2), 
                        fill=255)
        draw.pieslice((int(self.width * (1 - (self.percentageRed / 100))) - 2 * self.rayon, 0, 
                       int(self.width * (1 - (self.percentageRed / 100))), 2 * self.rayon), 
                       270, 0, fill=255)
        draw.pieslice((int(self.width * (1 - (self.percentageRed / 100))) - 2 * self.rayon, self.height - 2 * self.rayon, 
                       int(self.width * (1 - (self.percentageRed / 100))), self.height), 
                       0, 90, fill=255)
        blueImage.putalpha(blueMask)

        image.paste(redImage, (0, 0), redImage)
        image.paste(blueImage, (int(self.width * (self.percentageRed / 100)), 0), blueImage)


        borderImage = Image.open(paths / "../../assets/quiz/Frame1.png")

        position = ((250 - borderImage.width) // 2, (40 - borderImage.height) // 2)
        image.paste(borderImage, position, borderImage)

        return image
    
    def get(self):
        return ImageTk.PhotoImage(self.image)