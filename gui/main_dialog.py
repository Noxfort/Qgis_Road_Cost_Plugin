from qgis.PyQt.QtWidgets import (QDialog, QVBoxLayout, QLabel, QPushButton,
                                 QLineEdit, QFileDialog, QListWidget, QCheckBox, QMessageBox, QListWidgetItem)
from qgis.PyQt.QtGui import QPixmap
from qgis.core import QgsProject
from qgis.PyQt.QtCore import Qt # Import Qt for item flags
import os

from ..processing.road_cost_calculator import calculate_road_cost


class MainDialog(QDialog):
    def __init__(self, iface):
        super().__init__()
        self.iface = iface
        self.setWindowTitle("Qgis Road Cost Plugin")

        layout = QVBoxLayout()

        # Adiciona o logo no topo
        logo_label = QLabel()
        logo_path = os.path.join(os.path.dirname(__file__), '..', 'resources', 'logo_32x32.png')
        pixmap = QPixmap(logo_path)
        logo_label.setPixmap(pixmap)
        layout.addWidget(logo_label)

        layout.addWidget(QLabel("Custo por Km (opcional):"))
        self.cost_input = QLineEdit()
        layout.addWidget(self.cost_input)

        layout.addWidget(QLabel("Selecione as camadas de linha:"))
        self.layer_list = QListWidget()
        # No longer needed: self.layer_list.setSelectionMode(QListWidget.MultiSelection)
        layout.addWidget(self.layer_list)

        self.refresh_layers()
        refresh_button = QPushButton("Atualizar Camadas")
        refresh_button.clicked.connect(self.refresh_layers)
        layout.addWidget(refresh_button)

        self.checkbox_export_txt = QCheckBox("Exportar para TXT")
        self.checkbox_export_csv = QCheckBox("Exportar para CSV")
        layout.addWidget(self.checkbox_export_txt)
        layout.addWidget(self.checkbox_export_csv)

        run_button = QPushButton("Executar")
        run_button.clicked.connect(self.run_calculation)
        layout.addWidget(run_button)

        self.setLayout(layout)

    def refresh_layers(self):
        self.layer_list.clear()
        layers = QgsProject.instance().mapLayers().values()
        for layer in layers:
            if layer.type() == layer.VectorLayer and layer.geometryType() == 1:  # Linhas
                item = QListWidgetItem(layer.name()) # Create a QListWidgetItem
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled | Qt.ItemIsSelectable) # Set flags
                item.setCheckState(Qt.Unchecked) # Set initial state to unchecked
                self.layer_list.addItem(item)

    def run_calculation(self):
        selected_layers = []
        for i in range(self.layer_list.count()):
            item = self.layer_list.item(i)
            if item.checkState() == Qt.Checked:
                selected_layers.append(item.text())

        try:
            cost = float(self.cost_input.text()) if self.cost_input.text() else 0
        except ValueError:
            QMessageBox.warning(self, "Erro", "Custo inválido.")
            return

        if not selected_layers:
            QMessageBox.warning(self, "Erro", "Nenhuma camada selecionada.")
            return

        calculate_road_cost(self.iface, selected_layers, cost,
                            export_txt=self.checkbox_export_txt.isChecked(),
                            export_csv=self.checkbox_export_csv.isChecked())