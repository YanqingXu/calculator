"""基础UI组件模块"""
from PySide2.QtWidgets import QWidget
from PySide2.QtGui import QPainter
from PySide2.QtCore import Qt

class BackgroundWidget(QWidget):
    """支持背景图片的基础部件"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.background_pixmap = None
        
    def setBackgroundPixmap(self, pixmap):
        """设置背景图片"""
        self.background_pixmap = pixmap
        self.update()
        
    def paintEvent(self, event):
        """绘制背景"""
        if self.background_pixmap:
            painter = QPainter(self)
            painter.setOpacity(0.5)  # 设置透明度为50%
            scaled_pixmap = self.background_pixmap.scaled(
                self.size(),
                Qt.KeepAspectRatioByExpanding,
                Qt.SmoothTransformation
            )
            # 居中绘制
            x = (self.width() - scaled_pixmap.width()) // 2
            y = (self.height() - scaled_pixmap.height()) // 2
            painter.drawPixmap(x, y, scaled_pixmap)
