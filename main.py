import sys

from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow

def main():

# Ініціалізація (QApplication): Створює базовий процес додатка та передає йому системні аргументи (sys.argv).
# Створення UI (MainWindow): Імпортує та створює екземпляр головного вікна з модуля ui/main_window.
# Відображення (window.show()): Робить вікно видимим для користувача.
# Цикл подій (app.exec()): Запускає нескінченний цикл очікування дій користувача (кліки, введення тексту тощо).
# Чисте завершення (sys.exit): Гарантує коректне закриття процесу Python після виходу з програми.
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

# дозволяє запускати цей файл як самостійний скрипт.

if __name__ == "__main__":
    main()
