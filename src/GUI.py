# This Code is made by Artificial Inteligence 
#Maintainer: @Thvrett77, GPT-6


import os
import sys
from pathlib import Path

from PyQt6.QtCore import QObject, QThread, Qt, pyqtSignal
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QWizard,
    QWizardPage,
)

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from adbcheck import ConnectADB, RemovePackageADB
FLUENT_DARK_STYLE = """
QWidget {
    background: #1c1c1c;
    color: #ffffff;
    font-family: "Segoe UI Variable", "Segoe UI", sans-serif;
    font-size: 10pt;
}
QWizard, QWizardPage, QMessageBox {
    background: #1c1c1c;
    color: #ffffff;
}
QWizardPage { padding: 12px; }
QLabel { background: transparent; color: #ffffff; }
QLineEdit {
    min-height: 34px;
    padding: 0 10px;
    color: #ffffff;
    background: #292929;
    border: 1px solid rgba(255, 255, 255, 17);
    border-radius: 5px;
    selection-background-color: #60cdff;
    selection-color: #002633;
}
QLineEdit:hover {
    background: #303030;
    border-color: rgba(255, 255, 255, 30);
}
QLineEdit:focus {
    border: 2px solid #60cdff;
}
QLineEdit:disabled, QPushButton:disabled {
    color: rgba(255, 255, 255, 100);
    background: #242424;
}
QPushButton {
    min-height: 34px;
    padding: 0 15px;
    color: #ffffff;
    background: #292929;
    border: 1px solid rgba(255, 255, 255, 17);
    border-radius: 5px;
}
QPushButton:hover {
    background: #373737;
    border-color: rgba(255, 255, 255, 30);
}
QPushButton:pressed { background: #242424; }
QPushButton:default {
    color: #002633;
    background: #60cdff;
    border-color: #60cdff;
}
QPushButton:default:hover { background: #78d5ff; }
QToolTip {
    color: #ffffff;
    background: #292929;
    border: 1px solid rgba(255, 255, 255, 30);
    padding: 5px;
}
"""


def apply_fluent_dark_palette(app):
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor("#1c1c1c"))
    palette.setColor(QPalette.ColorRole.WindowText, QColor("#ffffff"))
    palette.setColor(QPalette.ColorRole.Base, QColor("#202020"))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor("#252525"))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor("#292929"))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor("#ffffff"))
    palette.setColor(QPalette.ColorRole.Text, QColor("#ffffff"))
    palette.setColor(QPalette.ColorRole.Button, QColor("#292929"))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor("#ffffff"))
    palette.setColor(QPalette.ColorRole.Highlight, QColor("#60cdff"))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#002633"))
    app.setPalette(palette)
    app.setStyleSheet(FLUENT_DARK_STYLE)


class AdbCheckWorker(QObject):
    finished = pyqtSignal(bool, str)

    def run(self):
        try:
            self.finished.emit(ConnectADB(), "")
        except Exception as exc:
            self.finished.emit(False, str(exc))


class PackageRemovalWorker(QObject):
    progress = pyqtSignal(int, int, str)
    finished = pyqtSignal(str, str, str)

    def __init__(self, preset_path):
        super().__init__()
        self.preset_path = preset_path

    def run(self):
        try:
            message, warning = RemovePackageADB(self.preset_path, self.progress.emit)
            self.finished.emit(message, warning, "")
        except Exception as exc:
            self.finished.emit("", "", str(exc))


class DeviceCheckPage(QWizardPage):
    def __init__(self, wizard):
        super().__init__()
        self.wizard = wizard

    def validatePage(self):
        if self.wizard.device_connected:
            return True

        QMessageBox.warning(
            self,
            "ADB connection required",
            "Check the ADB connection successfully before continuing.",
        )
        return False


