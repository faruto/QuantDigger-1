__author__ = 'Wenwei Huang'

from matplotlib.colors import colorConverter
from matplotlib.collections import PolyCollection
from .aux_renderer import AuxRenderer
import config

class VolumeRenderer(AuxRenderer):
    def __init__(self, df, axes, divider):
        super(VolumeRenderer, self).__init__(axes, divider)
        self.set_data(df)

    def set_data(self, df):
        super(VolumeRenderer, self).set_data(df)
        self.x = self.dates
        self.y = self.volumes

    def plot_bar(self, width=1, alpha=1.0):
        r,g,b = colorConverter.to_rgb(config.colorup)
        colorup = r,g,b,alpha
        r,g,b = colorConverter.to_rgb(config.colordown)
        colordown = r,g,b,alpha
        colord = {True: colorup, False: colordown}
        colors = [colord[open<close] for open, close in zip(self.opens, self.closes)]

        delta = width/2.0
        bars = [((x-delta, 0), (x-delta, y), (x+delta, y), (x+delta, 0)) 
            for x, y in zip(self.x, self.y)]

        barCollection = PolyCollection(bars, facecolors=colors, edgecolors=colors)
        self.axes.add_collection(barCollection)

    def render(self):
        super(VolumeRenderer, self).render()

        self.plot_bar()

    def adjust_ylim(self, xmin, xmax):
        if self.x is None or self.y is None: return
        ys = [y for x, y in zip(self.x, self.y) if xmin<=x<=xmax]
        if not ys: return
        ymin = 0
        ymax = max(ys) + 0.1*(max(ys)-min(ys))
        self.axes.set_ylim([ymin, ymax])

