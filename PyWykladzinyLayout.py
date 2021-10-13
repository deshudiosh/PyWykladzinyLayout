import sys
from pathlib import Path
from tkinter import messagebox

import click
from PIL import Image, ImageOps, ImageDraw, ImageFont

from tkinterdnd2 import TkinterDnD, DND_FILES
import tkinter as tk


def valid_image(arg) -> Path:
    """ Return if arg is existing file and is jpg or png"""
    p = Path(arg)
    return p if p.is_file() and p.suffix in ['.jpg', '.png'] else None


def process_image(p: Path):
    last = p.stem[-1]

    if last == 'a' or last == 'b':
        scale = p.stem.find('_scale')

        if scale > -1:
            scale = p.stem[scale:-1]
            tex_path = Path(p.parent / (p.stem[:-(len(scale)+1)] + p.suffix))
        else:
            scale = ""
            tex_path = Path(p.parent / (p.stem[:-1] + p.suffix))

    else:
        return

    a_path = Path(p.parent / (tex_path.stem + scale + 'a' + p.suffix))
    b_path = Path(p.parent / (tex_path.stem + scale + 'b' + p.suffix))

    if valid_image(tex_path) and valid_image(a_path) and valid_image(b_path):
        layout = Image.new('RGB', (3840, 2160), (255, 255, 255))

        b = 5  # border
        b2 = b*2

        rug = Image.open(tex_path)
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

        layout_path = Path(p.parent / (tex_path.stem + scale + "_layout" + p.suffix))
        layout.save(layout_path, optimize=True, quality=60)


# TODO: CAN"T MAKE THIS SHIT TO WORK WHEN FROZEN WITH PYINSTALLER!
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
        # files = str(event.data).split("} {")
        # files = [file.replace('}', '').replace('{', '') for file in files]
        # print(files)
        # start(files)
        messagebox.showinfo("x", event.data)


def start(args):
    if len(args) == 0:
        tkw = TkWindow()
    else:
        images = [valid_image(arg) for arg in args if valid_image(arg) is not None]
        [process_image(img) for img in images]


@click.command()
@click.argument("args", nargs=-1)
def cli(args):
    start(args)
    # click.confirm('♥♥♥♥♥♥♥♥♥♥?')


def test():
    # start([r'X:\!Budynki-Xrefy\Warsaw Spire\3d\smieci\WYKLADZINY\2021.10.12 grz bumps\bumps_linie1a.jpg',
    #        r'X:\!Budynki-Xrefy\Warsaw Spire\3d\smieci\WYKLADZINY\2021.10.12 grz bumps\bumps_linie1b.jpg',
    #        r'X:\!Budynki-Xrefy\Warsaw Spire\3d\smieci\WYKLADZINY\2021.10.12 grz bumps\bumps_linie1_scale2a.jpg',
    #        r'X:\!Budynki-Xrefy\Warsaw Spire\3d\smieci\WYKLADZINY\2021.10.12 grz bumps\bumps_linie1_scale2b.jpg',
    #        r'X:\!Budynki-Xrefy\Warsaw Spire\3d\smieci\WYKLADZINY\2021.10.12 grz bumps\bumps_brick1_scale1b.jpg',
    #        r'X:\!Budynki-Xrefy\Warsaw Spire\3d\smieci\WYKLADZINY\2021.10.12 grz bumps\bumps_brick1_scale2a.jpg'])
    start([])  # force tkinter window app run


if getattr(sys, "frozen", False):  # if frozen with pyinstaller
    cli()
else:  # tests are run only if app is not frozen
    test()