class ExperimentalWizardBase(QWizard):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Omni Debloat")
        self.resize(860, 560)
        self.setMinimumSize(760, 500)
        self.setWizardStyle(QWizard.WizardStyle.ModernStyle)
        self.setOptions(
            QWizard.WizardOption.NoBackButtonOnStartPage
            | QWizard.WizardOption.HaveNextButtonOnLastPage
            | QWizard.WizardOption.NoCancelButtonOnLastPage
        )
        self.setButtonText(QWizard.WizardButton.FinishButton, "Run")
        self.setButtonText(QWizard.WizardButton.NextButton, "Next")
        self.setButtonText(QWizard.WizardButton.CancelButton, "Close")

        self.device_connected = False
        self.preset_path = QLineEdit()
        self.preset_path.setPlaceholderText("Select a .xm preset file")
        self.check_button = None
        self.adb_thread = None
        self.adb_worker = None
        self.removal_thread = None
        self.removal_worker = None

        self.device_status = QLabel("Not checked yet")

        self.addPage(self.create_intro_page())
        self.addPage(self.create_device_page())
        self.addPage(self.create_preset_page())
        self.progress_page = self.create_progress_page()
        self.progress_page_id = self.addPage(self.progress_page)
        self.currentIdChanged.connect(self._update_status_panel)

    def create_intro_page(self):
        raise NotImplementedError

    def create_device_page(self):
        raise NotImplementedError

    def create_preset_page(self):
        raise NotImplementedError

    def create_progress_page(self):
        raise NotImplementedError

    def browse_preset(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Choose a preset file",
            os.getcwd(),
            "XM Files (*.xm);;All Files (*)",
        )
        if file_path:
            self.preset_path.setText(file_path)

    def check_adb_connection(self):
        if self.adb_thread is not None:
            return

        self.check_button.setEnabled(False)
        self.check_button.setText("Checking ADB connection...")
        self.device_status.setText("Checking ADB connection...")
        self.adb_thread = QThread(self)
        self.adb_worker = AdbCheckWorker()
        self.adb_worker.moveToThread(self.adb_thread)
        self.adb_thread.started.connect(self.adb_worker.run)
        self.adb_worker.finished.connect(self._adb_check_finished)
        self.adb_worker.finished.connect(self.adb_thread.quit)
        self.adb_worker.finished.connect(self.adb_worker.deleteLater)
        self.adb_thread.finished.connect(self._adb_thread_finished)
        self.adb_thread.finished.connect(self.adb_thread.deleteLater)
        self.adb_thread.start()

    def _adb_check_finished(self, connected, error_message):
        self.check_button.setEnabled(True)
        if error_message:
            self.device_connected = False
            self.check_button.setText("Retry ADB connection")
            self.device_status.setText("ADB check failed")
            QMessageBox.critical(self, "ADB Error", error_message)
        elif connected:
            self.device_connected = True
            self.check_button.setText("Check ADB connection")
            self.device_status.setText("Connected and ready")
            QMessageBox.information(self, "ADB Status", "Device connected and ready.")
        else:
            self.device_connected = False
            self.check_button.setText("Retry ADB connection")
            self.device_status.setText("No device detected")
            QMessageBox.warning(
                self, "ADB Status", "No connected Android device was detected."
            )

    def _adb_thread_finished(self):
        self.adb_worker = None
        self.adb_thread = None

    def _update_status_panel(self, *_):
        page = self.currentPage()
        if page is not None and page.title() == "Device connection" and self.device_connected:
            self.device_status.setText("Connected and ready")
        self._update_run_button_text()

    def _update_run_button_text(self, *_):
        page = self.currentPage()
        is_removal_run = page is not None and page.title() == "Remove packages from preset"
        label = "Run" if is_removal_run else "Next"
        self.setButtonText(QWizard.WizardButton.NextButton, label)


class ExperimentalPresetPage(QWizardPage):
    def __init__(self, wizard):
        super().__init__()
        self.wizard = wizard

    def validatePage(self):
        preset_path = self.wizard.preset_path.text().strip()
        if preset_path and os.path.isfile(preset_path) and Path(preset_path).suffix.lower() == ".xm":
            return True

        QMessageBox.warning(
            self,
            "Preset required",
            "Choose a valid .xm preset file for package removal.",
        )
        return False

    def nextId(self):
        return self.wizard.progress_page_id


