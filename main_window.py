
# PyQt6:
    # QtWidgets (QMainWindow, QTableWidget, QDockWidget) — побудова каркаса інтерфейсу, таблиць, кнопок та випадаючих списків.
    # QtCore (QThread, pyqtSignal) — керування фоновими потоками та безпечна передача даних (прогресу, статусів) між потоками та GUI.
    # QtGui (QPainter) — низькорівневе малювання для створення вертикальної кнопки.

# collections (Counter) — вбудований модуль для швидкого підрахунку категорій.
# pathlib (Path) — безпечна робота зі шляхами файлів, виділення розширень документів.

from __future__ import annotations
from pathlib import Path
from collections import Counter

from PyQt6.QtCore import Qt, QThread, pyqtSignal, QObject, QSize, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QMainWindow, QDockWidget,
    QFileDialog, QTableWidget, QTableWidgetItem, QMessageBox, QComboBox, QProgressBar, QTableView, QSizePolicy,
    QGraphicsOpacityEffect, QHeaderView
)

from core.scanner import folder_way
from core.organizer import MovePlanItem
from core.extractor import extract_text

# OverlayWidget Створює ефект «розматого» або затемненого фону поверх основного вікна (часто використовується під час тривалого фонового процесу чи показу модальних вікон).
# rgba(0, 0, 0, 140) задає чорний колір із прозорістю.
# QGraphicsOpacityEffect додано для того, щоб у майбутньому можна було плавно (через анімацію) змінювати прозорість від 0.0 до 1.0.

class OverlayWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.hide()
        self.setStyleSheet("background-color: rgba(0, 0, 0, 140);")
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.opacity_effect.setOpacity(0.0)
        self.setGraphicsEffect(self.opacity_effect)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

# Звичайна кнопка QPushButton, але її текст повернуто вертикально на 90 градусів проти годинникової стрілки. Dикористовуються для бічноЇ панеі.
        
class RotatedButton(QPushButton):
    def __init__(self, text="", parent = None):
        super().__init__(text, parent)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def sizeHint(self):
        s = super().sizeHint()
        return QSize(s.height(), s.width())

    def minimumSizeHint(self):
        s = super().sizeHint()
        return QSize(s.height(), s.width())

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.translate(0, self.height())
        painter.rotate(-90)
        rect = painter.viewport()
        rect.setWidth(self.height())
        rect.setHeight(self.width())
        painter.fillRect(rect, self.palette().button())
        painter.setFont(self.font())
        painter.setPen(self.palette().buttonText().color())
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, self.text())


# Кастомний Drag & Drop
# Спадкується від QLabel, але вмикає підтримку перетягування через self.setAcceptDrops(True).
# У методі dragEnterEvent віджет суворо перевіряє, що саме користувач приніс. Якщо це не файл, а саме існуюча папка (is_dir()), інтерфейс змінює стиль на дружній синій (_set_hover_style()) та підсвічується.
# СЯкщо користувач відпускає мишку над зоною (dropEvent), віджет генерує кастомний Qt-сигнал folder_dropped.emit(str(first_path)). 
# Головне вікно зможе підписатися на цей сигнал і миттєво підтягнути шлях source.
        
class DropZone(QLabel):
    folder_dropped = pyqtSignal(str)
    def __init__(self):
        super().__init__("Drop source folder here")
        self.setAcceptDrops(True)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setMinimumHeight(260)
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        self._set_normal_style()

    def _set_normal_style(self):
        self.setStyleSheet("""
            QLabel {
                border: 2px dashed #6b7280;
                border-radius: 12px;
                padding: 18px;
                font-size: 14px;
                color: #9ca3af;
                background-color: #111827;
                }
            """)

    def _set_hover_style(self):
        self.setStyleSheet("""
            QLabel {
                border: 2px dashed #60a5fa;
                border-radius: 14px;
                padding: 18px;
                font-size: 14px;
                color: #dbeafe;
                background-color: #1e3a8a;
                }
            """)

    def dragEnterEvent(self, event):
        try:
            if event.mimeData().hasUrls():
                urls = event.mimeData().urls()
                if urls:
                    first_path = Path(urls[0].toLocalFile())
                    if first_path.exists() and first_path.is_dir():
                        self._set_hover_style()
                        event.acceptProposedAction()
                        return
            event.ignore()
        except Exception:
            event.ignore()

    def dragLeaveEvent(self, event):
        self._set_normal_style()
        event.accept()

    def dropEvent(self, event):
        try:
            self._set_normal_style()

            urls = event.mimeData().urls()
            if not urls:
                event.ignore()
                return

            first_path = Path(urls[0].toLocalFile())

            if first_path.exists() and first_path.is_dir():
                self.folder_dropped.emit(str(first_path))
                event.acceptProposedAction()
            else:
                event.ignore()
        except Exception:
            event.ignore()

