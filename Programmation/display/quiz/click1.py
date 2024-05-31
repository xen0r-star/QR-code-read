from tkinter import *
from tkinter import font
from PIL import Image, ImageTk, ImageDraw
from pathlib import Path

from widgets.Button import custom_Button
from widgets.Image import custom_Image

paths = Path(__file__).parent.resolve()



class displayClick1(Frame):
    def __init__(self, master, style=1, playerPoint=[0, 0], time=60, currentQuestion = 0, maxQuestion=20, cursorStyle=1):
        super().__init__(master)
        
        self.style = style
        self.cursorStyle = cursorStyle
        self.time = time
        self.playerPoint = playerPoint

        self.questionNumber = f"{currentQuestion}/{maxQuestion}"
        self.responseDistance = [0, 0]
        self.errorRate = [50, 25, 12, 12]

        self.textQuestion = "Quelle est la zone la plus polluée par les voitures ?"
        self.correctResponse = [322, 73]

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

        self.canvas = Canvas(self.body, height=310, width=620, bg=self.master.color_second, highlightthickness=4, highlightbackground="white")
        self.canvas.grid(column=0, row=0)
        self.photo = ImageTk.PhotoImage(Image.open(paths / "../../assets/quiz/World.png"))
        self.canvas.create_image(620 // 2 + 4, 310 // 2 + 4, anchor=CENTER, image=self.photo)
        self.canvas.bind("<Button-1>", self.on_click)


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
    
    def on_click(self, event):
        x, y = event.x, event.y
        self.responseDistance = [x, y]

        if self.cursorStyle >= 4:
            self.image = ImageTk.PhotoImage(Image.open(paths / "../../assets/quiz/Location.png"))

            self.canvas.create_image(
                x, y, anchor=S,
                image=self.image, tags="circle"
            )
        else:
            radius = [[50, 5], [25, 4], [12, 3]]
            size = (radius[self.cursorStyle - 1][0] * 2, radius[self.cursorStyle - 1][0] * 2)
            circle_image = Image.new("RGBA", size, (0, 0, 0, 0))

            draw = ImageDraw.Draw(circle_image)
            draw.ellipse((0, 0, size[0] - 2, size[1] - 2), fill=(200, 61, 61, 200), outline=(193, 30, 30, 200), width=radius[self.cursorStyle - 1][1])

            self.image = ImageTk.PhotoImage(circle_image)

            self.canvas.create_image(
                x - radius[self.cursorStyle - 1][0], y - radius[self.cursorStyle - 1][0], anchor="nw",
                image=self.image, tags="circle"
            )
    
    
    def validate(self):
        if (self.responseDistance[0] >= self.correctResponse[0] - self.errorRate[self.cursorStyle - 1] and 
            self.responseDistance[0] <= self.correctResponse[0] + self.errorRate[self.cursorStyle - 1]) and (
            self.responseDistance[1] >= self.correctResponse[1] - self.errorRate[self.cursorStyle - 1] and 
            self.responseDistance[1] <= self.correctResponse[1] + self.errorRate[self.cursorStyle - 1]):

            print(1)
        else:
            print(0)



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