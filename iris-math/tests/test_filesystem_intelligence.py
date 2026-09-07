import os


class FilesystemTool:
    def list_directory(self, path):
        if not os.path.isdir(path):
            return "Directory not found"

        return os.listdir(path)

    def file_exists(self, path):
        return os.path.isfile(path)

    def absolute_path(self, path):
        return os.path.abspath(path)


class IRISFilesystemAgent:
    def __init__(self):
        self.filesystem = FilesystemTool()

    def run(self, path):
        print("IRIS FILESYSTEM INTELLIGENCE")
        print("=" * 40)

        print("\nDIRECTORY")
        print(path)

        print("\nFILES")
        files = self.filesystem.list_directory(path)

        if isinstance(files, list):
            for file in files:
                print(file)
        else:
            print(files)

        print("\nABSOLUTE PATH")
        print(self.filesystem.absolute_path(path))


agent = IRISFilesystemAgent()

project_path = "/Users/nitin/Desktop/IRIS/iris-math"

agent.run(project_path)