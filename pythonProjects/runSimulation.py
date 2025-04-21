import signAtzuma
import threading


def main():
    threads = []

    for i in range(3):
        threads.append(threading.Thread(target=signAtzuma.main, daemon=True))

    for i in range(3):
        threads[i].start()

    for i in range(3):
        threads[i].join()



if __name__ == "__main__":
    main()
