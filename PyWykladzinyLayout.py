import sys
from pathlib import Path

import click
from PIL import Image, ImageOps, ImageDraw, ImageFont

import wx


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
        text.text((10, layout.height - text_size * 1.2), tex_path.stem + scale,
                  font=ImageFont.truetype("arial.ttf", text_size),
                  fill=(255, 255, 255), stroke_fill=(0, 0, 0), stroke_width=5)

        layout_path = Path(p.parent / (tex_path.stem + scale + "_layout" + p.suffix))
        layout.save(layout_path, optimize=True, quality=60)


class WxApp(wx.App):
    class DropTarget(wx.FileDropTarget):
        def OnDropFiles(self, x, y, filenames):
            start(filenames)
            return True

    def __init__(self):
        wx.App.__init__(self)
        style = wx.CAPTION | wx.CLOSE_BOX | wx.STAY_ON_TOP
        self.frame = wx.Frame(None, title='Make Layouts', size=(160, 65), style=style)
        self.frame.SetIcon(wx.Icon("./layout_icon.ico"))
        self.panel = wx.Panel(self.frame)
        self.label = wx.StaticText(self.panel, label='drop renders here', pos=(24, 5))
        self.label.SetDropTarget(self.DropTarget())
        self.frame.Center()
        self.frame.Show()


def start(args):
    if len(args) == 0:
        WxApp().MainLoop()
    else:
        images = [valid_image(arg) for arg in args if valid_image(arg) is not None]
        [process_image(img) for img in images]


@click.command()
@click.argument("args", nargs=-1)
def cli(args):
    # with open("parameters.log", "ab") as f:
    #     f.write(str(sys.argv))
    start(args)
    # click.confirm('♥♥♥♥♥♥♥♥♥♥?')


def test():
    # start([r'X:\!Budynki-Xrefy\Warsaw Spire\3d\smieci\WYKLADZINY\2021.10.15 anemone\anemone1_color1_scale2a.jpg'])
    start([])  # force window app run


if getattr(sys, "frozen", False):  # if frozen with pyinstaller
    cli()
else:  # tests are run only if app is not frozen
    test()
