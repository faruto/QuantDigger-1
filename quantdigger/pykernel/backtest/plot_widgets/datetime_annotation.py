__author__ = 'Wenwei Huang'

import numpy as np
import matplotlib.dates as mdates
from datetime import time, datetime

class DatetimeAnnotation(object):
    def __init__(self, axes, x):
        self.axes = axes
        self.x = x

    def set_visible(self, visible):
        self.annot.set_visible(visible)

    def render(self):
        if self.axes is None: return
        props = dict(boxstyle='round', facecolor='black', alpha=0.8)

        #jself.annot = self.axes.text(
        #j    0, 0, '', transform=self.axes.transAxes, 
        #j    ha='left', va='top', bbox=props)

        self.annot = self.axes.annotate('angle', xy=(3., 1),  xycoords='data',
                xytext=(-50, 30), textcoords='offset points',
                bbox=dict(boxstyle="round", fc="0.8"),
                )
        print '%s' % self.annot

        #self.annot = self.axes.annotate('', xy=(0,0), xycoords='data',
        #    xytext=(0,0), textcoords='data', bbox=props, zorder=100, rotation=30)

    def mouse_move(self, event):
        if not event.inaxes: return
        if self.x is None: return
        x, y = event.xdata, event.ydata
        idx = np.searchsorted(self.x, x)
        if idx >= len(self.x): return
        x = self.x[idx]

        day = mdates.num2date(x)
        if day.time() == time(0,0):
            date_str = datetime.strftime(day, '%b %d %Y')
        else:
            date_str = datetime.strftime(day, '%b %d %Y %H:%M:%S')

        #self.annot.set_position((x, y))
        self.annot.set_text(date_str)
        self.axes.draw_artist(self.annot)
        print 'day %s, x %s, %s' % (date_str, x, self.annot)

    def cleanup(self):
        try:
            self.annot.remove()
        except ValueError:
            import traceback
            logger.warn(traceback.format_exc())

