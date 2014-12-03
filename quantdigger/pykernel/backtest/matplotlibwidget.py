__author__ = 'Wenwei Huang'

import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

from plot_widgets.volumerenderer import VolumeRenderer
from plot_widgets.mainrenderer import MainRenderer
from plot_widgets.indicator_renderer import IndicatorRenderer

import logging
import config
logger = logging.getLogger(__name__)

class MatplotlibWidget(FigureCanvasQTAgg):
    def __init__(self, parent=None):
        self.fig = Figure(facecolor=config.backgroundcolor)
        super(MatplotlibWidget, self).__init__(self.fig)
        self.setParent(parent)
        self.fig.subplots_adjust(top=0.95, left=0.05, right=0.95, bottom=0.05, hspace=0)
        self.press = None
        self.df = None
        self.divider = None
        self.renderers = {}
        self.renderer_backgrounds = {}

    def connect(self):
        self.cidpress = self.fig.canvas.mpl_connect(
            "button_press_event", self.on_press)
        self.cidrelease = self.fig.canvas.mpl_connect(
            "button_release_event", self.on_release)
        self.cidmotion = self.fig.canvas.mpl_connect(
            "motion_notify_event", self.on_motion)
        self.cidresize = self.fig.canvas.mpl_connect(
            "resize_event", self.on_resize)
        self.cidscroll = self.fig.canvas.mpl_connect(
            "scroll_event", self.on_scroll)

    def disconnect(self):
        self.fig.canvas.mpl_disconnect(self.cidresize)
        self.fig.canvas.mpl_disconnect(self.cidmotion)
        self.fig.canvas.mpl_disconnect(self.cidrelease)
        self.fig.canvas.mpl_disconnect(self.cidpress)

    def add_main_renderer(self):
        axes = self.fig.add_subplot(111, axisbg=config.backgroundcolor)
        axes.name = 'main'
        main_renderer = MainRenderer(axes, self.df)
        self.renderers['main'] = main_renderer
        self.divider = make_axes_locatable(axes)

    def add_volume_renderer(self):
        main_renderer = self.renderers.get('main')
        if main_renderer:
            main_axes = main_renderer.get_axes()
            volume_renderer = VolumeRenderer(self.df, main_axes, self.divider)
            axes = volume_renderer.get_axes()
            axes.name = 'volume'
            self.renderers['volume'] = volume_renderer

    def set_data(self, df):
        if df is None: return
        self.df = df

    def setxlim(self, windowsize):
        for renderer in self.renderers.values():
            renderer.setxlim(windowsize)
        self.fig.canvas.draw()
        self.update_backgrounds()

    def update_backgrounds(self):
        for renderer in self.renderers.values():
            renderer.set_artist_visible(False)
        self.fig.canvas.draw()
        for renderer in self.renderers.values():
            axes = renderer.get_axes()
            background = self.fig.canvas.copy_from_bbox(axes.bbox)
            self.renderer_backgrounds[axes] = background
            renderer.set_artist_visible(True)
        self.fig.canvas.draw()

    def render(self):
        if self.df is None: return
        for key in self.renderers.keys()[:]:
            renderer = self.renderers.pop(key)
            axes = renderer.get_axes()
            self.fig.delaxes(axes)
            if axes in self.renderer_backgrounds:
                self.renderer_backgrounds.pop(axes)

        self.add_main_renderer()

        if 'volume' in self.df.columns:
            self.add_volume_renderer()

        for renderer in self.renderers.values():
            renderer.render()

        self.update_backgrounds()

    def on_press(self, event):
        if event.inaxes is not None:
            self.press = event.xdata, event.ydata
            print event.inaxes.name

    def on_release(self, event):
        if self.press is not None:
            self.update_backgrounds()
        self.press = None

    def on_motion(self, event):
        if event:
            if self.press is None:
                for renderer in self.renderers.values():
                    axes = renderer.get_axes()
                    background = self.renderer_backgrounds.get(axes, None)
                    self.fig.canvas.restore_region(background)
                    renderer.mouse_move(event)
                    self.fig.canvas.blit(axes.bbox)

            else:
                if event.xdata is not None:
                    # drag
                    xpress, ypress = self.press
                    dx =  xpress - event.xdata
                    dy =  ypress - event.ydata
                    for renderer in self.renderers.values():
                        renderer.drag(dx, dy)
                    self.fig.canvas.draw()

    def on_resize(self, event):
        self.update_backgrounds()

    def on_scroll(self, event):
        print 'scroll'

    def on_change_plot_style(self, action):
        renderer = self.renderers['main']
        if isinstance(renderer, MainRenderer):
            renderer.change_plot_style(action.text())
            self.update_backgrounds()

    def get_bottom_axes(self):
        low_y = 1
        bottom_axes = None
        for renderer in self.renderers.values():
            axes = renderer.get_axes()
            if low_y > axes.get_position().ymin:
                low_y = axes.get_position().ymin
                bottom_axes = axes
        return bottom_axes

    def add_indicator(self, action):
        indicator_type = action.data().toPyObject()
        main_axes = self.renderers['main'].get_axes()
        if not main_axes: return
        if indicator_type in self.renderers: return
        xmin, xmax = main_axes.get_xlim()
        renderer = IndicatorRenderer(indicator_type, self.df, main_axes, self.divider)
        axes = renderer.get_axes()
        self.renderers[indicator_type] = renderer
        renderer.render()
        axes.set_xlim(xmin, xmax)
        renderer.adjust_ylim(xmin, xmax)
        self.update_backgrounds()


