import sys
from pathlib import Path

import psutil
import cpuinfo
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout,
    QProgressBar,
)

BYTES_PER_GB = 1024 ** 3


# desktop window class
# inherits from QWidget, meaning that this class is the app window
class SystemMonitorWindow(QWidget):
    def __init__(self):
        super().__init__()

        # -- window config --
        self.setWindowTitle("System Monitor")
        self.resize(600, 400)
        self.setStyleSheet("""
            QWidget {
                background-color: #181a1f;
                color: #ffffff;
                font-family: "Segoe UI";
                font-size: 14px;
            }

            QProgressBar {
                background-color: #2a2d35;
                border: none;
                border-radius: 3px;
                height: 18px;
                text-align: center;
            }

            QProgressBar::chunk {
                background-color: #cc4385;
                border-radius: 3px;
            }
        """)

        # -- cpu detection --
        cpu_name = cpuinfo.get_cpu_info()['brand_raw'] or "Unknown"

        # -- storage detection --
        self.storage_path = Path.home()
        storage_name = self.storage_path.anchor  # readable name

        # -- widgets --
        cpu_label = QLabel(f"CPU ({cpu_name}) Usage:")
        self.cpu_progress = QProgressBar()

        ram_label = QLabel("RAM Usage:")
        self.ram_progress = QProgressBar()

        disk_label = QLabel(f"Storage ({storage_name}):")
        self.disk_progress = QProgressBar()

        # -- layouts --
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(50, 25, 50, 25)
        main_layout.setSpacing(25)

        cpu_layout = QVBoxLayout()
        cpu_layout.setSpacing(4)
        cpu_layout.addWidget(cpu_label)
        cpu_layout.addWidget(self.cpu_progress)

        memory_layout = QVBoxLayout()
        memory_layout.setSpacing(4)
        memory_layout.addWidget(ram_label)
        memory_layout.addWidget(self.ram_progress)

        disk_layout = QVBoxLayout()
        disk_layout.setSpacing(4)
        disk_layout.addWidget(disk_label)
        disk_layout.addWidget(self.disk_progress)

        main_layout.addLayout(cpu_layout)
        main_layout.addLayout(memory_layout)
        main_layout.addLayout(disk_layout)
        main_layout.addStretch()

        self.setLayout(main_layout)

        # -- timer --
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.monitor)
        self.timer.start(1000)

        self.monitor()

    # function to monitor the user's system and update the metrics
    def monitor(self):
        # -- cpu --
        cpu_usage = psutil.cpu_percent(interval=None)
        self.cpu_progress.setValue(int(cpu_usage))

        # -- memory --
        ram_usage = psutil.virtual_memory()
        ram_used = ram_usage.used / BYTES_PER_GB
        ram_total = ram_usage.total / BYTES_PER_GB
        self.ram_progress.setValue(int(ram_usage.percent))
        self.ram_progress.setFormat(f"{ram_used:.2f} GB "
                                    f"/ {ram_total:.2f} GB")

        # -- disk --
        disk_usage = psutil.disk_usage(str(self.storage_path))
        disk_used = disk_usage.used / BYTES_PER_GB
        disk_total = disk_usage.total / BYTES_PER_GB
        self.disk_progress.setValue(int(disk_usage.percent))
        self.disk_progress.setFormat(f"{disk_used:.2f} GB / {disk_total:.2f} GB")


def main():
    app = QApplication(sys.argv)

    window = SystemMonitorWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
