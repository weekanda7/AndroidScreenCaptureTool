import os
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QGraphicsScene, QGraphicsView, QListWidget, QFileDialog, QFrame , QMainWindow
from PyQt6.QtCore import Qt, QRectF, QPoint, QPointF, QSizeF
from PyQt6.QtGui import QPixmap, QImageReader, QPainter, QPen, QColor

class CroppableImageView(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        self.crop_rect = None
        self.start = QPointF()
        self.end = QPointF()

    def set_image(self, pixmap):
        self.scene.clear()
        self.scene.addPixmap(pixmap)
        self.setSceneRect(QRectF(pixmap.rect()))

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.start = self.mapToScene(event.position().toPoint())
            if not self.crop_rect:
                self.crop_rect = self.scene.addRect(QRectF(self.start, QSizeF()), QPen(QColor(255, 0, 0), 2))



    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            self.end = self.mapToScene(event.position().toPoint())
            self.crop_rect.setRect(QRectF(self.start, self.end).normalized())

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.end = self.mapToScene(event.position().toPoint())
            self.crop_rect.setRect(QRectF(self.start, self.end).normalized())

    def get_cropped_image(self):
        if self.crop_rect:
            crop_rect = self.crop_rect.rect()

            # Temporarily remove the red rectangle
            self.scene.removeItem(self.crop_rect)

            image = QPixmap(self.scene.sceneRect().size().toSize())
            image.fill(Qt.GlobalColor.transparent)
            painter = QPainter(image)
            self.scene.render(painter)
            painter.end()

            # Add the red rectangle back to the scene
            self.crop_rect = self.scene.addRect(crop_rect, QPen(QColor(255, 0, 0), 2))

            return image.copy(crop_rect.toRect())

        return None


class ScreenCaptureApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Screen Capture Tool")
        self.setGeometry(100, 100, 1400, 800)

        self.image_view = CroppableImageView()

        # Device list
        self.device_list = QListWidget()
        self.device_list.setMaximumWidth(200)  # Set the maximum width for the device list
        self.device_list.itemClicked.connect(self.change_device)
        # Refresh and Capture buttons
        self.refresh_button = QPushButton("Refresh Devices")
        self.capture_button = QPushButton("Capture Screen")
        self.crop_button = QPushButton("Crop Image")

        # Connect signals and slots
        self.refresh_button.clicked.connect(self.refresh_devices)
        self.capture_button.clicked.connect(self.capture_screenshot)
        self.crop_button.clicked.connect(self.crop_image)

        # Layouts
        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        left_layout.addWidget(self.device_list)
        left_layout.addWidget(self.refresh_button)
        left_layout.addWidget(self.capture_button)
        left_layout.addWidget(self.crop_button)

        right_layout.addWidget(self.image_view)

        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.refresh_devices()



    def refresh_devices(self):
        result = os.popen("adb devices").read()
        devices = result.split("\n")[1:-2]
        self.device_list.clear()
        for device in devices:
            uid = device.split("\t")[0]
            self.device_list.addItem(uid)

    def change_device(self, item):
        self.current_device = item.text()

    def capture_screenshot(self):
        if self.current_device:
            os.system("adb -s {} shell screencap -p /sdcard/screenshot.png".format(self.current_device))
            os.system("adb -s {} pull /sdcard/screenshot.png".format(self.current_device))
            pixmap = QPixmap("screenshot.png")
            #pixmap = pixmap.scaled(1280, 720, Qt.AspectRatioMode.KeepAspectRatio)
            self.image_view.set_image(pixmap)
        else:
            print("No device selected")

    def crop_image(self):
        cropped_image = self.image_view.get_cropped_image()

        if cropped_image:
            file_dialog = QFileDialog()
            save_path, _ = file_dialog.getSaveFileName(self, "Save Image", "", "Images (*.png *.jpg *.bmp)")

            if save_path:
                cropped_image.save(save_path)

        else:
            print("No image to crop")
def main():
    app = QApplication(sys.argv)
    main_window = ScreenCaptureApp()
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()