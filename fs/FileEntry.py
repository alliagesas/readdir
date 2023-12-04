from smbprotocol.file_info import FileAttributes
from smbprotocol.open import FileAttributes
from acl import ACL

class FileEntry:
    def __init__(self, path, file_directory_info):
        self.name = file_directory_info['file_name'].value.decode('utf-16-le')
        self.path = r"%s\%s" % (path, self.name)
        self.ctime = file_directory_info['creation_time'].value
        self.atime = file_directory_info['last_access_time'].value
        self.wtime = file_directory_info['last_write_time'].value
        self.size = file_directory_info['allocation_size'].value
        self.attributes = file_directory_info['file_attributes'].value

        self.is_archive = self._flag_set(FileAttributes.FILE_ATTRIBUTE_ARCHIVE)
        self.is_compressed = self._flag_set(FileAttributes.FILE_ATTRIBUTE_COMPRESSED)
        self.is_directory = self._flag_set(FileAttributes.FILE_ATTRIBUTE_DIRECTORY)
        self.is_hidden = self._flag_set(FileAttributes.FILE_ATTRIBUTE_HIDDEN)
        self.is_normal = self._flag_set(FileAttributes.FILE_ATTRIBUTE_NORMAL)
        self.is_readonly = self._flag_set(FileAttributes.FILE_ATTRIBUTE_READONLY)
        self.is_reparse_point = self._flag_set(FileAttributes.FILE_ATTRIBUTE_REPARSE_POINT)
        self.is_system = self._flag_set(FileAttributes.FILE_ATTRIBUTE_SYSTEM)
        self.is_temporary = self._flag_set(FileAttributes.FILE_ATTRIBUTE_TEMPORARY)

        if self.is_directory:
            # Read ACL
            self.acl = ACL(self.path)

    def _flag_set(self, attribute):
        return self.attributes & attribute == attribute

    def heritage(self):
        return True
