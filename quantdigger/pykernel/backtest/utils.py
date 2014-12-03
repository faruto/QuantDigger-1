__author__ = 'Wenwei Huang'


from PyQt4 import QtCore, QtGui
import os, sys

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)
tr=_translate

fromUtf8 = _fromUtf8
global_shared = {}

class WindowSize(object):
    ONEDAY = 'ONEDAY'
    FIVEDAY = 'FIVEDAY'
    ONEMONTH = 'ONEMONTH'
    THREEMONTH = 'THREEMONTH'
    SIXMONTH = 'SIXMONTH'
    ONEYEAR = 'ONEYEAR'
    TWOYEAR = 'TWOYEAR'
    FIVEYEAR = 'FIVEYEAR'
    MAX = 'MAX'


def sysopen(filename):
    if os.name == 'nt':
        os.startfile(filename)
    elif sys.platform.startswith('darwin'):
        os.system('open %s' % filename)
    elif os.name == 'posix':
        os.system('xdg-open %s' % filename)

def init_global():
    global global_shared
    global_shared = {}


