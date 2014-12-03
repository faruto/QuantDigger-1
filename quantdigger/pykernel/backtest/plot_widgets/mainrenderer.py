__author__ = 'Wenwei Huang'

from matplotlib.colors import colorConverter
from matplotlib.collections import PolyCollection
from matplotlib.collections import LineCollection

from .ohlc_textbox import OHLCVTextBox
from .baserenderer import BaseRenderer
import config
import collections

class MainRenderer(BaseRenderer):
    def __init__(self, axes, df):
        super(MainRenderer, self).__init__(axes)
        self.ohlcvtextbox = None
        self.set_data(df)

    def set_data(self, df):
        super(MainRenderer, self).set_data(df)
        self.x = self.dates
        self.y = self.closes

    def render(self):
        super(MainRenderer, self).render()
        if self.x is None or self.y is None: return

        self.ohlcvtextbox = OHLCVTextBox(self.axes, self.df)
        self.ohlcvtextbox.render()
        self.artists.append(self.ohlcvtextbox)

        self.lines = self.axes.plot(
            self.x, self.y, '-', color=config.main_curve_color)

        self.axes.yaxis.tick_right()

    def remove_lines(self):
        if self.lines:
            if isinstance(self.lines, collections.Iterable):
                for line in self.lines:
                    line.remove()
                    del line
            else:
                self.lines.remove()
                del self.lines

    def candlestick(self, width=0.2, alpha=1.0):
        delta = width/2.0
        r,g,b = colorConverter.to_rgb(config.colorup)
        colorup = r,g,b,alpha
        r,g,b = colorConverter.to_rgb(config.colordown)
        colordown = r,g,b,alpha
        colord = {True: colorup, False: colordown}
        colors = [colord[open<close] for open, close in zip(self.opens, self.closes)]

        bars = [((dt-delta, close), (dt-delta, open), (dt+delta, open), (dt+delta, close)) 
            for dt, open, close in zip(self.dates, self.opens, self.closes)]
        lines = [((dt, low), (dt, high))
            for dt, high, low in zip(self.dates, self.highs, self.lows)]

        barCollection = PolyCollection(bars, facecolors=colors, edgecolors=colors)
        lineCollection = LineCollection(lines, colors=colors)
        self.axes.add_collection(barCollection)
        self.axes.add_collection(lineCollection)

        self.lines = [barCollection, lineCollection]

    def plot_bar(self, width=0.4, alpha=1.0):
        delta = width/2.0
        r,g,b = colorConverter.to_rgb(config.colorup)
        colorup = r,g,b,alpha
        r,g,b = colorConverter.to_rgb(config.colordown)
        colordown = r,g,b,alpha
        colord = {True: colorup, False: colordown}
        colors = [colord[open<close] for open, close in zip(self.opens, self.closes)]

        lines = [((dt, low), (dt, high))
            for dt, high, low in zip(self.dates, self.highs, self.lows)]

        lines2 = [((dt, open), (dt-delta, open))
            for dt, open in zip(self.dates, self.opens)]

        lines3 = [((dt, close), (dt+delta, close))
            for dt, close in zip(self.dates, self.closes)]

        lineCollection = LineCollection(lines, colors=colors)
        lineCollection2 = LineCollection(lines2, colors=colors)
        lineCollection3 = LineCollection(lines3, colors=colors)

        self.axes.add_collection(lineCollection)
        self.axes.add_collection(lineCollection2)
        self.axes.add_collection(lineCollection3)

        self.lines = [lineCollection, lineCollection2, lineCollection3]

    def change_plot_style(self, style):
        if self.x is None or self.y is None: return

        if style == 'Line':
            self.remove_lines()
            self.lines = self.axes.plot(
                self.x, self.y, '-', color=config.main_curve_color)

        elif style == 'Area':
            self.remove_lines()
            polygon = self.axes.fill_between(
                self.x, self.y, color=config.main_curve_color, alpha=0.1)
            self.lines = self.axes.plot(
                self.x, self.y, '-', color=config.main_curve_color)
            self.lines.append(polygon)

        elif style == 'Bar':
            self.remove_lines()
            self.plot_bar()

        elif style == 'Candle':
            self.remove_lines()
            self.candlestick()

