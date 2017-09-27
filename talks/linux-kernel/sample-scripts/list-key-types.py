#!/usr/bin/env python2.7

import r2pipe


def get_field(struct, field):
    for item in struct["members"]:
        if item["name"] == field:
            return item
    return None

def get_addr(symbol):
    r2.cmd("s %s" % symbol)
    offset = r2.cmd("s")
    r2.cmd("s-")
    return int(offset, 16)

class list:
    def __init__(self, head, type, field, debug=0):
        self.list_type = r2.cmdj("idddj list_head")
        self.current = int(r2.cmd("iddv list_head.next @ %s" % head), 16)
        self.head = get_addr(head)
        self.type = r2.cmdj("idddj %s" % type)
        self.type_name = type
        self.offset = get_field(self.type, field)["offset"]
        self.debug = debug

    def __iter__(self):
        return self

    def next(self): # Python 3: def __next__(self)
        if self.debug == 1:
            print(" - head: %d - current: %d" % (self.head, int(self.current)))

        if (int(self.current) == self.head):
            raise StopIteration
        else:
            new_offset = self.current - self.offset
            res = r2.cmdj("iddvj %s @ %d" % (self.type_name, new_offset))
            cmd = "iddv list_head.next @ %d" % self.current
            self.current = int(r2.cmd(cmd), 16)
            return res


r2 = r2pipe.open();


for i in list("sym.key_types_list", "key_type", "link"):
    print r2.cmd("ps @ %s" % i["name"])
    #print i

