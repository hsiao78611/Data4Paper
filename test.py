import multiprocessing as mp

def crawler(x):
    print('test' + str(x))

    def _p(s):
        print(s)

    crawler.qr.put(_p('Doing: ' + str(x)))

def worker(queue):
    crawler.qr = queue


jobs = range(1, 6)

try:
    the_q = mp.Queue()
    p = mp.Pool(4, worker, [the_q])
    p.imap(crawler, jobs)
    p.close()

    for i in range(len(jobs)):
        print(str(i))
        the_q.get()
        #     print(the_q.get())
except Exception as e:
    print(e)