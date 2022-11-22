import voeventparse
import json
import argparse
from event import voevent

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", help="input VOEvent xml file name")
    parser.add_argument("groupid", help="TNS groupid")
    parser.add_argument("outfile", help="output json file name")
    args = parser.parse_args()


    ve = voevent.get_voevent(args.infile)
    dd = voevent.set_tns_dict(ve, args.groupid)
    voevent.write_tns(dd, args.outfile)