class PackageRemovalPage(QWizardPage):
    def __init__(self, wizard):
        super().__init__()
        self.wizard = wizard
        self.started = False

    def initializePage(self):
        if self.started:
            return
        self.started = True
        self.wizard.setButtonText(QWizard.WizardButton.FinishButton, "Run")
        self.wizard.button(QWizard.WizardButton.FinishButton).setEnabled(False)
        self.status_label.setText("Preparing package removal...")
        self.result_label.clear()

        self.wizard.removal_thread = QThread(self.wizard)
        self.wizard.removal_worker = PackageRemovalWorker(
            self.wizard.preset_path.text().strip()
        )
        self.wizard.removal_worker.moveToThread(self.wizard.removal_thread)
        self.wizard.removal_thread.started.connect(self.wizard.removal_worker.run)
        self.wizard.removal_worker.progress.connect(self._update_progress)
        self.wizard.removal_worker.finished.connect(self._removal_finished)
        self.wizard.removal_worker.finished.connect(self.wizard.removal_thread.quit)
        self.wizard.removal_worker.finished.connect(self.wizard.removal_worker.deleteLater)
        self.wizard.removal_thread.finished.connect(self.wizard._removal_thread_finished)
        self.wizard.removal_thread.finished.connect(self.wizard.removal_thread.deleteLater)
        self.wizard.removal_thread.start()

    def _update_progress(self, current, total, package):
        self.progress_bar.setRange(0, total)
        self.progress_bar.setValue(current)
        self.status_label.setText(f"Removing package {current} of {total}: {package}")

    def _removal_finished(self, message, warning, error_message):
        if error_message:
            self.status_label.setText("Package removal failed")
            self.result_label.setText(error_message)
            self.result_label.setStyleSheet("color: #ff99a4;")
        else:
            self.progress_bar.setRange(0, 1)
            self.progress_bar.setValue(1)
            self.status_label.setText("Package removal complete")
            self.result_label.setText(f"{message}\n{warning}")
            self.result_label.setStyleSheet("color: #6ccb5f;")
        self.wizard.setButtonText(QWizard.WizardButton.FinishButton, "Done")
        self.wizard.button(QWizard.WizardButton.FinishButton).setEnabled(True)


