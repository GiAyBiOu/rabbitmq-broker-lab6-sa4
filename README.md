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
- **RabbitMQ** installed and running locally on your machine (`localhost:5672`).

### Installation

#### On Windows / Linux / macOS
1. Open your terminal or command prompt.
2. Create and activate a Virtual Environment (**Recommended**):
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # Linux / macOS
   python3 -m venv venv
   source venv/bin/activate
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

### Expected Behavior
- The **Producer** continuously generates JSON objects containing traffic data (e.g., location, speed, vehicle plate, name, weather) and pushes them to the `traffic-events-queue`.
- The **Consumer** immediately retrieves messages from the queue, returning the consumed JSON details, displaying an acknowledgment message, and showing that it is continuously waiting for new items.
- If you stop the **Consumer** but leave the **Producer** running, the messages will wait safely in the queue. They will be processed once the Consumer is restarted.
- Press `CTRL + C` in either terminal window to safely stop the process.
