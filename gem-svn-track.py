#!/usr/bin/env python3

import re
import subprocess as sp
from database import Database

SVN_SERVER = 'http://sbfsvn02/gemini-sw/'

def exec_svn_cmd(cmd):
    svn_cmd = sp.run([cmd], shell=True, stdout=sp.PIPE,
                     stderr=sp.PIPE, encoding='utf-8')
    if svn_cmd.stderr:
        print(svn_cmd.stderr)
        return []
    return [l.strip() for l in svn_cmd.stdout.split('\n') if l]

def header_parser(entry_header, entry_d):
    l_cont = [i.strip() for i in entry_header.split('|')]
    entry_d['rev'] = l_cont[0]
    entry_d['user'] = l_cont[1]
    entry_d['date'] = l_cont[2]
    return entry_d


def log_verbose_parser(cmd_output):
    iter_out = iter(cmd_output)
    next(iter_out)
    entry_dict = {}
    entry_list = []
    changes_list = []
    for l in iter_out:
        if re.search(r'^--+-$', l):
            entry_dict['changes'] = changes_list[:-1]
            entry_dict['comment'] = changes_list[-1]
            entry_list.append(entry_dict)
            changes_list = []
            entry_dict = {}
            continue
        if re.search(r'^r[1-9]', l):
            entry_dict = header_parser(l, entry_dict)
            next(iter_out)
            continue
        changes_list.append(l)
    return entry_list

if __name__ == '__main__':
    Database.initialize()
    # base_cmd = 'svn log --stop-on-copy --verbose '
    base_cmd = 'svn log --stop-on-copy '
    branch = 'http://sbfsvn02/gemini-sw/gem/branches/ioc/tcs/cp/nfs_dbg'
    cmd = base_cmd + branch
    cmd_out = exec_svn_cmd(cmd)
    entries = log_parser(cmd_out)
    # for e in entries:
        # print(e)
    print(entries[-1])
    for e in entries:
        Database.insert('entries',e)
    all_entries = Database.find('entries',{})
    print(all_entries[0])
