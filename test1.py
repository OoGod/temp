def fib(max):
    n,a,b = 0,0,1
    while n<max:
        yield b
        a,b = b,a+b
        n = n + 1


import time

def A():
    while True:
        print('----A----')
        yield
        time.sleep(0.5)

def B(c):
    print('----B----')
    c.__next__()
    time.sleep(0.5)

if __name__ == '__main__':
    a = A()
    print(a.__next__())
    B(a)