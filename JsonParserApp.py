from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QTreeWidget, QTreeWidgetItem
import sys
from JsonParser import JSONParser

class JSONParserApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("JSON Parser")

        # UI Elements
        layout = QVBoxLayout()
        self.json_input = QTextEdit()
        self.parse_button = QPushButton("Parse JSON")
        self.tree_view = QTreeWidget()
        self.tree_view.setHeaderLabels(["Key", "Value"])

        # Add elements to layout
        layout.addWidget(self.json_input)
        layout.addWidget(self.parse_button)
        layout.addWidget(self.tree_view)
        self.setLayout(layout)

        # Button click event
        self.parse_button.clicked.connect(self.parse_json)

    def parse_json(self):
        json_text = self.json_input.toPlainText()
        try:
            parser = JSONParser(json_text)
            json_data = parser.parse()
            self.tree_view.clear()
            self.populate_tree(json_data, self.tree_view.invisibleRootItem())
        except Exception as e:
            self.tree_view.clear()
            self.tree_view.setHeaderLabel(f"Error: {str(e)}")

    def populate_tree(self, data, parent):
        if isinstance(data, dict):
            for key, value in data.items():
                item = QTreeWidgetItem([key, str(value) if not isinstance(value, (dict, list)) else ""])
                parent.addChild(item)
                self.populate_tree(value, item)
        elif isinstance(data, list):
            for index, value in enumerate(data):
                item = QTreeWidgetItem([f"[{index}]", str(value) if not isinstance(value, (dict, list)) else ""])
                parent.addChild(item)
                self.populate_tree(value, item)

# Run UI
app = QApplication(sys.argv)
window = JSONParserApp()
window.show()
sys.exit(app.exec())
