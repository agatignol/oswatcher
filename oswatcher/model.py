import stat
from enum import Enum

from py2neo.ogm import GraphObject, Property, RelatedTo


class OS(GraphObject):

    def __init__(self, name, release_date):
        super().__init__()
        self.name = name
        self.release_date = release_date

    # properties
    name = Property()
    release_date = Property()

    # relationships
    root_fileystem = RelatedTo("GraphInode", "OWNS_FILESYSTEM")
    syscall_tables = RelatedTo("SyscallTable", "OWNS_SYSCALL_TABLE")
    processes = RelatedTo("Process", "OWNS_PROCESS")


class InodeType(Enum):
    DIR = stat.S_IFDIR
    CHR = stat.S_IFCHR
    BLK = stat.S_IFBLK
    REG = stat.S_IFREG
    FIFO = stat.S_IFIFO
    LNK = stat.S_IFLNK
    SOCK = stat.S_IFSOCK
    DOOR = stat.S_IFDOOR


class GraphInode(GraphObject):

    def __init__(self, inode):
        super().__init__()
        # default
        self.checksec = False

        self.s_filepath = str(inode.path)
        self.name = inode.name
        # if guestfs.is_file(self.s_filepath) and checksums:
        #     # checksums
        #     self.md5sum = guestfs.checksum('md5', self.s_filepath)
        #     self.sha1sum = guestfs.checksum('sha1', self.s_filepath)
        #     self.sha256sum = guestfs.checksum('sha256', self.s_filepath)
        #     self.sha512sum = guestfs.checksum('sha512', self.s_filepath)

        # l -> if symbolic link, returns info about the link itself
        self.size = inode.size
        self.mode = inode.mode
        self.inode_type = inode.inode_type
        self.file_type = inode.file_type

    # properties
    name = Property()
    size = Property()
    md5sum = Property()
    sha1sum = Property()
    sha256sum = Property()
    sha512sum = Property()
    inode_type = Property()
    file_type = Property()
    mime_type = Property()
    # checksec prop
    checksec = Property()
    relro = Property()
    canary = Property()
    nx = Property()
    pie = Property()
    rpath = Property()
    runpath = Property()
    symtables = Property()
    fortify_source = Property()
    fortified = Property()
    fortifyable = Property()

    # relationships
    children = RelatedTo("GraphInode", "HAS_CHILD")
    owned_by = RelatedTo("OS", "OWNED_BY")


class SyscallTable(GraphObject):

    def __init__(self, index, name):
        super().__init__()
        self.index = index
        self.name = name

    # properties
    index = Property()
    name = Property()

    syscalls = RelatedTo("Syscall", "OWNS_SYSCALL")
    owned_by = RelatedTo("OS", "OWNED_BY")


class Syscall(GraphObject):

    def __init__(self, index, name, address):
        super().__init__()
        self.index = index
        self.name = name
        self.address = address

    # properties
    table = Property()
    index = Property()
    name = Property()
    address = Property()

    owned_by = RelatedTo("SyscallTable", "OWNED_BY")


class Process(GraphObject):

    def __init__(self, name, pid, ppid, thread_count,
                 handle_count, wow64):
        super().__init__()
        self.name = name
        self.pid = pid
        self.ppid = ppid
        self.thread_count = thread_count
        self.handle_count = handle_count
        self.wow64 = wow64

    # properties
    name = Property()
    pid = Property()
    ppid = Property()
    thread_count = Property()
    handle_count = Property()
    wow64 = Property()

    owned_by = RelatedTo("OS", "OWNED_BY")
