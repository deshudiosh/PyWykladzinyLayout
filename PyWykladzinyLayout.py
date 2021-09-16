import sys
from pathlib import Path
from tkinter import messagebox

import click
from PIL import Image, ImageOps, ImageDraw, ImageFont

from tkinterdnd2 import TkinterDnD, DND_FILES
import tkinter as tk

tbox = None

def validate_image(arg) -> Path:
    """ Return if arg is existing file and is jpg or png"""
    p = Path(arg)
    return p if p.is_file() and p.suffix in ['.jpg', '.png'] else None


def process_image(p: Path):
    if validate_image(p) is None:
        return

    a_path = Path(p.parent / (p.stem + 'a' + p.suffix))
    b_path = Path(p.parent / (p.stem + 'b' + p.suffix))

    if validate_image(a_path) and validate_image(b_path):
        layout = Image.new('RGB', (3840, 2160), (255,255,255))

        b = 5  # border
        b2 = b*2

        rug = Image.open(p)
        rug = ImageOps.fit(rug, (1920-b2, 2160-b2))
        rug = ImageOps.expand(rug, border=b, fill='white')
        layout.paste(rug, box=(0, 0))

        aimg = Image.open(a_path)
        aimg = ImageOps.fit(aimg, (1920-b2, 1080-b2))
        aimg = ImageOps.expand(aimg, border=b, fill='white')
        layout.paste(aimg, box=(1920, 0))

        bimg = Image.open(b_path)
        bimg = ImageOps.fit(bimg, (1920-b2, 1080-b2))
        bimg = ImageOps.expand(bimg, border=b, fill='white')
        layout.paste(bimg, box=(1920, 1080))

        text = ImageDraw.Draw(layout)
        text_size = 80
        text.text((10, layout.height - text_size * 1.2), p.stem, font=ImageFont.truetype("arial.ttf", text_size),
                  fill=(255, 255, 255), stroke_fill=(0, 0, 0), stroke_width=5)


        layout_path = Path(p.parent / (p.stem + "_layout" + p.suffix))
        layout.save(layout_path, optimize=True, quality=60)


class TkWindow:
    def __init__(self):
        self.window = TkinterDnD.Tk()
        self.window.title("Wykladzina Layout")
        self.window.resizable(0,0)
        self.window.attributes("-toolwindow", 1)
        self.window.geometry("200x100")
        self.tbox = tk.Listbox(self.window, selectmode=tk.SINGLE, background="#ffe0d6")
        self.tbox.pack(fill=tk.BOTH)
        self.tbox.drop_target_register(DND_FILES)
        self.tbox.dnd_bind('<<Drop>>', self.tk_files_dropped)
        self.window.mainloop()

    def tk_files_dropped(self, event):
        files = str(event.data).split("} {")
        files = [file.replace('}', '').replace('{', '') for file in files]
        # print(files)
        # start(files)
        messagebox.showinfo("x", event.data)


def start(args):
    if len(args) == 0:
        tkw = TkWindow()
    else:
        images = [validate_image(arg) for arg in args if validate_image(arg) is not None]
        [process_image(img) for img in images]


@click.command()
@click.argument("args", nargs=-1)
def cli(args):
    start(args)
    # click.confirm('♥♥♥♥♥♥♥♥♥♥?')


def test():
    args = [r'X:\!Budynki-Xrefy\Warsaw Spire\3d\smieci\WYKLADZINY\2021.09.10 piasek\PIASEK5.jpg']
    # start(args)
    start([])


if getattr(sys, "frozen", False):
    cli()
else:
    # tests are run only if app is not frozen
    test()
    pass