class ExperimentalOmniDebloatWizard(ExperimentalWizardBase):
    def _set_theme(self, widget):
        app = QApplication.instance()
        if app is not None:
            apply_fluent_dark_palette(app)
        widget.setStyleSheet(FLUENT_DARK_STYLE)

    def create_intro_page(self):
        page = QWizardPage()
        page.setTitle("Welcome")
        page.setSubTitle("A focused workspace for Android device maintenance.")
        self._set_theme(page)

        layout = QVBoxLayout(page)
        layout.setContentsMargins(12, 12, 12, 24)
        layout.setSpacing(18)

        eyebrow = QLabel("OMNI DEBLOAT  /  ANDROID TOOLS")
        eyebrow.setStyleSheet("color: #60cdff; font-size: 9pt; font-weight: 700;")
        layout.addWidget(eyebrow)

        title = QLabel("Your device,\nyour control.")
        title.setStyleSheet("font-size: 28pt; font-weight: 600; color: #ffffff;")
        layout.addWidget(title)

        description = QLabel(
            "Connect over ADB, select a preset, and remove its listed packages."
        )
        description.setWordWrap(True)
        description.setStyleSheet("font-size: 11pt; color: rgba(255, 255, 255, 199);")
        layout.addWidget(description)

        overview = QLabel(
            "01   Verify your device\n\n"
            "02   Select an XM preset\n\n"
            "03   Review and run the command"
        )
        overview.setStyleSheet(
            "padding: 18px; background: #242424; color: #ffffff; "
            "border: 1px solid rgba(255, 255, 255, 20); "
            "border-radius: 6px; line-height: 1.5;"
        )
        layout.addWidget(overview)
        layout.addStretch(1)
        return page

    def create_device_page(self):
        page = DeviceCheckPage(self)
        page.setTitle("Device connection")
        page.setSubTitle("Make sure Android Debug Bridge can see your device.")
        self._set_theme(page)

        layout = QVBoxLayout(page)
        layout.setContentsMargins(12, 12, 12, 24)
        layout.setSpacing(14)

        section_title = QLabel("ADB connection")
        section_title.setStyleSheet("font-size: 16pt; font-weight: 600;")
        layout.addWidget(section_title)

        self.device_status.setText("Not checked yet")
        self.device_status.setStyleSheet(
            "padding: 14px; background: #242424; "
            "border: 1px solid rgba(255, 255, 255, 20); "
            "border-radius: 6px; color: rgba(255, 255, 255, 199);"
        )
        layout.addWidget(self.device_status)

        self.check_button = QPushButton("Check ADB connection")
        self.check_button.clicked.connect(self.check_adb_connection)
        layout.addWidget(self.check_button, alignment=Qt.AlignmentFlag.AlignLeft)

        detail = QLabel(
            "Unlock your phone and accept the USB debugging prompt if Android asks."
        )
        detail.setWordWrap(True)
        detail.setStyleSheet("color: rgba(255, 255, 255, 199);")
        layout.addWidget(detail)
        layout.addStretch(1)
        return page

    def create_preset_page(self):
        page = ExperimentalPresetPage(self)
        page.setTitle("Remove packages from preset")
        page.setSubTitle("Choose an XM preset file to remove its listed packages.")
        self._set_theme(page)

        layout = QVBoxLayout(page)
        layout.setContentsMargins(12, 12, 12, 24)
        layout.setSpacing(12)

        action_label = QLabel("Operation")
        action_label.setStyleSheet("font-weight: 600;")
        layout.addWidget(action_label)
        operation_name = QLabel("Remove packages from preset")
        operation_name.setStyleSheet("font-size: 12pt; font-weight: 600;")
        layout.addWidget(operation_name)
        self.preset_row = self._file_row(self.preset_path, "Browse preset", self.browse_preset)
        self.preset_label = QLabel("XM preset")
        self.preset_label.setStyleSheet("font-weight: 600;")

        layout.addWidget(self.preset_label)
        layout.addWidget(self.preset_row)
        layout.addStretch(1)

        return page

    def create_progress_page(self):
        page = PackageRemovalPage(self)
        page.setTitle("Removing packages")
        page.setSubTitle("Package removal progress and results.")
        self._set_theme(page)

        layout = QVBoxLayout(page)
        layout.setContentsMargins(12, 12, 12, 24)
        layout.setSpacing(14)

        page.status_label = QLabel("Waiting to start")
        page.status_label.setWordWrap(True)
        layout.addWidget(page.status_label)

        page.progress_bar = QProgressBar()
        page.progress_bar.setRange(0, 0)
        layout.addWidget(page.progress_bar)

        page.result_label = QLabel()
        page.result_label.setWordWrap(True)
        layout.addWidget(page.result_label)
        layout.addStretch(1)
        return page

    def _file_row(self, field, button_text, callback):
        row = QWidget()
        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(0, 0, 0, 0)
        row_layout.setSpacing(8)
        browse_button = QPushButton(button_text)
        browse_button.clicked.connect(callback)
        row_layout.addWidget(field, 1)
        row_layout.addWidget(browse_button)
        return row

    def _adb_check_finished(self, connected, error_message):
        super()._adb_check_finished(connected, error_message)
        if connected and not error_message:
            self.device_status.setStyleSheet(
                "padding: 14px; background: #203428; border: 1px solid #3a6847; "
                "border-radius: 6px; color: #6ccb5f;"
            )
        elif not connected or error_message:
            self.device_status.setStyleSheet(
                "padding: 14px; background: #3a2426; border: 1px solid #75434a; "
                "border-radius: 6px; color: #ff99a4;"
            )

    def _removal_thread_finished(self):
        self.removal_worker = None
        self.removal_thread = None


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setApplicationName("Omni Debloat")
    apply_fluent_dark_palette(app)
    window = ExperimentalOmniDebloatWizard()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()