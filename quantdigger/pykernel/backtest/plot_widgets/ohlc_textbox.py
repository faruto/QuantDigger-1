__author__ = 'Wenwei Huang'

import numpy as np
import matplotlib.dates as mdates
from datetime import time, datetime
import config

class OHLCVTextBox(object):
    def __init__(self, axes, df):
        self.axes = axes
        self.set_data(df)

    def set_data(self, df):
        if df is None: return
        self.dates = df['datetime'].values if 'datetime' in df.columns else None
        self.opens = df['open'].values if 'open' in df.columns else None
        self.highs = df['high'].values if 'high' in df.columns else None
        self.lows = df['low'].values if 'low' in df.columns else None
        self.closes = df['close'].values if 'close' in df.columns else None
        self.volumes = df['volume'].values if 'volume' in df.columns else None

    def set_visible(self, visible):
        self.txt.set_visible(visible)

    def render(self):
        if self.axes is None: return
        props = dict(boxstyle='round', facecolor=config.backgroundcolor, 
            edgecolor=config.foregroundcolor)
        self.txt = self.axes.text(
            0.005, 0.99, '', transform=self.axes.transAxes, name='monospace',
            size='smaller', va='top', bbox=props,
            fontdict={'color': config.foregroundcolor})

    def mouse_move(self, event):
        if not event.inaxes: return
        if self.dates is None: return
        x, y = event.xdata, event.ydata
        idx = np.searchsorted(self.dates, x)
        if idx >= len(self.dates): return
        x = self.dates[idx]

        text = []
        open = self.opens[idx] if self.opens is not None and idx < len(self.opens) else None
        close = self.closes[idx] if self.closes is not None and idx < len(self.closes) else None
        high = self.highs[idx] if self.highs is not None and idx < len(self.highs) else None
        low = self.lows[idx] if self.lows is not None and idx < len(self.lows) else None
        vol = self.volumes[idx] if self.volumes is not None and idx < len(self.volumes) else None
        day = mdates.num2date(x)
        if day.time() == time(0,0):
            date_str = datetime.strftime(day, '%b %d %Y')
        else:
            date_str = datetime.strftime(day, '%b %d %Y %H:%M:%S')
        text.append("{0:>5s} {1:<12s}".format('Date', date_str))
        if open:
            text.append("{0:>5s} {1:.2f}".format('Open', open))
        if close:
            text.append("{0:>5s} {1:.2f}".format('Close', close))
        if high:
            text.append("{0:>5s} {1:.2f}".format('High', high))
        if low:
            text.append("{0:>5s} {1:.2f}".format('Low', low))
        if vol:
            text.append("{0:>5s} {1:.2f}M".format('Vol', (float(vol)/1000000)))
        self.txt.set_text('\n'.join(text))

        self.axes.draw_artist(self.txt)

    def cleanup(self):
        try:
            self.txt.remove()
        except ValueError:
            import traceback
            logger.warn(traceback.format_exc())

