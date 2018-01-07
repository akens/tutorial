from multiprocessing import Process

import time
from scrapy import cmdline

def run_cmd(idx):
    process_idx = str(idx)
    cmdline.execute(("scrapy crawl tutorial -s JOBDIR=jobdir"+process_idx+" -a process_idx="+process_idx).split())


if __name__ == "__main__":
    process_list = []
    for i in range(22):
       process = Process(target=run_cmd,args=(i,))
       process_list.append(process)
       process.start()
    e = process_list.__len__()
    while True:
        for th in process_list:
            if not th.is_alive():
                e -= 1
        if e <= 0:
            break
        time.sleep(1)