# gdb --ex "target remote localhost:1234" -x script.py --ex "break *0x7ee92c5"
# When the breakpoint hits, just enter 'dumper' in the gdb prompt

import os
import gdb

class Dumper(gdb.Command):

    def __init__(self):
        super(Dumper, self).__init__("dumper", gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):
        for page in range(0, 0xffffffff, 0x1000):

            if page % 2**20 == 0:
               print(hex(page))

            try:
                mem = gdb.inferiors()[0].read_memory(page, 0x1000).tobytes()
            except gdb.MemoryError:
                continue
            if set(mem) == set([0]):
                continue

            if set(mem) == set([0xff]):
                continue

            with open("/tmp/dumps/page.0x%x" % page, 'wb') as f:
                f.write(mem)

Dumper()
