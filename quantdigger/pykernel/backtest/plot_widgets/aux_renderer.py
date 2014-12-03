__author__ = 'Wenwei Huang'

from .baserenderer import BaseRenderer
import config

class AuxRenderer(BaseRenderer):
    def __init__(self, axes, divider):
        self.axes = divider.append_axes(
            'bottom', size="20%", pad=0.2, sharex=axes,
            axisbg=config.backgroundcolor)
        super(AuxRenderer, self).__init__(self.axes)


