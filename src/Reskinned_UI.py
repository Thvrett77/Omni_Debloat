import os
import sys
from pathlib import Path

from PyQt6.QtCore import (
    QEasingCurve,
    QObject,
    QPropertyAnimation,
    QThread,
    Qt,
    pyqtSignal,
)
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QFrame,
    QGraphicsOpacityEffect,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QProgressBar,
    QVBoxLayout,
    QWidget,
    QWizard,
    QWizardPage,
)

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from Updated_GUI import (  # noqa: E402
    DeviceCheckPage,
    ExperimentalWizardBase,
)
from adbcheck import RemovePackageADB  # noqa: E402
from check_download_presets import Get_Content_Out_Of_CDN  # noqa: E402


RESKINNED_STYLE = """
QWidget {
    background: #080808;
    color: #f2f2f2;
    font-family: "Segoe UI Variable", "Segoe UI", sans-serif;
    font-size: 10pt;
}
QWizard, QWizardPage, QMessageBox { background: #080808; color: #f2f2f2; }
QWizardPage { padding: 18px; }
QLabel { background: transparent; color: #f2f2f2; }
QLineEdit, QPlainTextEdit, QComboBox {
    color: #f2f2f2;
    background: #141414;
    border: 1px solid #383838;
    border-radius: 8px;
    selection-background-color: #f2f2f2;
    selection-color: #080808;
}
QLineEdit, QComboBox { min-height: 38px; padding: 0 12px; }
QPlainTextEdit { padding: 12px; }
QLineEdit:focus, QPlainTextEdit:focus, QComboBox:focus {
    border: 2px solid #f2f2f2;
}
QComboBox::drop-down {
    width: 34px;
    border-left: 1px solid #383838;
}
QComboBox QAbstractItemView {
    color: #f2f2f2;
    background: #141414;
    border: 1px solid #383838;
    selection-background-color: #f2f2f2;
    selection-color: #080808;
}
QPushButton {
    min-height: 38px;
    padding: 0 16px;
    color: #f2f2f2;
    background: #1c1c1c;
    border: 1px solid #424242;
    border-radius: 8px;
}
QPushButton:hover { background: #303030; border-color: #f2f2f2; }
QPushButton:pressed { background: #111111; }
QPushButton:default {
    color: #080808;
    background: #f2f2f2;
    border-color: #f2f2f2;
    font-weight: 700;
}
QPushButton:default:hover { background: #d6d6d6; }
QPushButton:disabled { color: #777777; background: #141414; }
QProgressBar {
    min-height: 12px;
    color: #f2f2f2;
    background: #1c1c1c;
    border: 0;
    border-radius: 6px;
    text-align: center;
}
QProgressBar::chunk { background: #f2f2f2; border-radius: 6px; }
QToolTip {
    color: #f2f2f2;
    background: #141414;
    border: 1px solid #424242;
    padding: 5px;
}
"""

ANIMATION_DURATION_MS = 320


def apply_reskinned_theme(app):
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor("#080808"))
    palette.setColor(QPalette.ColorRole.WindowText, QColor("#f2f2f2"))
    palette.setColor(QPalette.ColorRole.Base, QColor("#141414"))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor("#1c1c1c"))
    palette.setColor(QPalette.ColorRole.Text, QColor("#f2f2f2"))
    palette.setColor(QPalette.ColorRole.Button, QColor("#1c1c1c"))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor("#f2f2f2"))
    palette.setColor(QPalette.ColorRole.Highlight, QColor("#f2f2f2"))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#080808"))
    app.setPalette(palette)
    app.setStyleSheet(RESKINNED_STYLE)


class ReskinnedRemovalWorker(QObject):
    progress = pyqtSignal(int, int, str)
    finished = pyqtSignal(str, str, str)

    def __init__(self, source, value):
        super().__init__()
        self.source = source
        self.value = value

    def run(self):
        try:
            if self.source == "auto":
                preset = Get_Content_Out_Of_CDN(str(ROOT / "temp_list.json"))
                if not preset.strip():
                    raise RuntimeError("The auto-detected preset is empty.")
            else:
                preset = self.value
            message, warning = RemovePackageADB(preset, self.progress.emit)
            self.finished.emit(message, warning, "")
        except Exception as exc:
            self.finished.emit("", "", str(exc))