# Потокобезпечна обробка помилок. 
# Якщо під час обробки конкретного (наприклад, третього з десяти) файлу нейромережа «впаде» з помилкою, додаток не закриється. 
# Програма запише йому категорію Misc/LLMError або Misc/Error, зафіксує статус невдачі й продовжить аналізувати інші файли. Це правильний підхід для софту, що працює з даними користувача.
# Гнучкість режимів - код чітко розділяє ai (класифікація через текстові промпти / генеративні моделі) та тестовий smart режим (семантичний пошук через порівняння близькості векторних ембеддингів).

class ScanWorker(QObject):
    progress_changed = pyqtSignal(int)
    status_changed = pyqtSignal(str)
    finished = pyqtSignal(list)
    error = pyqtSignal(str)

    def __init__(self, files, categorization_mode, embedder_categorizer, ai_open_categorizer):
        super().__init__()
        self.files = files
        self.categorization_mode = categorization_mode
        self.embedder_categorizer = embedder_categorizer
        self.ai_open_categorizer = ai_open_categorizer

    def run(self):
        try:
            total = len(self.files)
            if total == 0:
                self.finished.emit([])
                return
            files_rules = []
            for index, item in enumerate(self.files, start=1):
                self.status_changed.emit(f"[{index}/{total}]{item.name}")
                text = extract_text(item) or ""

                if self.categorization_mode == "ai":
                    try:
                        category, score, method = self.ai_open_categorizer.categorize(text)
                        score = f"{score:.3f}"
                    except Exception:
                        category = "Misc/LLMError"
                        score = "0.000"
                        method = "LLM_FAILED"
                elif self.categorization_mode == "smart":
                    try:
                        category, score_value, method = self.embedder_categorizer.categorize(text)
                        score = f"{score_value:.3f}"
                    except Exception:
                        category = "Misc/Error"
                        score = "0.000"
                        method = "EMBEDDING_FAILED"
                else:
                    category = "UNKNOWN"
                    score = "-"
                    method = "UNKNOWN_MODE"

                files_rules.append(
                    MovePlanItem(
                        source=item,
                        category=category,
                        score=score,
                        method=method
                    )
                )
                self.progress_changed.emit(int(index / total * 100))
            self.status_changed.emit("Done")
            self.finished.emit(files_rules)
        except Exception as e:
            self.error.emit(repr(e))

# Пряме зв'язування з ядром додатка, цей клас виступає мостом між інтерфейсом і модулем core/organizer.
# Передача емітерів сигналів як аргументів: Конструкція progress_callback=self.progress_changed.emit. 
# Функція сортування всередині core нічого не знає про PyQt6, вона просто викликає передану їй функцію-callback, а emit автоматично передає цей прогрес нагору у графічний інтерфейс.

class ApplyWorker(QObject):
    progress_changed = pyqtSignal(int)
    status_changed = pyqtSignal(str)
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, destination_folder, files_rules, mode):
        super().__init__()
        self.destination_folder = destination_folder
        self.files_rules = files_rules
        self.mode = mode

    def run(self):
        try:
            from core.organizer import organizer_sorted_folders
            organizer_sorted_folders(
                self.destination_folder, self.files_rules, self.mode,
                progress_callback=self.progress_changed.emit,
                status_callback=self.status_changed.emit)
            self.status_changed.emit("Apply done")
            self.finished.emit()

        except Exception as e:
            self.error.emit(repr(e))

