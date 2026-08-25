import sys
import psutil
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import QTimer

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("System Monitor")
window.resize(400, 200)

cpu_label = QLabel()
ram_label = QLabel()
disk_label = QLabel()

layout = QVBoxLayout()

layout.addWidget(cpu_label)
layout.addWidget(ram_label)
layout.addWidget(disk_label)

window.setLayout(layout)


# function to monitor the user's system and update the labels
def monitor():
    cpu_usage = psutil.cpu_percent(interval=None)
    cpu_label.setText(f"CPU Usage: {cpu_usage}%")

    ram_usage = psutil.virtual_memory().percent
    ram_label.setText(f"Memory Usage: {ram_usage}%")

    disk_usage = psutil.disk_usage('/').percent
    disk_label.setText(f"Disk Usage: {disk_usage}%")


monitor()

timer = QTimer()
timer.timeout.connect(monitor)
timer.start(1000)

window.show()
app.exec()