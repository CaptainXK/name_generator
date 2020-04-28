#! /usr/bin/python3
import sys, getopt, os
import re

class Duplicate_Removal:
    m_rule_set=None
    m_cnt=0

    def __init__(self):
        self.m_rule_set = set()
        self.cnt=0
    
    def is_dup(self, _rule):
        return ( _rule in self.m_rule_set)
    
    def add_rec(self, _rule):
        self.m_rule_set.add(_rule)
    
    def inc_dup(self):
        self.m_cnt += 1
    
    def dump_dup(self):
        return self.m_cnt

def is_valid_str(_str):
    ret = True

    for item in _str:
        if ord(item) < 0 or ord(item) > 127:
            ret = False
            break
    
    return ret

def is_dup_str(_dr, _str):
    ret = True

    if _dr.is_dup(_str):
        # duplicated rule detected
        ret = True
        _dr.inc_dup()
    else:
        ret = False
        _dr.add_rec(_str)
    
    return ret

def create_rule_file(_src):
    cnt = 0
    dr = Duplicate_Removal()

    with open(_src, 'r') as fin:
        with open("./data/rule.csv", 'w') as fout:
            lines = fin.readlines()
            for line in lines:
                items = line.split(" ")
                raw_str = items[1]
                match_obj = re.search(r'"Top(.*)"', raw_str, re.I)
                if match_obj:
                    raw_name = match_obj.group(1)
                    if is_valid_str(raw_name) and not is_dup_str(dr, raw_name):
                        fout.write(raw_name + " 1")
                        fout.write("\n")
                        cnt += 1
    
    print("{} duplicated rules had beed ignored".format(dr.dump_dup()))

def show_usage():
    print("Usage:")
    print("\t-h : show usage")
    print("\t-s : path of raw file")

def cmd_parse(argv):
    if len(argv) == 0:
        print("[no cmd detected!]")
        show_usage()
        sys.exit()

    try:
        opts, args = getopt.getopt(argv, "hs:")
    except getopt.GetoptError as err:
        print("[%s]"%(str(err)))
        show_usage()
        sys.exit()

    for opt, arg in opts:
        if opt == '-h':
            show_usage()
            sys.exit()
        elif opt == '-s':
            src_file = str(arg)
            create_rule_file(src_file)
        else:
            print("error option!")
            sys.exit()

def __main__():
    cmd_parse(sys.argv[1:])

# start here
__main__()


        

