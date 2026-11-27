import os
import sys
from pathlib import Path

from PyQt6.QtCore import QObject, QThread, Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWizard,
    QWizardPage,
)

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from adbcheck import ConnectADB, RemovePackageADB
from functions import force_uninstall, install, makecfg, uninstall


class AdbCheckWorker(QObject):
    finished = pyqtSignal(bool, str)

    def run(self):
        try:
            self.finished.emit(ConnectADB(), "")
        except Exception as exc:
            self.finished.emit(False, str(exc))


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


class PresetSelectionPage(QWizardPage):
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
            "Please select a valid .xm preset file before continuing.",
        )
        return False


class OmniDebloatWizard(QWizard):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Omni Debloat Wizard")
        self.resize(860, 560)
        self.setMinimumSize(760, 500)
        self.setWizardStyle(QWizard.WizardStyle.ModernStyle)
        self.setOptions(
            QWizard.WizardOption.NoBackButtonOnStartPage
            | QWizard.WizardOption.HaveNextButtonOnLastPage
            | QWizard.WizardOption.NoCancelButtonOnLastPage
        )
        self.setButtonText(QWizard.WizardButton.FinishButton, "Run")
        self.setButtonText(QWizard.WizardButton.CancelButton, "Close")

        self.device_connected = False

        self.preset_path = QLineEdit()
        self.preset_path.setPlaceholderText("Select a .xm preset file")

        self.apk_path = QLineEdit()
        self.apk_path.setPlaceholderText("Select an APK file")

        self.package_name = QLineEdit()
        self.package_name.setPlaceholderText("com.example.package")

        self.check_button = None
        self.summary_details = None
        self.adb_thread = None
        self.adb_worker = None

        self.action_combo = QComboBox()
        self.action_combo.addItems(
            [
                "Remove packages from preset",
                "Install APK",
                "Uninstall package",
                "Force uninstall package",
                "Create preset config",
            ]
        )

        self.device_status = QLabel("Not checked yet")
        self.device_status.setStyleSheet(
            "padding: 8px; border: 1px solid #2a3d5f; background: #132131; border-radius: 8px; color: #dfeaff;"
        )

        self.addPage(self.create_intro_page())
        self.addPage(self.create_device_page())
        self.addPage(self.create_preset_page())

        self.currentIdChanged.connect(self._update_status_panel)
        self.accepted.connect(self.execute_selected_action)

    def _set_theme(self, widget):
        widget.setStyleSheet(
            """
            QWidget {
                background: #121417;
                color: #edf4ff;
                font-family: "Segoe UI", sans-serif;
            }
            QLabel {
                color: #edf4ff;
            }
            QLineEdit, QComboBox {
                background: #1b2129;
                color: #edf4ff;
                border: 1px solid #2d3640;
                border-radius: 10px;
                padding: 8px 10px;
                min-height: 32px;
            }
            QLineEdit:focus, QComboBox:focus {
                border-color: #5a8cff;
            }
            QPushButton {
                background: #1f2732;
                border: 1px solid #2d3640;
                border-radius: 10px;
                padding: 9px 14px;
                color: #edf4ff;
                min-height: 32px;
            }
            QPushButton:hover {
                background: #2a313b;
                border-color: #5a8cff;
            }
            QPushButton:pressed {
                background: #1c7ae6;
            }
            QWizard {
                background: #121417;
            }
            QWizardPage {
                background: #121417;
            }
            """
        )

    def create_intro_page(self):
        page = QWizardPage()
        page.setTitle("Welcome")
        page.setSubTitle("Set up your Android debloat workflow in a few steps.")
        self._set_theme(page)

        layout = QVBoxLayout(page)
        layout.setSpacing(16)

        title = QLabel("Omni Android Debloater")
        title.setStyleSheet("font-size: 26px; font-weight: 700; color: #dfe9ff;")
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(title)

        description = QLabel(
            "This wizard will help you check ADB connectivity, select a preset, and run the debloat actions you need."
        )
        description.setWordWrap(True)
        layout.addWidget(description)

        steps = QLabel(
            "1. Check your device\n"
            "2. Choose a preset or package action\n"
            "3. Run the debloat operation"
        )
        steps.setStyleSheet("padding: 12px; background: #171c22; border: 1px solid #2a313b; border-radius: 10px;")
        layout.addWidget(steps)

        spacer = QLabel()
        spacer.setMinimumHeight(150)
        layout.addWidget(spacer)
        return page

    def create_device_page(self):
        page = DeviceCheckPage(self)
        page.setTitle("Device check")
        page.setSubTitle("Verify your Android device is connected through ADB.")
        self._set_theme(page)

        layout = QVBoxLayout(page)
        layout.setSpacing(12)

        self.device_status.setText("Not checked yet")
        layout.addWidget(self.device_status)

        self.check_button = QPushButton("Check ADB Connection")
        self.check_button.clicked.connect(self.check_adb_connection)
        layout.addWidget(self.check_button)

        info = QLabel(
            "If the device is connected correctly, the wizard will allow you to continue to preset and package actions."
        )
        info.setWordWrap(True)
        layout.addWidget(info)
        return page

    def create_preset_page(self):
        page = PresetSelectionPage(self)
        page.setTitle("Preset selection")
        page.setSubTitle("Choose the .xm preset you want to use.")
        self._set_theme(page)

        layout = QVBoxLayout(page)
        layout.setSpacing(12)

        preset_row = QHBoxLayout()
        preset_row.addWidget(self.preset_path)
        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.browse_preset)
        preset_row.addWidget(browse_button)
        layout.addLayout(preset_row)
        return page

    def _update_action_fields(self):
        selected = self.action_combo.currentText()
        if selected == "Remove packages from preset":
            self.apk_path.setVisible(False)
            self.package_name.setVisible(False)
        elif selected == "Install APK":
            self.apk_path.setVisible(True)
            self.package_name.setVisible(False)
        elif selected in {"Uninstall package", "Force uninstall package"}:
            self.apk_path.setVisible(False)
            self.package_name.setVisible(True)
        elif selected == "Create preset config":
            self.apk_path.setVisible(False)
            self.package_name.setVisible(False)

    def _update_status_panel(self):
        page = self.currentPage()
        if page is not None:
            title = page.title()
            if title == "Device check" and self.device_connected:
                self.device_status.setText("Connected")
                self.device_status.setStyleSheet(
                    "padding: 8px; border: 1px solid #2d6b4a; background: #122d22; border-radius: 8px; color: #bcf7d4;"
                )
    def browse_preset(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Choose a preset file",
            os.getcwd(),
            "XM Files (*.xm);;All Files (*)",
        )
        if file_path:
            self.preset_path.setText(file_path)

    def browse_apk(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Choose an APK file",
            os.getcwd(),
            "APK Files (*.apk);;All Files (*)",
        )
        if file_path:
            self.apk_path.setText(file_path)

    def check_adb_connection(self):
        if self.adb_thread is not None:
            return

        self.check_button.setEnabled(False)
        self.check_button.setText("Checking ADB Connection...")
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
            self.check_button.setText("Retry ADB Connection")
            self.device_status.setText("ADB check failed")
            self.device_status.setStyleSheet(
                "padding: 8px; border: 1px solid #6b3c3c; background: #2b1d1d; border-radius: 8px; color: #ffc3c3;"
            )
            QMessageBox.critical(self, "ADB Error", error_message)
        elif connected:
            self.device_connected = True
            self.check_button.setText("Check ADB Connection")
            self.device_status.setText("Connected and ready")
            self.device_status.setStyleSheet(
                "padding: 8px; border: 1px solid #2d6b4a; background: #122d22; border-radius: 8px; color: #bcf7d4;"
            )
            QMessageBox.information(self, "ADB Status", "Device connected and ready.")
        else:
            self.device_connected = False
            self.check_button.setText("Retry ADB Connection")
            self.device_status.setText("No device detected")
            self.device_status.setStyleSheet(
                "padding: 8px; border: 1px solid #6b3c3c; background: #2b1d1d; border-radius: 8px; color: #ffc3c3;"
            )
            QMessageBox.warning(self, "ADB Status", "No connected Android device was detected.")

    def _adb_thread_finished(self):
        self.adb_worker = None
        self.adb_thread = None

    def create_preset_folder(self):
        try:
            created_path = makecfg()
            QMessageBox.information(self, "Preset config", f"Preset directory created: {created_path}")
        except Exception as exc:  # pragma: no cover - UI error reporting
            QMessageBox.critical(self, "Preset creation failed", str(exc))

    def execute_selected_action(self):
        action = self.action_combo.currentText()

        try:
            if action == "Remove packages from preset":
                preset_path = self.preset_path.text().strip()
                if (
                    not preset_path
                    or not os.path.isfile(preset_path)
                    or Path(preset_path).suffix.lower() != ".xm"
                ):
                    raise ValueError("Please select a valid .xm preset file before continuing.")
                RemovePackageADB(preset_path)
                QMessageBox.information(self, "Preset removal", "Package removal process finished.")

            elif action == "Install APK":
                apk_path = self.apk_path.text().strip()
                if not apk_path or not os.path.isfile(apk_path):
                    raise ValueError("Please choose a valid APK file before installing.")
                install(apk_path)
                QMessageBox.information(self, "Installation", "Install command has been sent to ADB.")

            elif action == "Uninstall package":
                pkg = self.package_name.text().strip()
                if not pkg:
                    raise ValueError("Please enter a package name to uninstall.")
                uninstall(pkg)
                QMessageBox.information(self, "Uninstall", f"ADB uninstall command sent for {pkg}.")

            elif action == "Force uninstall package":
                pkg = self.package_name.text().strip()
                if not pkg:
                    raise ValueError("Please enter a package name to force uninstall.")
                force_uninstall(pkg)
                QMessageBox.information(self, "Force uninstall", f"Force uninstall command sent for {pkg}.")

            elif action == "Create preset config":
                created_path = makecfg()
                QMessageBox.information(self, "Preset config", f"Preset directory created: {created_path}")

        except Exception as exc:  # pragma: no cover - UI error reporting
            QMessageBox.critical(self, "Action failed", str(exc))


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = OmniDebloatWizard()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
