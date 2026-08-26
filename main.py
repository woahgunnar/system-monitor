import sys
import psutil
from pathlib import Path
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import (QApplication, QWidget, QLabel,
                               QVBoxLayout, QProgressBar)

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("System Monitor")
window.resize(600, 400)
window.setStyleSheet("""
    QWidget {
        background-color: #181a1f;
        color: #ffffff;
        font-family: "Segoe UI";
        font-size: 14px;
    }

    QProgressBar {
        background-color: #2a2d35;
        border: none;
        border-color: ;
        border-width: ;
        border-radius: 3px;
        height: 18px;
        text-align: center;
    }

    QProgressBar::chunk {
        background-color: #cc4385;
        border-radius: 3px;
    }
""")

# -- storage detection --
storage_path = Path.home()
storage_name = storage_path.anchor # readable name

# -- widgets --
cpu_label = QLabel("CPU Usage:")
cpu_progress = QProgressBar()
ram_label = QLabel("RAM Usage:")
ram_progress = QProgressBar()
disk_label = QLabel(f"Storage: ({storage_name})")
disk_progress = QProgressBar()

# -- layouts --
layout = QVBoxLayout()
layout.setContentsMargins(50, 25, 50, 25)
layout.setSpacing(25)

cpu_layout = QVBoxLayout()
cpu_layout.setSpacing(4)
cpu_layout.addWidget(cpu_label)
cpu_layout.addWidget(cpu_progress)

memory_layout = QVBoxLayout()
memory_layout.setSpacing(4)
memory_layout.addWidget(ram_label)
memory_layout.addWidget(ram_progress)

disk_layout = QVBoxLayout()
disk_layout.setSpacing(4)
disk_layout.addWidget(disk_label)
disk_layout.addWidget(disk_progress)

layout.addLayout(cpu_layout)
layout.addLayout(memory_layout)
layout.addLayout(disk_layout)
layout.addStretch()

window.setLayout(layout)


# function to monitor the user's system and update the metrics
def monitor():
    # -- cpu --
    cpu_usage = psutil.cpu_percent(interval=None)
    cpu_progress.setValue(int(cpu_usage))

    # -- memory --
    ram_usage = psutil.virtual_memory()
    ram_used = ram_usage.used/1024 ** 3
    ram_total = ram_usage.total / 1024 ** 3
    ram_progress.setValue(int(ram_usage.percent))
    ram_progress.setFormat(f"{ram_used:.2f} GB "
                           f"/ {ram_total:.2f} GB")

    # -- disk --
    disk_usage = psutil.disk_usage(str(storage_path))
    disk_used = disk_usage.used/1024 ** 3
    disk_total = disk_usage.total / 1024 ** 3
    disk_progress.setValue(int(disk_usage.percent))
    disk_progress.setFormat(f"{disk_used:.2f} GB / {disk_total:.2f} GB")


monitor()

# -- timer --
timer = QTimer()
timer.timeout.connect(monitor)
timer.start(1000)

window.show()
app.exec()