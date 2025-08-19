from customtkinter import *
from tkinter import *
from tkinter import messagebox as mb
from tkinter import filedialog as fd
import os, random, json, subprocess
from PIL import Image, ImageTk, ImageDraw
from tkinter.font import *
from tkinter import colorchooser

from utils.generator import generator

class THEME:
    PRIMARY = "#202020"
    PRIMARY_LIGHT = "#2C2C2C"
    PRIMARY_EXTRA_LIGHT = "#3C3C3C"
    SECONDARY = "#FFFFFF"
    SECONDARY_LIGHT = "#F0F0F0"
    TEXT_COLOR = "white"
    TEXT_COLOR_S = "#D8D8D8"
    TEXT_COLOR_D = "#4C4C4C"
    TEXT_COLOR_R = ("#000000", "#202020")
    
class GUI(CTk):
    content = None
    isEmpty = True
    qrCode = None
    image_path = None
    backColor = "#FFFFFF"
    frontColor = "#202020"
    border = 4
    
    def __init__(self):
        super().__init__()
        self.title("QR Code Generator")
        self.geometry("1150x600")
        self.resizable(False, False)
        self.config(bg=THEME.PRIMARY)

        self.create_widgets()

    def create_widgets(self):
        self.header = CTkLabel(self, text="QR Code Generator", font=("Arial", 48), fg_color=THEME.PRIMARY, bg_color=THEME.PRIMARY, text_color=THEME.TEXT_COLOR)
        self.header.pack(padx=24, pady=24, side=TOP, anchor="nw")

        self.contentEntryHead = CTkLabel(self, text="Enter Content:", font=("Arial", 18), fg_color=THEME.PRIMARY, bg_color=THEME.PRIMARY, text_color=THEME.TEXT_COLOR_S)
        self.contentEntryHead.pack(padx=24, pady=(24, 5), side=TOP, anchor="nw")

        self.contentEntry = CTkTextbox(self, text_color=THEME.TEXT_COLOR, border_width=0, corner_radius=7.5, fg_color=THEME.PRIMARY_LIGHT, bg_color=THEME.PRIMARY, height=210, width=725, font=("Arial", 16))
        self.contentEntry.pack(padx=24, pady=(5, 24), side=TOP, anchor="nw")
        
        if self.isEmpty:
            self.qrArea = CTkFrame(self, fg_color=THEME.PRIMARY_LIGHT, bg_color=THEME.PRIMARY, corner_radius=15, width=350, height=350, border_width=3, border_color=THEME.PRIMARY_EXTRA_LIGHT)
            self.qrArea.place(x=776, y=25)
            
            self.thereIsEmpty = CTkLabel(self.qrArea, text="QR Code", font=("Arial", 24, BOLD), fg_color=THEME.PRIMARY_LIGHT, bg_color=THEME.PRIMARY, text_color=THEME.TEXT_COLOR_D)
            self.thereIsEmpty.place(relx=0.5, rely=0.5, anchor="center")

        else:
            self.qrArea = CTkFrame(self, fg_color=THEME.PRIMARY_LIGHT, bg_color=THEME.PRIMARY, corner_radius=7.5, width=350, height=350, border_width=3, border_color=THEME.PRIMARY_EXTRA_LIGHT)
            self.qrArea.place(x=776, y=25)
            
            self.qrCode = ImageTk.PhotoImage(Image.open(self.image_path))
            self.qrCodeLabel = CTkLabel(self.qrArea, text="", corner_radius=15, image=self.qrCode, fg_color=THEME.PRIMARY_LIGHT, bg_color=THEME.PRIMARY)
            self.qrCodeLabel.pack(padx=0, pady=0)
            
        self.frontColorArea = CTkFrame(self, fg_color=THEME.PRIMARY_LIGHT, bg_color=THEME.PRIMARY, corner_radius=7.5, width=350, height=50, border_width=3, border_color=THEME.PRIMARY_EXTRA_LIGHT)
        self.frontColorArea.place(x=24, y=400)
        
        self.frontColorLabel = CTkLabel(self.frontColorArea, text="Front Color:", font=("Arial", 16), fg_color=THEME.PRIMARY_LIGHT, bg_color=THEME.PRIMARY, text_color=THEME.TEXT_COLOR_S)
        self.frontColorLabel.pack(padx=12, pady=12, side=LEFT, anchor="nw")
        
        self.frontColorButton = CTkButton(self.frontColorArea, text="", command=lambda: self.selectFrontColor(), font=("Arial", 16), height=35, corner_radius=7.5, fg_color=self.frontColor, text_color=THEME.TEXT_COLOR_R[1], hover=None)
        self.frontColorButton.pack(padx=12, pady=12, side=RIGHT, anchor="ne")

        self.backColorArea = CTkFrame(self, fg_color=THEME.PRIMARY_LIGHT, bg_color=THEME.PRIMARY, corner_radius=7.5, width=350, height=50, border_width=3, border_color=THEME.PRIMARY_EXTRA_LIGHT)
        self.backColorArea.place(x=322, y=400)
        
        self.backColorLabel = CTkLabel(self.backColorArea, text="Back Color:", font=("Arial", 16), fg_color=THEME.PRIMARY_LIGHT, bg_color=THEME.PRIMARY, text_color=THEME.TEXT_COLOR_S)
        self.backColorLabel.pack(padx=12, pady=12, side=LEFT, anchor="nw")
        
        self.backColorButton = CTkButton(self.backColorArea, text="", command=lambda: self.selectBackColor(), font=("Arial", 16), height=35, corner_radius=7.5, fg_color=self.backColor, text_color=THEME.TEXT_COLOR_R[1], hover=None)
        self.backColorButton.pack(padx=12, pady=12, side=RIGHT, anchor="ne")

        self.resetColorsButton = CTkButton(self, text="↺", command=lambda: (self.frontColorButton.configure(fg_color=self.frontColor), self.backColorButton.configure(fg_color=self.backColor)), font=("Sans Serif", 24), height=35, width=35, corner_radius=7.5, fg_color=THEME.SECONDARY, text_color=THEME.TEXT_COLOR_R[1], hover_color=THEME.SECONDARY_LIGHT)
        self.resetColorsButton.place(x=620, y=412)

        self.borderWidthLabel = CTkLabel(self, text=f"Border Space: {self.border}", font=("Arial", 16), fg_color=THEME.PRIMARY, bg_color=THEME.PRIMARY, text_color=THEME.TEXT_COLOR_S)
        self.borderWidthLabel.place(x=24, y=477.5)
        
        self.borderWidth = CTkSlider(self, from_=0, to=10, number_of_steps=10, command=lambda value: self.changeBorder(value), width=200, height=20, corner_radius=7.5, fg_color=THEME.PRIMARY_LIGHT, bg_color=THEME.PRIMARY, button_color=THEME.SECONDARY, button_hover_color=THEME.SECONDARY_LIGHT)
        self.borderWidth.set(self.border)
        self.borderWidth.place(x=22, y=510)

        self.generateButton = CTkButton(self, text="Generate", command=self.generate_qr_code, font=("Arial", 16), height=35, corner_radius=7.5, fg_color=THEME.SECONDARY, text_color=THEME.TEXT_COLOR_R[1], hover_color=THEME.SECONDARY_LIGHT)
        self.generateButton.pack(padx=24, pady=(5, 24), side=BOTTOM, anchor="se")
        
    def changeBorder(self, value):
        self.border = int(value)
        self.borderWidthLabel.configure(text=f"Border Space: {self.border}")
    
    def selectFrontColor(self):
        color = colorchooser.askcolor(title="Select Front Color", initialcolor=self.frontColor)
        if color:
            self.frontColor = color[1]
            self.frontColorButton.configure(fg_color=self.frontColor)

    def selectBackColor(self):
        color = colorchooser.askcolor(title="Select Back Color", initialcolor=self.backColor)
        if color:
            self.backColor = color[1]
            self.backColorButton.configure(fg_color=self.backColor)

    def round_corners(self,image, radius):
        mask = Image.new("L", image.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle([0, 0, image.size[0], image.size[1]], radius=radius, fill=255)

        rounded = image.convert("RGBA")
        rounded.putalpha(mask)
        return rounded


    def generate_qr_code(self):
        content = self.contentEntry.get("1.0", "end-1c").strip()
        if not content:
            mb.showerror("Error", "Content cannot be empty!")
            return
        
        try:
            self.image, self.image_path = generator(content, self.frontColor, self.backColor, self.border)
            self.isEmpty = False
            
            if hasattr(self, 'qrCodeLabel'):
                self.qrCodeLabel.destroy()
            
            img = Image.open(self.image_path).resize((342, 342), Image.LANCZOS)

            img = self.round_corners(img, radius=12.5)

            self.qrCode = ImageTk.PhotoImage(img)

            self.qrCodeLabel = CTkLabel(
                self.qrArea,
                text="",
                image=self.qrCode,
                fg_color=THEME.PRIMARY_EXTRA_LIGHT,
                bg_color=THEME.PRIMARY_EXTRA_LIGHT,
                cursor="hand2"
            )
            self.qrCodeLabel.place(x=4, y=4)
            self.qrCodeLabel.bind(
                "<Button-1>",
                lambda e: subprocess.run(["explorer", "/select,", os.path.normpath(self.image_path)])
            )

        except Exception as e:
            mb.showerror("Error", f"Failed to generate QR Code: {e}")

def start():
    app = GUI()
    app.mainloop()

if __name__ == "__main__":
    start()