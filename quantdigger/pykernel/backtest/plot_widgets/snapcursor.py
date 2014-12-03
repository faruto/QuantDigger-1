__author__ = 'Wenwei Huang'

import numpy as np
import config

class SnaptoCursor(object):
    def __init__(self, axes, x, y):
        self.x, self.y = x, y
        self.axes = axes
    
    def render(self):
        if self.axes is None: return
        self.lx = self.axes.axhline(color=config.foregroundcolor, linestyle=':')
        self.ly = self.axes.axvline(color=config.foregroundcolor, linestyle=':')
        self.lx.disable=False
        self.ly.disable=False

    def disable_lx(self):
        self.lx.disable=True
        self.lx.set_visible(False)
        
    def disable_ly(self):
        self.ly.disable=True
        self.ly.set_visible(False)

    def set_visible(self, visible):
        if not self.lx.disable:
            self.lx.set_visible(visible)
        if not self.ly.disable:
            self.ly.set_visible(visible)

    def mouse_move(self, event):
        if not event.inaxes: return
        if self.x is None or self.y is None: return
        x, y = event.xdata, event.ydata
        idx = np.searchsorted(self.x, x)
        if idx >= len(self.x): return
        x = self.x[idx]
        y = self.y[idx]
        # update the line positions self.ly.set_xdata(x)
        self.lx.set_ydata(y)
        self.ly.set_xdata(x)

        self.axes.draw_artist(self.lx)
        self.axes.draw_artist(self.ly)
        
    def cleanup(self):
        try:
            self.lx.remove()
            self.ly.remove()
        except ValueError:
            import traceback
            logger.warn(traceback.format_exc())

    def __repr__(self):
        return "axes: %s" % self.axes.name

