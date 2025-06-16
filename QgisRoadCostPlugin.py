from qgis.PyQt.QtWidgets import QAction
from qgis.PyQt.QtGui import QIcon
from qgis.utils import iface
import os
from .gui.main_dialog import MainDialog


class QgisRoadCostPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.action = None
        self.dialog = None

    def initGui(self):
        icon_path = os.path.join(os.path.dirname(__file__), 'resources', 'logo_32x32.png')
        self.action = QAction(QIcon(icon_path), "Qgis Road Cost Plugin", self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("Qgis Road Cost Plugin", self.action)

    def unload(self):
        self.iface.removePluginMenu("Qgis Road Cost Plugin", self.action)
        self.iface.removeToolBarIcon(self.action)

    def run(self):
        if not self.dialog:
            self.dialog = MainDialog(self.iface)
        self.dialog.show()
        self.dialog.raise_()
        self.dialog.activateWindow()