# Конструктор — Центральний контролер інтерфейсу. 
# Реалізує компоновку макетів (QVBoxLayout, QHBoxLayout), конфігурує інтерактивну таблицю результатів QTableWidget з підтримкою сортування та задає єдиний темний стиль додатку через QSS (Qt Style Sheets).

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Categorizer (Beta)")
        self.resize(900, 520)

        self.files_rules: list[MovePlanItem] = []
        self.source_folder: str | None = None
        self.destination_folder: str | None = None
        self.files: list[Path] = []

        self.ai_open_categorizer = None

        self.embedder = None
        self.embedder_categorizer = None

        self.drop_zone = DropZone()
        self.drop_dock = QDockWidget("Drag and Drop", self)
        self.drop_dock.setMaximumWidth(0)
        self.drop_dock.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea)
        self.drop_dock.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.drop_dock.setVisible(True)
        dock_content = QWidget()
        dock_layout = QVBoxLayout()
        dock_layout.setContentsMargins(12, 12, 12, 12)
        dock_layout.setSpacing(10)
        drop_hint = QLabel("Drag & Drop a folder here to set it as source")
        drop_hint.setWordWrap(True)
        dock_layout.addWidget(drop_hint)
        dock_layout.addWidget(self.drop_zone ,1)
        dock_content.setLayout(dock_layout)
        self.drop_dock.setWidget(dock_content)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.drop_dock)

        self.label_source = QLabel("Source: (not selected)")
        self.label_destination = QLabel("Destination: (not selected)")
        self.status_label = QLabel("Ready")
        self.button_choose_source = QPushButton("Choose Source Folder")
        self.button_choose_destination = QPushButton("Choose Destination Folder")
        self.button_toggle_drop = RotatedButton("Drag and Drop")
        self.button_toggle_drop.setObjectName("DropToggleButton")
        self.button_toggle_drop.setCheckable(True)
        self.button_toggle_drop.setFixedWidth(18)
        self.button_toggle_drop.setMinimumHeight(600)
        self.button_scan = QPushButton("Scan")
        self.button_apply = QPushButton("Apply")

        self.mode_combo = QComboBox()
        self.mode_combo.addItem("Preview", "preview")
        self.mode_combo.addItem("Copy", "copy")
        self.mode_combo.addItem("Move", "move")
        self.mode_sorting = QComboBox()
        self.mode_sorting.addItem("Fast (Embeddings + Keywords)", "smart")
        self.mode_sorting.addItem("Smart (AI LLM)", "ai")

        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(
            ["Filename", "Extension", "Category", "Score", "Method", "Full path"]
        )
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.itemChanged.connect(self.on_item_changed)
        self._ignore_table_events = False
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(False)
        self.table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.table.setSortingEnabled(True)
        self.table.sortItems(0, Qt.SortOrder.AscendingOrder)
        self.table.horizontalHeader().setSortIndicatorShown(True)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)

        top_row = QHBoxLayout()
        top_row.addWidget(self.button_choose_source)
        top_row.addWidget(self.button_choose_destination)
        top_row.addStretch(1)
        top_row.addWidget(QLabel("Sorting mode:"))
        top_row.addWidget(self.mode_sorting)
        top_row.addWidget(QLabel("Duty:"))
        top_row.addWidget(self.mode_combo)
        top_row.setSpacing(10)
        for btn in [self.button_choose_destination, self.button_scan, self.button_apply]:
            btn.setMinimumHeight(36)

        action_row = QHBoxLayout()
        action_row.addWidget(self.button_scan)
        action_row.addWidget(self.button_apply)
        action_row.addStretch(1)

        main_layout = QVBoxLayout()
        main_layout.addLayout(top_row)
        main_layout.addWidget(self.label_source)
        main_layout.addWidget(self.label_destination)
        main_layout.addLayout(action_row)
        main_layout.addWidget(self.table)
        main_layout.addWidget(self.status_label)
        main_layout.addWidget(self.progress_bar)

        self.content_widget = QWidget()
        self.content_widget.setLayout(main_layout)
        self.content_effect = QGraphicsOpacityEffect(self.content_widget)
        self.content_effect.setOpacity(1.0)
        self.content_widget.setGraphicsEffect(self.content_effect)

        left_panel = QWidget()
        left_panel.setFixedWidth(28)
        left_bar = QVBoxLayout()
        left_bar.setContentsMargins(0, 0, 0, 0)
        left_bar.setSpacing(0)
        left_bar.addStretch()
        left_bar.addWidget(self.button_toggle_drop, alignment=Qt.AlignmentFlag.AlignCenter)
        left_bar.addStretch()
        left_panel.setLayout(left_bar)

        common_layout = QHBoxLayout()
        common_layout.setContentsMargins(0, 0, 0, 0)
        common_layout.setSpacing(10)
        common_layout.addWidget(left_panel)
        common_layout.addWidget(self.content_widget, 1)
        central_widget = QWidget()
        central_widget.setLayout(common_layout)
        self.setCentralWidget(central_widget)

        self.overlay = OverlayWidget(self.content_widget)
        self.overlay.setGeometry(self.content_widget.rect())
        self.overlay.hide()
        self.overlay.raise_()

        self.button_toggle_drop.clicked.connect(self.toggle_drop_panel)
        self.drop_zone.folder_dropped.connect(self.set_source_folder_from_drop)
        self.button_choose_source.clicked.connect(self.choose_source_folder)
        self.button_choose_destination.clicked.connect(self.choose_destination_folder)
        self.button_scan.clicked.connect(self.scan)
        self.button_apply.clicked.connect(self.apply)
        self.button_scan.setEnabled(False)
        self.button_apply.setEnabled(False)

        self.scan_thread = None
        self.scan_worker = None
        self.apply_thread = None
        self.apply_worker = None

        self.setStyleSheet("""
            QWidget {
                background-color: #0b1220;
                color: #e5e7eb;
                font-family: Segoe UI;
                font-size: 13px;
            }
            QPushButton {
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 10px;
                padding: 8px 14px;
            }
            QPushButton:hover {
                background-color: #334155;
            }
            QPushButton:pressed {
                background-color: #475569;
            }
            QPushButton:checked {
                background-color: #2563eb;
                border: 1px solid #3b82f6;
            }
            QPushButton#DropToggleButton {
                background-color: #111827;
                color: #cbd5e1;
                border: 1px solid #334155;
                border-left: none;
                border-top-right-radius: 10px;
                border-bottom-right-radius: 10px;
                border-top-left-radius: 0px;
                border-bottom-left-radius: 0px;
                padding: 2px 0px;
                font-size: 10px;
                font-weight: 700;
            }
            QPushButton#DropToggleButton:hover {
                background-color: #1e293b;
                color: #f8fafc;
                border-color: #475569;
            }
            QPushButton#DropToggleButton:pressed {
                background-color: #334155;
            }
            QPushButton#DropToggleButton:checked {
                background-color: #3b82f6;
            }
            QComboBox {
                background-color: #111827;
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 6px 10px;
            }
            QTableWidget {
                background-color: #111827;
                alternate-background-color: #0f172a;
                border: 1px solid #334155;
                border-radius: 10px;
                gridline-color: #1f2937;
            }
            QTableWidget::item:selected {
                background-color: #1d4ed8;
                color: #e0e7ff;
            }
            QTableWidget::item {
                background-color: #111827;
                color: #e5e7eb;
            }
            QHeaderView::section {
                background-color: #1e293b;
                color: #f8fafc;
                padding: 6px;
                border: none;
            }
            QHeaderView::section:vertical {
                background-color: #1e293b;
                color: #e5e7eb;
            }
            QTableCornerButton::section {
                background-color: #1e293b;
                border: none;
            }
            QProgressBar {
                border: 1px solid #334155;
                border-radius: 8px;
                text-align: center;
                background-color: #111827;
            }
            QProgressBar::chunk {
                background-color: #3b82f6;
                border-radius: 6px;
            }
            QLabel {
                background: transparent;
            }
        """)


