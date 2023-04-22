import os
import sys
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QFont, QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QFileDialog,
    QTextEdit,
    QLineEdit,
    QMessageBox,
    QListWidget,
    QListWidgetItem,
    QListView,
    QListWidget,
    QListWidgetItem,
    QFileDialog,
    QListView,
    QAbstractItemView,
    QTabWidget,
    QPlainTextEdit
)
import re
import unicodedata
import markdown

def title_to_url(title):
    # unicodedata.normalize() is usedNormalize the title string by converting accented characters to their ASCII equivalent
    title = unicodedata.normalize('NFKD', title).encode('ASCII', 'ignore').decode('utf-8')
    # The regex pattern matches any non-alphanumeric character (including whitespace) and replaces it with an empty string.
    url = re.sub(r"[^a-zA-Z0-9\s-]", "", title).strip().lower()
    # Consecutive whitespace characters (i.e., more than two spaces) are replaced with a single space.
    url = re.sub(r"\s{2,}", " ", url).strip().lower()
    # Replace remaining whitespace with hyphens
    url = url.replace(" ", "-").lower()
    return url


class ImageListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(800, 110)
        self.setViewMode(QListView.ViewMode.IconMode)
        self.setIconSize(QSize(150, 110))
        self.setResizeMode(QListView.ResizeMode.Adjust)
        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.itemClicked.connect(self.copy_path_to_clipboard)

    def add_image(self, image_path):
        item = QListWidgetItem()
        pixmap = QPixmap(image_path).scaled(
            150,
            110,
            aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio
            )
        item.setIcon(QIcon(pixmap))
        item.setData(Qt.ItemDataRole.UserRole, image_path)
        item.setToolTip(image_path)
        self.addItem(item)
    
    def clear_all_images(self):
        self.clear()
    
    def copy_path_to_clipboard(self, item):
        image_path = item.data(Qt.ItemDataRole.UserRole)
        clipboard = QApplication.clipboard()
        clipboard.setText(image_path)
        QMessageBox.information(self, "Image Path Copied", f"The path '{image_path}' has been copied to the clipboard.")


class BlogApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Blog App")
        self.setGeometry(100, 100, 800, 600)

        # Set up main label
        self.main_label = QLabel("Create a new blog post", self)
        self.main_label.setFont(QFont("Arial", 18))

        # Set up upload button
        self.upload_button = QPushButton("Upload Image", self)
        self.upload_button.clicked.connect(self.upload_image)

        # images
        self.image_paths = []

        # uploaded images List
        self.image_list_widget = ImageListWidget(self)

        # Set up article input
        self.article_name_label = QLabel("article name:", self)
        self.article_name_input = QLineEdit(self)

        # Header Image URL input
        self.header_img_url_label = QLabel("header image url:", self)
        self.header_img_url_input = QLineEdit(self)

        # create tab widget (Markdown/Preview)
        self.tab_widget = QTabWidget()

        # create markdown widget
        markdown_widget = QWidget()
        markdown_layout = QVBoxLayout()
        markdown_widget.setLayout(markdown_layout)
        self.markdown_editor = QPlainTextEdit()
        markdown_layout.addWidget(self.markdown_editor)
        self.tab_widget.addTab(markdown_widget, "Markdown")

        # create preview widget
        preview_widget = QWidget()
        preview_layout = QVBoxLayout()
        preview_widget.setLayout(preview_layout)
        self.preview_widget = QTextEdit()
        self.preview_widget.setReadOnly(True)
        preview_layout.addWidget(self.preview_widget)
        self.tab_widget.addTab(preview_widget, "Preview")

        # set up signals and slots
        self.markdown_editor.textChanged.connect(self.update_preview)

        # Set up submit button
        self.submit_button = QPushButton("Submit", self)
        self.submit_button.clicked.connect(self.submit_post)

        # Set up main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.main_label)
        self.main_layout.addWidget(self.upload_button)
        self.main_layout.addWidget(self.image_list_widget)

        # Set up form layout
        self.form_layout = QVBoxLayout()
        self.form_layout.addWidget(self.article_name_label)
        self.form_layout.addWidget(self.article_name_input)
        self.form_layout.addWidget(self.header_img_url_label)
        self.form_layout.addWidget(self.header_img_url_input)
        self.form_layout.addWidget(self.tab_widget)

        # Set up horizontal layout for form and submit button
        self.h_layout = QHBoxLayout()
        self.h_layout.addLayout(self.form_layout)
        self.h_layout.addWidget(self.submit_button)

        # Add horizontal layout to main layout
        self.main_layout.addLayout(self.h_layout)

    def upload_image(self):
        # options = QFileDialog.Options()
        # options |= QFileDialog.Option.DontUseNativeDialog
        file_names, _ = QFileDialog.getOpenFileNames(
            self,
            "Select images",
            "",
            "Image Files (*.png *.jpg *.jpeg *.gif)",
            # options=options
            )

        for file_name in file_names:
            if file_name:
                # Save image to assets folder
                image_folder = "assets/images"
                if not os.path.exists(image_folder):
                    os.makedirs(image_folder)

                _, extension = os.path.splitext(file_name)

                # os.path.basename() function returns the last component of the path
                image_name = os.path.basename(file_name)
                image_path = os.path.join(image_folder, image_name)

                pixmap = QPixmap(file_name)
                # pixmap = pixmap.scaledToHeight(700)

                # save image into assets/images
                pixmap.save(image_path)

                # add image to ImageListWidget
                self.image_list_widget.add_image(image_path)
                self.image_paths.append(image_path)


    def update_preview(self):
        markdown_text = self.markdown_editor.toPlainText()
        html_text = markdown.markdown(markdown_text)
        self.preview_widget.setHtml(html_text)

    def submit_post(self):
        # gather informations
        description = self.markdown_editor.toPlainText()
        article_name = self.article_name_input.text()
        header_img_url = self.header_img_url_input.text()

        # verify informations
        if not header_img_url or not description or not header_img_url or not article_name:
            QMessageBox.warning(self, "Attention", "Veuillez remplir tous les champs.")
            return

        # get the template markdown
        with open("assets/template.md", "r", encoding="utf-8") as f:
            template = f.read()

        # replace all the   placeholders by our informations
        markdown = template.replace("[TITLE]", article_name)
        markdown = markdown.replace("[HEADER_IMAGE]", header_img_url)
        markdown = markdown.replace("[DESCRIPTION]", description)

        # save the markdown file
        with open(f"{title_to_url(article_name)}.md", "w", encoding="utf-8") as f:
            f.write(markdown)

        # Reset du formulaire
        self.article_name_input.clear()
        self.header_img_url_input.clear()
        self.markdown_editor.clear()
        self.image_paths = []
        self.image_list_widget.clear_all_images()

        QMessageBox.information(self, "Succès", "Article enregistré avec succès !")

    def copy_to_clipboard(self, path):
        clipboard = QApplication.clipboard()
        clipboard.setText(path)



def main():
    app = QApplication(sys.argv)
    window = BlogApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()