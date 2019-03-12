from time import sleep
from src.producer import Producer

producer = Producer('plaintext-input')


# //TODO: this is just to test the topic, remove this file later.
def main():
    print('started producer')
    producer.send_message('test message')

    for e in range(10):
        producer.send_message(e)
        sleep(5)


if __name__ == "__main__":
    main()


