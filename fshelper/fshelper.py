"""
    File system helper module
"""
import os
from db.controller import get_setting_value

class FsHelper:
    """
        FS helper. to provide os file system utility
    """
    def __new__(cls):
        if not hasattr(cls, 'fs_helper'):
            cls.fs_helper = super(FsHelper, cls).__new__(cls)

        return cls.fs_helper

    def get_base_dir(self):
        """helper class to get base dir"""
        base_dir = get_setting_value('BASE_DIR')
        parent_dir = base_dir if base_dir else os.getcwd()

        return parent_dir

    def make_dir(self, path):
        """helper class to create directory"""
        os.makedirs(path, exist_ok=True)

    def write_to_file(self, file_name, value):
        """
            write value to file
        """
        base_dir = self.get_base_dir()
        file_path = os.path.join(base_dir, file_name)
        dir_name = os.path.dirname(file_path)

        self.make_dir(dir_name)
        with open(file_path, 'w') as file_writer:
            file_writer.write(value)

__fs_helper = FsHelper()

def write_to_file(file_name, value):
    """Write to file api"""
    __fs_helper.write_to_file(file_name=file_name, value=value)
