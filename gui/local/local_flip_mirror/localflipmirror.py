# -*- coding: utf-8 -*-

"""

Qudi is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Qudi is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Qudi. If not, see <http://www.gnu.org/licenses/>.

Copyright (c) the Qudi Developers. See the COPYRIGHT.txt file at the
top-level directory of this distribution and at <https://github.com/Ulm-IQO/qudi/>
"""

import os

from core.connector import Connector
from gui.guibase import GUIBase
from gui.colordefs import QudiPalettePale as palette
from qtpy import QtWidgets
from qtpy import QtCore
from qtpy import uic
import time

class LocalFlipMirrorMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        this_dir = os.path.dirname(__file__)
        ui_file = os.path.join(this_dir,'ui_localflipmirror.ui')

        super().__init__()
        uic.loadUi(ui_file, self)
        self.show



class LocalFlipMirrorGui(GUIBase):
    localflipmirrorlogic = Connector(interface='LocalFlipMirrorLogic')
    def __init__(self, config, **kwargs):
        super().__init__(config=config, **kwargs)
    def on_activate(self):
        
        self._flip_mirror_logic = self.localflipmirrorlogic()
    
        self._mw= LocalFlipMirrorMainWindow()

        self._mw.setDockNestingEnabled(True)

        self._angle= self._flip_mirror_logic._current_angle

        self._mw.actionStart.triggered.connect(self.attach_clicked)
        self._mw.actionStop.triggered.connect(self.detach_clicked)

        self._mw.statuspushbutton.clicked.connect(self.flipmirror)
        self.show()
    
    def show(self):
        """Make window visible and put it above all other windows. """
        self._mw.show()
        self._mw.activateWindow()
        self._mw.raise_()

    def on_deactivate(self):
        self._mw.actionStart.triggered.disconnect()
        self._mw.actionStop.triggered.disconnect()

        self._mw.statuspushbutton.clicked.disconnect()
        return 0


    def detach_clicked(self):
        self._flip_mirror_logic.detach()
        self._mw.statuspushbutton.setDisabled(True)
        self._mw.actionStart.setEnabled(True)
        self._mw.actionStop.setDisabled(True)
    def attach_clicked(self):
        self._flip_mirror_logic.attach()
        self._mw.statuspushbutton.setEnabled(True)
        self._mw.actionStart.setDisabled(True)
        self._mw.actionStop.setEnabled(True)
    def flipmirror(self):
        self._mw.statuspushbutton.setDisabled(True)

        if  self._mw.statuspushbutton.text()=='off':
            self._flip_mirror_logic.move_abs(90)
            self._mw.statuspushbutton.setText('on')
        else:
            self._flip_mirror_logic.move_abs(0)
            self._mw.statuspushbutton.setText('off')
        self._mw.statuspushbutton.setEnabled(True)


    