# Патерн «Ледаче завантаження» (Lazy Loading). Моделі ШІ та ваги нейромереж ініціалізуються в пам'яті лише в момент виклику відповідного режиму, що забезпечує миттєвий старт графічної оболонки додатка. 
# Пінгування сервера Ollama винесено в нативний потік Python, щоб уникнути фризів вікна.
    
    def ensure_embedding_components(self):
        if self.embedder is None:
            from core.embeddings import Embedder
            self.embedder = Embedder()

        if self.embedder_categorizer is None:
            from core.basic_categorizer import EmbedderCategorizer
            self.embedder_categorizer = EmbedderCategorizer(embedder=self.embedder)

    def ensure_llm_components(self):
        if self.ai_open_categorizer is None:
            from core.categorizer_ai import LLMCategorizer
            self.ai_open_categorizer = LLMCategorizer()

            import threading
            from core.llm_utils import ensure_ollama_ready

            threading.Thread(target=ensure_ollama_ready, daemon=True).start()

# Обробники встановлення цільових директорій. Реалізують два альтернативні інтерфейси введення: через Drag & Drop (сигнал від кастомної зони) або через нативні діалогові вікна ОС (QFileDialog.getExistingDirectory).
    
    def set_source_folder_from_drop(self, folder_path: str):
        self.source_folder = folder_path
        self.label_source.setText(f"Source: {folder_path}")
        self.status_label.setText("Folder dropped successfully")
        self._update_buttons()

    def choose_source_folder(self):
        path = QFileDialog.getExistingDirectory(self, "Select Source Folder")
        if not path:
            return
        self.source_folder = path
        self.label_source.setText(f"Source: {path}")
        self._update_buttons()

    def choose_destination_folder(self):
        path = QFileDialog.getExistingDirectory(self, "Select Destination Folder")
        if not path:
            return
        self.destination_folder = path
        self.label_destination.setText(f"Destination: {path}")
        self._update_buttons()

