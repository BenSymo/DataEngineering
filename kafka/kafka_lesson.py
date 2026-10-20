"""
Kafka Lesson: What it is, how to set it up, and how to use it.

Run this file to print the lesson:  python kafka_lesson.py
"""

LESSON = """
=====================================================================
1. WHAT IS APACHE KAFKA?
=====================================================================
Kafka is a tool for moving data between systems in real time.

One part of your system sends out events (messages). Other parts read
them as they arrive. Kafka sits in the middle and stores them.

Think of a post office with a very good filing system. Senders drop
messages into labelled mailboxes. Readers collect them whenever they
want. The messages stay stored, so new readers can go back and read
old ones too.

Why data engineers care:
  - Handles huge amounts of data with low delay.
  - Separates systems: the sender doesn't need to know who reads.
  - Messages are stored, so you can replay them if something breaks.
  - The usual way to feed live data into Spark, databases and lakes.

Kafka vs a database: a database holds the CURRENT state of things.
Kafka holds a LOG of everything that happened, in order.

=====================================================================
2. KEY WORDS
=====================================================================
EVENT       One piece of data (e.g. "user clicked buy").
            Also called a message or record.
TOPIC       A named category of events, like `orders`.
PRODUCER    An app that sends events to a topic.
CONSUMER    An app that reads events from a topic.
BROKER      A Kafka server that stores events. Many = a cluster.
PARTITION   A topic is split into parts to work in parallel.
            Order is kept inside one partition.
OFFSET      The position number of an event in a partition.
            A consumer uses it to remember where it got to.
GROUP       A consumer group shares the work of reading a topic.
            Each partition is read by one member of the group.
KEY         An optional label on an event. Events with the same
            key always go to the same partition (so stay in order).

=====================================================================
3. INSTALL (EASIEST WAY: DOCKER)
=====================================================================
This uses what you learned in the docker folder.

    docker run -d --name kafka -p 9092:9092 apache/kafka:latest

Check it is running:
    docker ps
    docker logs kafka

Kafka is now available at localhost:9092.

=====================================================================
4. TRY IT FROM THE COMMAND LINE
=====================================================================
The Kafka tools live inside the container.

Create a topic:
    docker exec kafka /opt/kafka/bin/kafka-topics.sh \\
      --bootstrap-server localhost:9092 \\
      --create --topic orders --partitions 3

List topics:
    docker exec kafka /opt/kafka/bin/kafka-topics.sh \\
      --bootstrap-server localhost:9092 --list

Send messages (type lines, press Ctrl+C to quit):
    docker exec -it kafka /opt/kafka/bin/kafka-console-producer.sh \\
      --bootstrap-server localhost:9092 --topic orders

Read messages, from the start (in a second terminal):
    docker exec -it kafka /opt/kafka/bin/kafka-console-consumer.sh \\
      --bootstrap-server localhost:9092 --topic orders --from-beginning

Type in the producer window and watch it appear in the consumer.

=====================================================================
5. USE KAFKA FROM PYTHON
=====================================================================
Install a client library:
    pip install confluent-kafka

Producer (producer.py):

    import json
    from confluent_kafka import Producer

    producer = Producer({"bootstrap.servers": "localhost:9092"})

    for i in range(5):
        event = {"order_id": i, "amount": 10 * i}
        producer.produce(
            "orders",
            key=str(i),
            value=json.dumps(event),
        )

    producer.flush()      # wait until all messages are sent

Consumer (consumer.py):

    import json
    from confluent_kafka import Consumer

    consumer = Consumer({
        "bootstrap.servers": "localhost:9092",
        "group.id": "order-readers",
        "auto.offset.reset": "earliest",   # start from the beginning
    })
    consumer.subscribe(["orders"])

    try:
        while True:
            msg = consumer.poll(1.0)       # wait up to 1 second
            if msg is None:
                continue
            if msg.error():
                print("Error:", msg.error())
                continue
            print(json.loads(msg.value()))
    finally:
        consumer.close()                   # always close cleanly

Run the consumer in one terminal, then run the producer in another.

=====================================================================
6. HOW IT SCALES
=====================================================================
  - A topic with 3 partitions can be read by up to 3 consumers in
    the same group at once, each taking different partitions.
  - Start a second copy of consumer.py with the same group.id and
    Kafka shares the partitions between the two.
  - Use a different group.id and that group gets its OWN full copy
    of every event.
  - Events are kept for a set time (7 days by default), whether or
    not anyone has read them.

=====================================================================
7. GOOD HABITS
=====================================================================
  - Pick a sensible key (e.g. customer_id) so related events stay
    in order.
  - Choose the partition count with care. You can add partitions
    later but not remove them.
  - Design consumers so handling the same event twice is safe
    (delivery can be repeated after a failure).
  - Keep events small and use a clear format like JSON (or Avro for
    larger projects).
  - Kafka moves data. Do heavy processing in other tools like Spark.

=====================================================================
8. PRACTICE EXERCISE
=====================================================================
  1. Start Kafka with Docker.
  2. Create a topic called `clicks` with 2 partitions.
  3. Send 5 messages with the console producer and read them back.
  4. Write producer.py to send 20 JSON events with a user_id key.
  5. Run two consumers in the same group. Which one gets which
     messages?
  6. Start a consumer with a new group.id and
     auto.offset.reset=earliest. Does it see the old events?
  7. Clean up:  docker stop kafka && docker rm kafka

Next steps: learn Kafka Connect (move data in and out of databases)
and Spark Structured Streaming (process Kafka data live).
"""


def main():
    print(LESSON)


if __name__ == "__main__":
    main()
