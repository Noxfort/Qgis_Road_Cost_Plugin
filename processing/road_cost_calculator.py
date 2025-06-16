from qgis.core import QgsProject
from PyQt5.QtCore import QVariant
from qgis.PyQt.QtWidgets import QMessageBox
import csv
import os


def calculate_road_cost(iface, layer_names, cost_per_km, export_txt=False, export_csv=False):
    project = QgsProject.instance()
    total_cost = 0
    total_distance = 0

    for layer in project.mapLayers().values():
        if layer.name() in layer_names:
            distance = 0
            for feat in layer.getFeatures():
                geom = feat.geometry()
                if geom:
                    distance += geom.length() / 1000  # metros para km

            cost = distance * cost_per_km
            total_distance += distance
            total_cost += cost

    message = f"Distância Total: {total_distance:.2f} km\nCusto Total: {total_cost:.2f}"
    QMessageBox.information(iface.mainWindow(), "Resultado", message)

    if export_txt:
        with open(os.path.expanduser("~/road_cost_output.txt"), "w") as f:
            f.write(message)

    if export_csv:
        with open(os.path.expanduser("~/road_cost_output.csv"), "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Distância (km)", "Custo Total"])
            writer.writerow([f"{total_distance:.2f}", f"{total_cost:.2f}"])
