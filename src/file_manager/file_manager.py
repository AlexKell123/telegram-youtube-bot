import os

class FileManager:
    @staticmethod
    def delete_file(file_name):
        os.remove(file_name)
