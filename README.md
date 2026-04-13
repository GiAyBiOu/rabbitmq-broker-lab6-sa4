# RabbitMQ Traffic Broker Lab

Welcome to the RabbitMQ Traffic Event Broker project! This application demonstrates a Producer-Consumer message queue architecture where random vehicle traffic events are sent into a local RabbitMQ queue and consumed by processing instances in real-time. 

## Author 
**Gabriel Mendoza**  
**Course:** Software Architecture 4 - Lab 6

---

## Quick Start

This application uses a local RabbitMQ instance (`localhost`) by default. *(Cloud queue credentials are securely commented out in the code repository).*

### Prerequisites

- **Python 3.8+**
- **Docker & Docker Compose** (to easily run the RabbitMQ broker) or a manual RabbitMQ installation.

### Starting the Broker (Docker)

```bash
docker-compose up -d
```
*(The management UI will be available at http://localhost:15672 with credentials: guest/guest)*

### Installation (Python Scripts)


#### On Windows / Linux / macOS
1. Open your terminal or command prompt.
2. Create and activate a Virtual Environment (**Recommended**):
   ```bash
   # Linux / macOS
   python3 -m venv venv
   source venv/bin/activate

   # Windows
   .\venv\Scripts\Activate.ps1
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   *(If the file is missing, you can manually run `pip install pika`)*

---

## Running the Application

To observe the real-time processing and queue behavior, it is highly recommended to open **two separate terminal windows**.

### Step 1: Start the Consumer
In the **first terminal**, start listening for incoming traffic events:
```bash
# Windows
python consumer.py

# Linux / Mac
python3 consumer.py
```
> You will see the consumer start and display that it is "Waiting for messages...". It will continue to run until it is stopped.

### Step 2: Start the Producer
In the **second terminal**, run the producer to start generating and publishing vehicle/traffic data:
```bash
# Windows
python producer.py

# Linux / Mac
python3 producer.py
```

---

## Experiments and Observation

This broker is set up specifically to allow you to test RabbitMQ's distribution and queuing logic.

### 1. Consumer Distribution (Round Robin)
To observe how messages are distributed among multiple workers:
1. Open **three** separate terminals.
2. In the first and second terminal, run `python consumer.py`. (You now have TWO consumers listening).
3. In the third terminal, run `python producer.py` to start spamming messages.
4. Watch the two consumer terminals. You will notice that RabbitMQ automatically distributes the messages evenly between Consumer A and Consumer B, preventing either from doing all the work.

### 2. Queue Accumulation and Retention
To observe how messages wait in the queue when no one is listening:
1. Run `python producer.py` and let it generate and send it.
2. Stop the **Producer**
3. Keep the **Consumer** closed / terminated completely. The messages are now patiently waiting inside the `gm_lab6` queue.
4. Run `python consumer.py` to start the consumer.
5. You will see the consumer instantly "catch up" and process all the accumulated messages back-to-back until the queue is empty.
