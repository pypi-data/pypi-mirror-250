# pyqttoolkit
# Copyright (C) 2018-2019, Simmovation Ltd.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QLineEdit

from pyqttoolkit.properties import AutoProperty
from pyqttoolkit.views.styleable import make_styleable

class LineEdit(QLineEdit):
    def __init__(self, parent):
        QLineEdit.__init__(self, parent)
        self.focusLost.connect(self._on_edit_complete)
        self.enterPressed.connect(self._on_edit_complete)

    focusLost = pyqtSignal()
    enterPressed = pyqtSignal()
    editComplete = pyqtSignal(str)

    def focusOutEvent(self, event):
        self.focusLost.emit()
        QLineEdit.focusOutEvent(self, event)
    
    def keyPressEvent(self, event):
        if event.key() in [Qt.Key_Enter, Qt.Key_Return]:
            self.enterPressed.emit()
        QLineEdit.keyPressEvent(self, event)

    def _on_edit_complete(self):
        self.editComplete.emit(self.text())

class BindableLineEdit(LineEdit):
    def __init__(self, parent):
        LineEdit.__init__(self, parent)
        self.editComplete.connect(self._update_value)
        self.valueChanged.connect(self._handle_value_changed)
    
    valueChanged = pyqtSignal(str)

    value = AutoProperty(str)
    
    def _update_value(self, value):
        self.value = value
    
    def _handle_value_changed(self, value):
        self.setText(value)

BindableLineEdit = make_styleable(BindableLineEdit)