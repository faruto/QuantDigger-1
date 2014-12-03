__author__ = 'Wenwei Huang'

from .aux_renderer import AuxRenderer
import config

class IndicatorRenderer(AuxRenderer):
    def __init__(self, type, df, axes, divider):
        self.type = type
        super(IndicatorRenderer, self).__init__(axes, divider)
        self.axes.name = self.type
        self.set_data(df)
        self.rsi = 14

    def set_data(self, df):
        super(IndicatorRenderer, self).set_data(df)
        self.x = self.dates
        self.y = self.closes

    def render(self):
        super(IndicatorRenderer, self).render()

    def config(self):
        print 'config'

