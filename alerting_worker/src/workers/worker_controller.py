import time

def main():
    print("Worker started...")
    while True:
        print("Working...")
        time.sleep(5)  

if __name__ == "__main__":
    main()