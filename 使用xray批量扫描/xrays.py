import os
import hashlib
import re


def get_url():
    f = open("targets.txt")
    lines = f.readlines()
    pattern = re.compile(r'^(https|http)://')
    for line in lines:
        try:
            if not pattern.match(line.strip()):
                targeturl="http://"+line.strip()
            else:
                targeturl=line.strip()
            # print(targeturl.strip())
            outputfilename=hashlib.md5(targeturl.encode("utf-8"))
            do_scan(targeturl.strip(), outputfilename.hexdigest())
        except Exception as e:
            print(e)
            pass
    f.close()
    print("Xray Scan End")
    return


def do_scan(targeturl,outputfilename="test"):
    scan_command="/home/kali/Desktop/xray/xray_linux_386 webscan --basic-crawler {} --html-output {}.html".format(targeturl,outputfilename)
    # scan_command = "ping 943ogg.dnslog.cn"
    # print(scan_command)
    os.system(scan_command)
    return

if __name__ == '__main__':
    get_url()
