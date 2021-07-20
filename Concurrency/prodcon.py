import threading
from threading import Semaphore
import time
import random

MAX_SERVED = 3
TOTAL_CLIENTS = 5;

currentclients = 0;

# flags
chairLock = Semaphore(1)
clientReady = Semaphore(0)
serverReady = Semaphore(0)
clientDone = Semaphore(0)
serverDone = Semaphore(0)

# server thread
def Server(threadName):
    global currentclients

    time.sleep(random.uniform(0, 0.5))
    print(threadName + "-> power on")
    while (True):
        clientReady.acquire()
        print(threadName + "-> queue client")
        serverReady.release()

        # serving
        time.sleep(random.uniform(0, 2.5))
        print(threadName + "-> serving")

        # serving done
        clientDone.acquire()
        serverDone.release()
        print(threadName + "-> client served\n")


# client thread
def Client(threadName):
    global currentclients

    time.sleep(random.uniform(0, 6.0))
    while (True):
        # try entering queue
        chairLock.acquire()
        # leave if queue is full
        if currentclients == MAX_SERVED:
            print(threadName + "-> enter [WAIT: " + str(currentclients) + " clients in queue] [FULL; LEAVE]")
            chairLock.release()
            break
        print(threadName + "-> enter [WAIT: " + str(currentclients) + " clients in queue] [JOIN QUEUE]")
        currentclients += 1
        chairLock.release()

        # notify server
        clientReady.release()
        serverReady.acquire()

        # enter queue
        print(threadName + "-> queued\n")
        time.sleep(random.uniform(0, 2.5))

        # tell server we are done and wait for the server to confirm
        clientDone.release()
        serverDone.acquire()

        # leave queue
        chairLock.acquire()
        currentclients -= 1
        chairLock.release()

        print(threadName + "-> exit\n\n")
        break


startTime = time.perf_counter_ns() / 1000000

# make and start server and client threads
server = threading.Thread(target=Server, args=("server",))
server.start()

clients = []
for i in range(0, TOTAL_CLIENTS):
    clients.append(threading.Thread(target=Client, args=("client" + str((i + 1)),)))
    clients[i].start()

for i in range(0, TOTAL_CLIENTS):
    clients[i].join()

print("Client - server done. Runtime: " + str(int((time.perf_counter_ns() / 1000000) - startTime)) + "ms")