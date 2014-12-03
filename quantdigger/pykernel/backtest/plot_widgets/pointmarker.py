__author__ = 'Wenwei Huang'

import numpy as np
import config

class PointMarker(object):
    def __init__(self, axes, x, y):
        self.axes = axes
        self.x, self.y = x, y

    def render(self):
        if self.axes is None: return
        self.marker,  = self.axes.plot(
            -1, -1, 'o', color=config.foregroundcolor, alpha=0.5, zorder=10)

    def set_visible(self, visible):
        self.marker.set_visible(visible)

    def mouse_move(self, event):
        if not event.inaxes: return
        if self.x is None or self.y is None: return
        x, y = event.xdata, event.ydata
        idx = np.searchsorted(self.x, x)
        if idx >= len(self.x): return
        x = self.x[idx]
        y = self.y[idx]
        self.marker.set_xdata(x)
        self.marker.set_ydata(y)

        self.axes.draw_artist(self.marker)

    def cleanup(self):
        try:
            self.marker.remove()
        except ValueError:
            import traceback
            logger.warn(traceback.format_exc())

