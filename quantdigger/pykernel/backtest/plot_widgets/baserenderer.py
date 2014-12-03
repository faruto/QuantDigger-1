__author__ = 'Wenwei Huang'

from .snapcursor import SnaptoCursor
from .pointmarker import PointMarker
from .datetime_annotation import DatetimeAnnotation
from utils import WindowSize
import matplotlib.dates as mdates
from datetime import date, time, datetime, timedelta
import config
from utils import global_shared, tr

class BaseRenderer(object):
    def __init__(self, axes):
        assert axes is not None
        self.axes = axes
        self.render_axes()
        self.x = None
        self.y = None
        self.artists = []

    def set_data(self, df):
        if df is None: return
        self.df = df
        self.dates = self.df['datetime'].values if 'datetime' in self.df.columns else None
        self.opens = self.df['open'].values if 'open' in self.df.columns else None
        self.highs = self.df['high'].values if 'high' in self.df.columns else None
        self.lows = self.df['low'].values if 'low' in self.df.columns else None
        self.closes = self.df['close'].values if 'close' in self.df.columns else None
        self.volumes = self.df['volume'].values if 'volume' in self.df.columns else None

    def render(self):
        for artist in self.artists:
            artist.cleanup()
        self.artists = []

        self.cross_cursor = SnaptoCursor(self.axes, self.x, self.y)
        self.cross_cursor.render()
        self.artists.append(self.cross_cursor)
        if self.axes.name != 'main':
            self.cross_cursor.disable_lx()

        self.marker = PointMarker(self.axes, self.x, self.y)
        self.marker.render()
        self.artists.append(self.marker)

        #self.dt_annot = DatetimeAnnotation(self.axes, self.x)
        #self.dt_annot.render()
        #self.artists.append(self.dt_annot)

    def mouse_move(self, event):
        for artist in self.artists:
            artist.mouse_move(event)

    def drag(self, dx, dy):
        if self.x is None or self.y is None: return
        xmin, xmax = self.axes.get_xlim()
        xmin = xmin+dx
        xmax = xmax+dx
        if min(self.x) > xmin or max(self.x) < xmax: return

        if self.axes.name == 'main':
            self.axes.set_xlim([xmin, xmax])
        self.adjust_ylim(xmin, xmax)

    def set_artist_visible(self, visible):
        for artist in self.artists:
            artist.set_visible(visible)

    def setxlim(self, windowsize):
        if self.x is None or self.y is None: return
        xmax = max(self.x)
        date = mdates.num2date(xmax).date()
        global global_shared
        status_bar = global_shared.get('status_bar')
        if windowsize == WindowSize.ONEDAY:
            if status_bar:
                status_bar.showMessage(tr('ErrorMSG', 'No intraday data', None), 1000)
            return 
        elif windowsize == WindowSize.FIVEDAY:
            if status_bar:
                status_bar.showMessage(tr('ErrorMSG', 'No intraday data', None), 1000)
            return
        elif windowsize == WindowSize.ONEMONTH:
            xmin = mdates.date2num(date-timedelta(days=30))
        elif windowsize == WindowSize.THREEMONTH:
            xmin = mdates.date2num(date-timedelta(days=90))
        elif windowsize == WindowSize.SIXMONTH:
            xmin = mdates.date2num(date-timedelta(days=180))
        elif windowsize == WindowSize.ONEYEAR:
            xmin = mdates.date2num(date-timedelta(days=365))
        elif windowsize == WindowSize.TWOYEAR:
            xmin = mdates.date2num(date-timedelta(days=365*2))
        elif windowsize == WindowSize.FIVEYEAR:
            xmin = mdates.date2num(date-timedelta(days=365*5))
        elif windowsize == WindowSize.MAX:
            xmin = min(self.x)

        self.axes.set_xlim([xmin, xmax])
        self.adjust_ylim(xmin, xmax)

    def adjust_ylim(self, xmin, xmax):
        if self.x is None or self.y is None: return
        ys = [y for x, y in zip(self.x, self.y) if xmin<=x<=xmax]
        ymin = min(ys) - 0.2*(max(ys)-min(ys))
        ymax = max(ys) + 0.2*(max(ys)-min(ys))
        self.axes.set_ylim([ymin, ymax])

    def get_axes(self):
        return self.axes

    def render_axes(self):
        self.axes.spines['bottom'].set_color(config.foregroundcolor)
        self.axes.spines['top'].set_color(config.foregroundcolor) 
        self.axes.spines['right'].set_color(config.foregroundcolor)
        self.axes.spines['left'].set_color(config.foregroundcolor)
        self.axes.tick_params(axis='x', colors=config.foregroundcolor)
        self.axes.tick_params(axis='y', colors=config.foregroundcolor)
        self.axes.yaxis.label.set_color(config.foregroundcolor)
        self.axes.xaxis.label.set_color(config.foregroundcolor)
        self.axes.grid(
            color=config.foregroundcolor, linestyle='-', 
            linewidth=1, alpha=0.2)

