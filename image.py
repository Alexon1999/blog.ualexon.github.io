import os
import pyperclip
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, QLabel, QPushButton, QFileDialog, QMessageBox

class BlogApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowTitle('Blog App')
        self.setGeometry(100, 100, 800, 600)

        # Create widgets
        self.upload_button = QPushButton('Upload Images')
        self.upload_button.clicked.connect(self.upload_images)

        self.image_list = QListWidget()
        self.image_list.setIconSize(QPixmap(100, 100).size())

        # Add widgets to layout
        layout = QHBoxLayout()
        layout.addWidget(self.upload_button)
        layout.addWidget(self.image_list)

        # Set central widget
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def upload_images(self):
        file_names, _ = QFileDialog.getOpenFileNames(self, "Select images", "", "Image Files (*.png *.jpg *.jpeg *.gif)")

        for file_name in file_names:
            # Add image to list
            item = QListWidgetItem(QIcon(file_name), os.path.basename(file_name))
            self.image_list.addItem(item)

            # Show image preview on hover
            label = QLabel()
            pixmap = QPixmap(file_name)
            label.setPixmap(pixmap.scaled(100, 100, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio))
            self.image_list.setItemWidget(item, label)

    def get_selected_image_path(self):
        selected_item = self.image_list.currentItem()
        if selected_item:
            image_path = os.path.abspath(selected_item.text())
            pyperclip.copy(image_path)
            QMessageBox.information(self, 'Image path copied', f'The path of the selected image has been copied to the clipboard:\n{image_path}')
        else:
            QMessageBox.warning(self, 'No image selected', 'Please select an image from the list.')

if __name__ == '__main__':
    app = QApplication([])
    window = BlogApp()
    window.show()
    app.exec()
