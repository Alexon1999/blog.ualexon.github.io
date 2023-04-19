import os
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QFont
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
    QMessageBox
)
import subprocess
import re
import unicodedata

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

class BlogApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Blog App")
        self.setGeometry(100, 100, 800, 600)
        
        self.image_path = None 
        # Set up image preview label
        self.image_preview = QLabel(self)
        self.image_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_preview.setFixedSize(300, 200)
        self.image_preview.setStyleSheet(
            "QLabel { border-style: solid; border-width: 2px; border-color: black; }"
        )

        # Set up main label
        self.main_label = QLabel("Create a new blog post", self)
        self.main_label.setFont(QFont("Arial", 18))

        # Set up upload button
        self.upload_button = QPushButton("Upload Image", self)
        self.upload_button.clicked.connect(self.upload_image)

        # Set up article input
        self.article_name_label = QLabel("article name:", self)
        self.article_name_input = QLineEdit(self)

        # Set up markdown input
        self.markdown_description_label = QLabel("Markdown:", self)
        self.markdown_description_input = QTextEdit(self)

        # Set up submit button
        self.submit_button = QPushButton("Submit", self)
        self.submit_button.clicked.connect(self.submit_post)

        # Set up main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.main_label)
        self.main_layout.addWidget(self.image_preview)
        self.main_layout.addWidget(self.upload_button)

        # Set up form layout
        self.form_layout = QVBoxLayout()
        self.form_layout.addWidget(self.article_name_label)
        self.form_layout.addWidget(self.article_name_input)
        self.form_layout.addWidget(self.markdown_description_label)
        self.form_layout.addWidget(self.markdown_description_input)

        # Set up horizontal layout for form and submit button
        self.h_layout = QHBoxLayout()
        self.h_layout.addLayout(self.form_layout)
        self.h_layout.addWidget(self.submit_button)

        # Add horizontal layout to main layout
        self.main_layout.addLayout(self.h_layout)

    def upload_image(self):
        # options = QFileDialog.Options()
        # options |= QFileDialog.Option.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Select Image",
            "",
            "Image Files (*.png *.jpg *.jpeg *.gif)",
            # options=options,
        )
        print(file_name)
        if file_name:
            pixmap = QPixmap(file_name)
            self.image_preview.setPixmap(pixmap.scaled(300, 200, Qt.AspectRatioMode.KeepAspectRatio))
            
            # Save image to assets folder
            image_folder = "assets/images"
            if not os.path.exists(image_folder):
                os.makedirs(image_folder)

            _, extension = os.path.splitext(file_name)
            # os.path.basename() function returns the last component of the path
            self.image_name = os.path.basename(file_name)
            self.image_path = os.path.join(image_folder, self.image_name)
            pixmap.save(self.image_path)

        
    def submit_post(self):
        # Récupération des informations
        markdown_description = self.markdown_description_input.toPlainText()
        image_path = self.image_path
        article_name = self.article_name_input.text()

        # Vérification des informations
        if not markdown_description or not image_path or not article_name:
            QMessageBox.warning(self, "Attention", "Veuillez remplir tous les champs.")
            return

        # Récupération du template markdown
        with open("assets/template.md", "r", encoding="utf-8") as f:
            template = f.read()

        # Remplacement des placeholders par les informations
        markdown = template.replace("[TITLE]", article_name)
        markdown = markdown.replace("[IMAGE]", image_path)
        markdown = markdown.replace("[DESCRIPTION]", markdown_description)

        # Enregistrement du markdown dans le dossier "articles"
        with open(f"{title_to_url(article_name)}.md", "w", encoding="utf-8") as f:
            f.write(markdown)

        # Ouverture du dossier "articles"
        subprocess.run(["open", "articles"])

        # Reset du formulaire
        self.article_name_input.clear()
        self.markdown_description_input.clear()
        self.image_preview.setPixmap(QPixmap())
        self.image_path = None
        self.image_name = None

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
