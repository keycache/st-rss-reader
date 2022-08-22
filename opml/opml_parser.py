import os

import listparser as lp
from listparser.common import SuperDict


def parse(file_obj: str) -> SuperDict:
    if os.path.exists(file_obj):
        with open(file=file_obj) as fh:
            return lp.parse(fh.read())
    else:
        return lp.parse(file_obj)
