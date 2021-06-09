from log_entry import LogEntry

class SvnDir():
    def __init__(self, system, name):
        pass

    def get_first_commit(self):
        pass

    def json(self):
        pass

class Release(SvnDir):
    def __init__(self, system, name):
        self.super().__init__(self)
        self.ops_version = False

    def check_ops(self):
        pass