class ReskinnedPresetPage(QWizardPage):
    def __init__(self, wizard):
        super().__init__()
        self.wizard = wizard

    def validatePage(self):
        source = self.wizard.preset_source.currentData()
        if source == "string":
            if self.wizard.preset_text.toPlainText().strip():
                return True
            message = "Enter at least one package name before continuing."
        elif source == "file":
            preset_path = self.wizard.preset_path.text().strip()
            if (
                preset_path
                and os.path.isfile(preset_path)
                and Path(preset_path).suffix.lower() == ".xm"
            ):
                return True
            message = "Choose a valid .xm preset file before continuing."
        else:
            return True

        QMessageBox.warning(self, "Preset required", message)
        return False

    def nextId(self):
        return self.wizard.progress_page_id


class ReskinnedProgressPage(QWizardPage):
    def __init__(self, wizard):
        super().__init__()
        self.wizard = wizard
        self.started = False
        self.progress_animation = None

    def initializePage(self):
        if self.started:
            return
        self.started = True
        self.wizard.setButtonText(QWizard.WizardButton.FinishButton, "Run")
        self.wizard.button(QWizard.WizardButton.FinishButton).setEnabled(False)
        self.status_label.setText("Preparing package removal...")
        self.result_label.clear()

        source = self.wizard.preset_source.currentData()
        value = (
            self.wizard.preset_text.toPlainText().strip()
            if source == "string"
            else self.wizard.preset_path.text().strip()
        )
        self.wizard.removal_thread = QThread(self.wizard)
        self.wizard.removal_worker = ReskinnedRemovalWorker(source, value)
        self.wizard.removal_worker.moveToThread(self.wizard.removal_thread)
        self.wizard.removal_thread.started.connect(self.wizard.removal_worker.run)
        self.wizard.removal_worker.progress.connect(self._update_progress)
        self.wizard.removal_worker.finished.connect(self._removal_finished)
        self.wizard.removal_worker.finished.connect(self.wizard.removal_thread.quit)
        self.wizard.removal_worker.finished.connect(
            self.wizard.removal_worker.deleteLater
        )
        self.wizard.removal_thread.finished.connect(
            self.wizard._removal_thread_finished
        )
        self.wizard.removal_thread.finished.connect(
            self.wizard.removal_thread.deleteLater
        )
        self.wizard.removal_thread.start()

    def _update_progress(self, current, total, package):
        self.progress_bar.setRange(0, total)
        if self.progress_animation is not None:
            self.progress_animation.stop()
        self.progress_animation = QPropertyAnimation(
            self.progress_bar, b"value", self.progress_bar
        )
        self.progress_animation.setDuration(220)
        self.progress_animation.setStartValue(self.progress_bar.value())
        self.progress_animation.setEndValue(current)
        self.progress_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.progress_animation.start()
        self.status_label.setText(f"Removing package {current} of {total}: {package}")

    def _removal_finished(self, message, warning, error_message):
        if error_message:
            self.status_label.setText("Package removal failed")
            self.result_label.setText(error_message)
            self.result_label.setStyleSheet("color: #f2f2f2;")
        else:
            if self.progress_bar.maximum() == 0:
                self.progress_bar.setRange(0, 1)
            if self.progress_animation is not None:
                self.progress_animation.stop()
            self.progress_animation = QPropertyAnimation(
                self.progress_bar, b"value", self.progress_bar
            )
            self.progress_animation.setDuration(220)
            self.progress_animation.setStartValue(self.progress_bar.value())
            self.progress_animation.setEndValue(self.progress_bar.maximum())
            self.progress_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
            self.progress_animation.start()
            self.status_label.setText("Package removal complete")
            self.result_label.setText(f"{message}\n{warning}")
            self.result_label.setStyleSheet("color: #f2f2f2;")
        self.wizard.setButtonText(QWizard.WizardButton.FinishButton, "Done")
        self.wizard.button(QWizard.WizardButton.FinishButton).setEnabled(True)


