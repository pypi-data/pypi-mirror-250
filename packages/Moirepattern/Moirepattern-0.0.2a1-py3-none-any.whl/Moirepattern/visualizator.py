import sys
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsItem
from PyQt5.QtSvg import QSvgRenderer, QGraphicsSvgItem
from PyQt5.QtCore import Qt
import tempfile

def visualize(Moire): 
    
    background = tempfile.NamedTemporaryFile(suffix='.svg', delete=False)
    foreground = tempfile.NamedTemporaryFile(suffix='.svg', delete=False)
    
    Moire.export(background.name)
    Moire.export_base(foreground.name)
    
    app = QApplication(sys.argv)
    scene = QGraphicsScene()

   
    item_bg = QGraphicsSvgItem(background.name)
    item_fg = QGraphicsSvgItem(foreground.name)
#center
    item_bg.setPos(-item_bg.boundingRect().width() / 2, -item_bg.boundingRect().height() / 2)
    item_fg.setPos(-item_fg.boundingRect().width() / 2, -item_fg.boundingRect().height() / 2)

    scene.addItem(item_bg)
    scene.addItem(item_fg)
 
    item_fg.setFlag(QGraphicsItem.ItemIsMovable)
    item_fg.setFlag(QGraphicsItem.ItemIsSelectable)

    view = QGraphicsView(scene)
    view.show()
    background.close()
    foreground.close()
    sys.exit(app.exec_())
    