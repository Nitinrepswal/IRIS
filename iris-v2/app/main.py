import os
import sys

from PySide6.QtWidgets import QApplication

from app.window import IRISWindow


def setup_runtime_directory():
    if getattr(sys, "frozen", False):
        runtime_directory = os.path.expanduser(
            "~/Library/Application Support/IRIS"
        )

        os.makedirs(runtime_directory, exist_ok=True)
        os.makedirs(
            os.path.join(runtime_directory, "sandbox"),
            exist_ok=True
        )
        os.makedirs(
            os.path.join(runtime_directory, "memory"),
            exist_ok=True
        )

        os.chdir(runtime_directory)


def main():
    setup_runtime_directory()

    app = QApplication(sys.argv)

    window = IRISWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()