class ReskinnedOmniDebloatWizard(ExperimentalWizardBase):
    def __init__(self):
        super().__init__()
        self._page_fade = None
        self.currentIdChanged.connect(self._animate_current_page)

    def showEvent(self, event):
        super().showEvent(event)
        self._animate_current_page()

    def _animate_current_page(self, *_):
        page = self.currentPage()
        if page is None:
            return
        if self._page_fade is not None:
            self._page_fade.stop()
            self._page_fade.deleteLater()

        opacity = QGraphicsOpacityEffect(page)
        page.setGraphicsEffect(opacity)
        self._page_fade = QPropertyAnimation(opacity, b"opacity", self)
        self._page_fade.setDuration(ANIMATION_DURATION_MS)
        self._page_fade.setStartValue(0.0)
        self._page_fade.setEndValue(1.0)
        self._page_fade.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._page_fade.start()

    def _set_page_theme(self, page):
        app = QApplication.instance()
        if app is not None:
            apply_reskinned_theme(app)
        page.setStyleSheet(RESKINNED_STYLE)

    def create_intro_page(self):
        page = QWizardPage()
        page.setTitle("Welcome")
        page.setSubTitle("A cleaner workspace for Android device maintenance.")
        self._set_page_theme(page)

        layout = QVBoxLayout(page)
        layout.setContentsMargins(22, 24, 22, 24)
        layout.setSpacing(18)

        eyebrow = QLabel("OMNI DEBLOAT  /  DEVICE TOOLS")
        eyebrow.setStyleSheet("color: #f2f2f2; font-weight: 700; letter-spacing: 1px;")
        layout.addWidget(eyebrow)

        title = QLabel("Take control\nof your device.")
        title.setStyleSheet("font-size: 30pt; font-weight: 700; color: #ffffff;")
        layout.addWidget(title)

        description = QLabel(
            "Connect over ADB, provide a package list or preset, then review the "
            "removal progress."
        )
        description.setWordWrap(True)
        description.setStyleSheet("font-size: 11pt; color: #b5b5b5;")
        layout.addWidget(description)

        card = QFrame()
        card.setObjectName("introCard")
        card.setStyleSheet(
            "QFrame#introCard { background: #141414; border: 1px solid #383838; "
            "border-radius: 12px; padding: 12px; }"
        )
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(10)
        for heading, detail in (
            ("01  Connect", "Verify your Android device through ADB."),
            ("02  Add packages", "Paste package names or choose a preset file."),
            ("03  Remove", "Track progress and see the result."),
        ):
            step = QLabel(
                f"<b>{heading}</b><br>"
                f"<span style='color:#b5b5b5'>{detail}</span>"
            )
            step.setTextFormat(Qt.TextFormat.RichText)
            card_layout.addWidget(step)
        layout.addWidget(card)
        layout.addStretch(1)
        return page

    def create_device_page(self):
        page = DeviceCheckPage(self)
        page.setTitle("Device connection")
        page.setSubTitle("Make sure Android Debug Bridge can see your device.")
        self._set_page_theme(page)

        layout = QVBoxLayout(page)
        layout.setContentsMargins(22, 20, 22, 24)
        layout.setSpacing(16)
        title = QLabel("ADB connection")
        title.setStyleSheet("font-size: 18pt; font-weight: 700;")
        layout.addWidget(title)
        self.device_status.setText("Not checked yet")
        self.device_status.setStyleSheet(
            "padding: 16px; background: #141414; border: 1px solid #383838; "
            "border-radius: 10px; color: #b5b5b5;"
        )
        layout.addWidget(self.device_status)
        self.check_button = QPushButton(" Check ADB connection ") # Leave the Spaces between the texts since idk how to fix it with another solution
        self.check_button.clicked.connect(self.check_adb_connection)
        layout.addWidget(self.check_button, alignment=Qt.AlignmentFlag.AlignLeft)
        detail = QLabel(
            "Unlock your phone and accept the USB debugging prompt if Android asks."
        )
        detail.setWordWrap(True)
        detail.setStyleSheet("color: #b5b5b5;")
        layout.addWidget(detail)
        layout.addStretch(1)
        return page

    def create_preset_page(self):
        page = ReskinnedPresetPage(self)
        page.setTitle("Remove packages from preset")
        page.setSubTitle("Paste package names directly or choose another source.")
        self._set_page_theme(page)

        was_blocked = self.preset_source.blockSignals(True)
        self.preset_source.clear()
        self.preset_source.addItem("Paste package list", "string")
        self.preset_source.addItem("Choose .xm file", "file")
        self.preset_source.addItem("Auto-detect for device", "auto")
        self.preset_source.blockSignals(was_blocked)

        layout = QVBoxLayout(page)
        layout.setContentsMargins(22, 20, 22, 24)
        layout.setSpacing(12)
        title = QLabel("Package list")
        title.setStyleSheet("font-size: 18pt; font-weight: 700;")
        layout.addWidget(title)
        detail = QLabel(
            "Paste package names below, one per line. Lines starting with # are ignored."
        )
        detail.setWordWrap(True)
        detail.setStyleSheet("color: #b5b5b5;")
        layout.addWidget(detail)
        layout.addWidget(self.preset_source)

        self.preset_text = QPlainTextEdit()
        self.preset_text.setPlaceholderText(
            "com.example.app\ncom.example.service\n\n# Comment lines are ignored"
        )
        self.preset_text.setMinimumHeight(190)
        layout.addWidget(self.preset_text, 1)

        self.preset_row = QWidget()
        file_layout = QHBoxLayout(self.preset_row)
        file_layout.setContentsMargins(0, 0, 0, 0)
        file_layout.setSpacing(8)
        self.preset_path.setPlaceholderText("Select a .xm preset file")
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_preset)
        file_layout.addWidget(self.preset_path, 1)
        file_layout.addWidget(self.browse_button)
        layout.addWidget(self.preset_row)

        self.preset_hint = QLabel()
        self.preset_hint.setWordWrap(True)
        self.preset_hint.setStyleSheet("color: #b5b5b5;")
        layout.addWidget(self.preset_hint)
        layout.addStretch(1)
        self._preset_source_changed()
        return page

    def create_progress_page(self):
        page = ReskinnedProgressPage(self)
        page.setTitle("Removing packages")
        page.setSubTitle("Package removal progress and results.")
        self._set_page_theme(page)

        layout = QVBoxLayout(page)
        layout.setContentsMargins(22, 20, 22, 24)
        layout.setSpacing(16)
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

    def browse_preset(self):
        if self.preset_source.currentData() != "file":
            return
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Choose a preset file",
            os.getcwd(),
            "XM Files (*.xm);;All Files (*)",
        )
        if file_path:
            self.preset_path.setText(file_path)

    def _preset_source_changed(self, *_):
        source = self.preset_source.currentData()
        self.preset_text.setVisible(source == "string")
        self.preset_row.setVisible(source == "file")
        hints = {
            "string": "Package names may be separated by spaces or new lines.",
            "file": "Select an existing .xm preset file.",
            "auto": "The matching preset will be fetched for the connected device.",
        }
        self.preset_hint.setText(hints.get(source, ""))

    def _update_run_button_text(self, *_):
        page = self.currentPage()
        is_removal_run = (
            page is not None and page.title() == "Remove packages from preset"
        )
        label = "Run" if is_removal_run else "Next"
        self.setButtonText(QWizard.WizardButton.NextButton, label)

    def _adb_check_finished(self, connected, error_message):
        super()._adb_check_finished(connected, error_message)
        if connected and not error_message:
            self.device_status.setStyleSheet(
                "padding: 16px; background: #1b1b1b; border: 1px solid #f2f2f2; "
                "border-radius: 10px; color: #ffffff;"
            )
        elif not connected or error_message:
            self.device_status.setStyleSheet(
                "padding: 16px; background: #111111; border: 1px solid #777777; "
                "border-radius: 10px; color: #b5b5b5;"
            )

    def _removal_thread_finished(self):
        self.removal_worker = None
        self.removal_thread = None


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setApplicationName("Omni Debloat")
    apply_reskinned_theme(app)
    window = ReskinnedOmniDebloatWizard()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
