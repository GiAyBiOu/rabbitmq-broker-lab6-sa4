import pika
import json
import sys
from datetime import datetime

def create_connection():
    # Only one set of parameters can be used at a time.
    # Cloud variables are commented out so they don't overwrite the local ones.
    credentials = pika.PlainCredentials('guest', 'guest')
    parameters = pika.ConnectionParameters(
        host='localhost',
        port=5672,
        credentials=credentials
    )
    # credentials = pika.PlainCredentials('alumno1', 'alumno1')
    # parameters = pika.ConnectionParameters(
    #     host='34.30.170.15',
    #     port=5672,
    #     credentials=credentials
    # )
    return pika.BlockingConnection(parameters)

def process_message(event):
    return json.dumps(event, indent=2)

def callback(ch, method, properties, body):
    print(f"\n[*] Received new message...")
    try:
        event = json.loads(body)
        
        message_info = process_message(event)
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Consumed Event Data:")
        print(message_info)
        print(f"[✓] Successfully processed event for vehicle: {event.get('vehicle_plate', 'Unknown')} (Driver: {event.get('name', 'Unknown')})")
        
        # Acknowledge the message was processed
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print("[*] Waiting for new messages in the queue...")
        
    except json.JSONDecodeError:
        print("[!] Error decoding message. Invalid JSON format.")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
    except Exception as e:
        print(f"[!] Error processing message: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

def main():
    connection = create_connection()
    channel = connection.channel()
    
    channel.queue_declare(queue='traffic-events-queue', durable=True)
    
    channel.basic_qos(prefetch_count=1)
    
    channel.basic_consume(
        queue='traffic-events-queue',
        on_message_callback=callback,
        auto_ack=False
    )
    
    print("[*] Consumer Started")
    print("[*] Listening and waiting for messages on 'traffic-events-queue'...")
        
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("\n[!] Consumer stopped by user.")
        channel.stop_consuming()
    finally:
        if connection.is_open:
            connection.close()

if __name__ == '__main__':
    main()
