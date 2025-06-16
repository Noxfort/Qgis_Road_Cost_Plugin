from .QgisRoadCostPlugin import QgisRoadCostPlugin

def classFactory(iface):
    return QgisRoadCostPlugin(iface)
