import os


class Sandbox:
    def __init__(self, root="sandbox"):
        self.root = os.path.abspath(root)

        os.makedirs(
            self.root,
            exist_ok=True
        )

    def is_safe_path(self, path):
        target = os.path.abspath(
            os.path.join(self.root, path)
        )

        return (
            target == self.root
            or target.startswith(
                self.root + os.sep
            )
        )

    def get_safe_path(self, path):
        if not self.is_safe_path(path):
            raise PermissionError(
                "Path is outside the IRIS sandbox."
            )

        return os.path.abspath(
            os.path.join(self.root, path)
        )