import re
import subprocess as sp
from database import Database


class LogEntry():
    SVN_SERVER = 'http://sbfsvn02/gemini-sw/'

    def __init__(self, svn_dir):
        self.svn_dir = svn_dir
        self.all_entries = []
        self.last_entry = []

    def log_stop_copy(self):
        cmd_soc = 'svn log --stop-on-copy --verbose '
        all_entries_raw = self.exec_svn_cmd(self.SVN_SERVER,
                                            self.svn_dir, cmd_soc)
        rev_entries = reversed(all_entries_raw)
        # Ignore first line of "-"
        next(rev_entries)
        for l in rev_entries:
            # svn log entries end with a line of "-"
            if re.search(r'^--+-$', l):
                break
            self.last_entry.insert(0,l)

    def all_logs_soc(self):
        cmd_asoc = 'svn log --stop-on-copy '
        all_entries_raw = self._exec_svn_cmd(cmd_asoc)
        entries = iter(all_entries_raw)
        next(entries)
        aux_entry = []
        for l in all_entries_raw:
            # svn log entries end with a line of "-"
            # use this fact to separate entries
            if re.search(r'^--+-$', l):
                self.all_entries.append(aux_entry)
                aux_entry = []
                continue
            aux_entry.append(l)

    @staticmethod
    def header_parser(entry_header, entry_d):
        l_cont = [i.strip() for i in entry_header.split('|')]
        entry_d['rev'] = l_cont[0]
        entry_d['user'] = l_cont[1]
        entry_d['date'] = l_cont[2]
        return entry_d

    @staticmethod
    def exec_svn_cmd(server, directory, cmd):
        branch = server + directory
        # Neato way to catch output from commands. Pysvn is kinda crappy
        svn_cmd = sp.run([cmd+branch], shell=True, stdout=sp.PIPE,
                        stderr=sp.PIPE, encoding='utf-8')
        if svn_cmd.stderr:
            print(svn_cmd.stderr)
            return []
        # Trim the fat (blank lines and leading and trailing spaces)
        return [l.strip() for l in svn_cmd.stdout.split('\n') if l]

if __name__ == '__main__':
    area = 'gem/release/'
    cb_type = 'ioc/'
    system = 'tcs/cp/'
    releases = {}

    branch = area + cb_type + system

    cmd = 'svn list '

    release_list = LogEntry.exec_svn_cmd(LogEntry.SVN_SERVER, branch, cmd)

    print(release_list)

    for r in release_list:
        rel_dir = branch + r
        releases[r] = LogEntry(rel_dir)
        releases[r].log_stop_copy()
        print(releases[r].last_entry)