# Автоматичний реактивний контроль стану UI. Динамічно керує доступністю кнопок (setEnabled), перевіряючи наявність обраних шляхів у пам'яті додатка та валідність списку запланованих дій.

    def _update_buttons(self):
        self.button_scan.setEnabled(bool(self.source_folder))
        self.button_apply.setEnabled(bool(self.destination_folder) and len(self.files_rules) > 0)

# Метод рендерингу результатів аналізу в QTableWidget. Тимчасово вимикає сортування та генерацію подій (_ignore_table_events) для уникнення аномалій рекурсії під час масової вставки рядків. 
# За допомогою побітових масок (~Qt.ItemFlag.ItemIsEditable) блокує для редагування всі стовпці, окрім стовпця «Категорія».

    def _fill_table(self, files_rules: list[MovePlanItem]):
        self._ignore_table_events = True
        self.table.setSortingEnabled(False)
        self.table.setRowCount(0)

        for item_rules in files_rules:
            item = item_rules.source
            row = self.table.rowCount()
            self.table.insertRow(row)

            name_item = QTableWidgetItem(item.name)
            extension_item = QTableWidgetItem(item.suffix.lower())
            category_item = QTableWidgetItem(item_rules.category)
            category_item.setToolTip(f"Detected by: {item_rules.method}")
            score_item = QTableWidgetItem(str(item_rules.score))
            method_item = QTableWidgetItem(str(item_rules.method))
            path_item = QTableWidgetItem(str(item))

            name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            extension_item.setFlags(extension_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            score_item.setFlags(score_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            method_item.setFlags(method_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            path_item.setFlags(path_item.flags() & ~Qt.ItemFlag.ItemIsEditable)

            self.table.setItem(row, 0, name_item)
            self.table.setItem(row, 1, extension_item)
            self.table.setItem(row, 2, category_item)
            self.table.setItem(row, 3, score_item)
            self.table.setItem(row, 4, method_item)
            self.table.setItem(row, 5, path_item)

        self.table.setSortingEnabled(True)
        self._ignore_table_events = False

# Метод ініціалізації багатопотокового аналізу. Запускає сканування через folder_way, конфігурує компоненти ШІ відповідно до обраного режиму й створює екземпляр класу QThread. 
# Передає об'єкт ScanWorker у фоновий потік, зв'язуючи його життєвий цикл (started/finished) з очищенням пам'яті (deleteLater).
    
    def scan(self):
        if not self.source_folder:
            QMessageBox.warning(self, "Missing source", "Choose source folder first.")
            return

        self.setEnabled(False)
        self.files = folder_way(self.source_folder, exclude_folder={"MainSortedFolders"})
        mode_sorting = self.mode_sorting.currentData()
        if mode_sorting in {"smart"}:
            try:
                self.ensure_embedding_components()
            except Exception as e:
                QMessageBox.critical(self, "Embedding init failed", repr(e))
                self.setEnabled(True)
                return

        if mode_sorting == "ai":
            self.ensure_llm_components()

        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.status_label.setText("Starting scan...")

        self.button_scan.setEnabled(False)
        self.button_apply.setEnabled(False)

        self.scan_thread = QThread()

        self.scan_worker = ScanWorker(
            files=self.files,
            categorization_mode=mode_sorting,
            embedder_categorizer=self.embedder_categorizer,
            ai_open_categorizer=self.ai_open_categorizer
        )

        self.scan_worker.moveToThread(self.scan_thread)
        self.scan_thread.started.connect(self.scan_worker.run)
        self.scan_worker.progress_changed.connect(self.on_progress_changed)
        self.scan_worker.status_changed.connect(self.on_status_changed)
        self.scan_worker.finished.connect(self.on_scan_finished)
        self.scan_worker.error.connect(self.on_scan_error)

        self.scan_worker.finished.connect(self.scan_thread.quit)
        self.scan_worker.finished.connect(self.scan_worker.deleteLater)
        self.scan_thread.finished.connect(self.scan_thread.deleteLater)

        self.scan_thread.start()

# Метод ініціалізації фізичних операцій на диску. 
# Аналогічно до сканування, делегує «важку» операцію копіювання чи переміщення файлів окремому асинхронному потоку ApplyWorker, захищаючи графічну оболонку від зависання під час дискового вводу-виводу.
    
    def apply(self):
        if not self.destination_folder:
            QMessageBox.warning(self, "Missing destination", "Choose destination folder first.")
            return
        if not self.files:
            QMessageBox.warning(self, "Nothing to do", "Scan first (no files in list).")
            return

        mode = self.mode_combo.currentData()

        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.status_label.setText("Applying...")

        self.button_scan.setEnabled(False)
        self.button_apply.setEnabled(False)

        self.apply_thread = QThread()
        self.apply_worker = ApplyWorker(
            destination_folder=self.destination_folder, files_rules=self.files_rules, mode=mode
        )

        self.apply_worker.moveToThread(self.apply_thread)
        self.apply_thread.started.connect(self.apply_worker.run)
        self.apply_worker.progress_changed.connect(self.on_progress_changed)
        self.apply_worker.status_changed.connect(self.on_status_changed)
        self.apply_worker.finished.connect(self.on_apply_finished)
        self.apply_worker.error.connect(self.on_apply_error)

        self.apply_worker.finished.connect(self.apply_thread.quit)
        self.apply_worker.finished.connect(self.apply_worker.deleteLater)
        self.apply_thread.finished.connect(self.apply_thread.deleteLater)

        self.apply_thread.start()

# Слот зворотного зв'язку (подія редагування клітинки). 
# Дозволяє користувачу вручну перевизначити семантичну категорію файлу безпосередньо в таблиці перед фізичним сортуванням. 
# Метод перезаписує відповідний об'єкт MovePlanItem у загальному списку.
    
    def on_item_changed(self, item: QTableWidgetItem):
        if self._ignore_table_events:
            return

        row = item.row()
        column = item.column()

        if column != 2:
            return

        new_category = item.text().strip()
        if not new_category:
            new_category = "UNKNOWN"
            item.setText(new_category)
        old_item = self.files_rules[row]

        self.files_rules[row] = MovePlanItem(
            source=old_item.source,
            category=new_category,
            score=old_item.score,
            method=old_item.method)

# Приймають асинхронні сигнали від фонових робочих потоків для динамічного оновлення прогрес-бару та текстового рядка стану в реальному часі.

    def on_progress_changed(self, value: int):
        self.progress_bar.setValue(value)

    def on_status_changed(self, text: str):
        self.status_label.setText(f"Processing -> {text}")

# Обробники успішного завершення задач. Повертають інтерфейс у штатної режим, ховають прогрес-бар, викликають оновлення таблиці та виводять інформаційне модальне вікно QMessageBox з фінальним звітом.

    def on_apply_finished(self):
        self.progress_bar.setValue(100)
        self.progress_bar.setVisible(False)
        self.status_label.setText("Operation done")
        self.button_scan.setEnabled(True)
        self.button_apply.setEnabled(bool(self.destination_folder) and len(self.files_rules) > 0)
        QMessageBox.information(self, "Operation done", "Operation finished. Check logs/ for report.")

    def on_scan_finished(self, files_rules: list):
        self.files_rules = files_rules
        self._fill_table(self.files_rules)
        self._update_buttons()
        self.progress_bar.setValue(100)
        self.progress_bar.setVisible(False)
        self.status_label.setText(f"Done. Found files: {len(self.files_rules)}")
        self.setEnabled(True)
        self.button_scan.setEnabled(True)
        self.button_apply.setEnabled(bool(self.destination_folder) and len(self.files_rules) > 0)
        summary_text = self.build_scan_summary(self.files_rules)
        QMessageBox.information(self, "Scan complete", summary_text)

# Обробники виняткових ситуацій (ексепшенів). Ловлять критичні помилки з фонових потоків, скидають стан інтерфейсу та інформують користувача через діалог помилки QMessageBox.critical.

    def on_scan_error(self, error_text: str):
        self.progress_bar.setVisible(False)
        self.status_label.setText("Scan error")
        self.setEnabled(True)
        self.button_scan.setEnabled(True)
        self._update_buttons()
        QMessageBox.critical(self, "Scan failed", error_text)

    def on_apply_error(self, error_text: str):
        self.progress_bar.setVisible(False)
        self.status_label.setText("Apply error")
        self.button_scan.setEnabled(True)
        self._update_buttons()
        QMessageBox.critical(self, "Apply failed", error_text)

# Реалізують плавне візуальне занурення основного контенту (затемнення фону за допомогою QPropertyAnimation по властивості opacity), коли відкривається бічна панель.

    def fade_in_overlay(self):
        self.dim_animation = QPropertyAnimation(self.content_effect, b"opacity")
        self.dim_animation.setDuration(220)
        self.dim_animation.setStartValue(self.content_effect.opacity())
        self.dim_animation.setEndValue(0.45)
        self.dim_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.dim_animation.start()

    def fade_out_overlay(self):
        self.dim_animation = QPropertyAnimation(self.content_effect, b"opacity")
        self.dim_animation.setDuration(180)
        self.dim_animation.setStartValue(self.content_effect.opacity())
        self.dim_animation.setEndValue(1.0)
        self.dim_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.dim_animation.start()

# Обробник тригера висувної шторки. Керує властивістю maximumWidth віджета QDockWidget за допомогою закону плавности ходу OutCubic. 
# Змінює ширину панелі між 0 та 260 пікселями, забезпечуючи плавний інтерфейсний перехід.

    def toggle_drop_panel(self):
        should_open = self.button_toggle_drop.isChecked()
        target_width = 260 if should_open else 0
        self.animation = QPropertyAnimation(self.drop_dock, b"maximumWidth")
        self.animation.setDuration(250)
        self.animation.setStartValue(self.drop_dock.maximumWidth())
        self.animation.setEndValue(target_width)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.animation.start()
        self.animation.finished.connect(self.sync_drop_button_state)
        if should_open:
            self.fade_in_overlay()
        else:
            self.fade_out_overlay()

    def sync_drop_button_state(self):
        is_open = self.drop_dock.maximumWidth() > 0
        self.button_toggle_drop.setChecked(is_open)

# Перевизначений системний метод зміни розміру вікна. Гарантує, що матриця блокувального оверлея (overlay) завжди точно масштабується під нові геометричні кордони контейнера контенту.

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, "overlay") and hasattr(self, "content_widget"):
            self.overlay.setGeometry(self.content_widget.rect())

# Статистичний аналізатор результатів сканування. 
# Використовує клас collections.Counter для агрегації даних, підраховуючи кількість файлів у кожній категорії, та формує текстовий звіт для фінального вікна.

    def build_scan_summary(self, files_rules: list[MovePlanItem]) -> str:
        if not files_rules:
            return "Found files: 0"
        counts = Counter(item.category for item in files_rules)
        lines = [f"Found files: {len(files_rules)}", ""]
        for category, count in counts.most_common():
            lines.append(f"{category}: {count}")
        return "\n".join(lines)
