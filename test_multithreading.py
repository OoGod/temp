import threading
import time
from queue import Queue


def job(l,q):
    for i in range(len(l)):
        l[i] = l[i]**2
    print(l,threading.current_thread())
    print('cur{}'.format(threading.enumerate()))
    time.sleep(0.05)
    q.put(l)
    return l


if __name__ == '__main__':
    q = Queue()
    threads = []
    data = [[1,2,3],[3,4,5],[4,4,4],[5,5,5]]
    t = time.time()
    a = []
    for i in data:
        a.append(job(i,q))
    print(a,'and',time.time()-t)
    c = time.time()
    for i in range(len(data)):
        t1 = threading.Thread(target = job, args = [data[i],q],name = 'T{}'.format(i))
        t1.start()
        threads.append(t1)
    for i in threads:
        print(i,'aaaa')
        i.join()
    results = []
    for i in threads:
        print("===========================")
        print('current{}'.format(threading.enumerate()))
        results.append(q.get())

    print(results,'and',time.time()-c)