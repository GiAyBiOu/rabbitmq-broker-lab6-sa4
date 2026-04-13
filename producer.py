import pika
import json
import random
import time
from datetime import datetime

def create_connection():

    credentials = pika.PlainCredentials('guest', 'guest')
    parameters = pika.ConnectionParameters(
        host='localhost',
        port=5672,
        credentials=credentials
    )
    # credentials = pika.PlainCredentials('', '')
    # parameters = pika.ConnectionParameters(
    #     host='34.30.170.15',
    #     port=5672,
    #     credentials=credentials
    # )
    return pika.BlockingConnection(parameters)

def declare_queue(channel):
    channel.queue_declare(queue='traffic-events-queue', durable=True)

def generate_traffic_event():
    locations = [
        'Downtown', 'Highway 101', 'Airport Road',
        'Central Avenue', 'West Bridge', 'East Pass'
    ]
    
    vehicles = ['ABC-1234', 'XYZ-5678', 'DEF-9012', 'GHI-3456', 'JKL-7890']
    
    location = random.choice(locations)
    vehicle_plate = random.choice(vehicles)
    speed = random.randint(20, 120)
    speed_limit = 60
    weather = random.choice(['clear', 'rain', 'snow'])
    
    event = {
        'timestamp': datetime.now().isoformat(),
        'name': 'Gabriel Mendoza',
        'location': location,
        'vehicle_plate': vehicle_plate,
        'current_speed': speed,
        'speed_limit': speed_limit,
        'violation': speed > speed_limit,
        'weather': weather,
        'volume': random.randint(100, 500)
    }
    
    return event

def main():
    connection = create_connection()
    channel = connection.channel()
    
    declare_queue(channel)
    
    print("[*] Producer Started")
    print("[*] Generating and sending traffic events...")
    
    try:
        # Previously, when using the Cloud connection, we only sent
        # one message to avoid spamming the remote server unnecessarily:
        #
        # message = {
        #     "nombre": "Gabriel Mendoza",
        #     "materia": "SA 4"
        # }
        # channel.basic_publish(
        #     exchange='',
        #     routing_key='sa4-queue',
        #     body=json.dumps(message),
        #     properties=pika.BasicProperties(
        #         delivery_mode=2,
        #         content_type='application/json'
        #     )
        # )
        # Now, to simulate queue accumulation and consumer distribution, 
        # we spam multiple messages locally using a loop.
        while True:
            event = generate_traffic_event()
            
            channel.basic_publish(
                exchange='',
                routing_key='traffic-events-queue',
                body=json.dumps(event),
                properties=pika.BasicProperties(
                    delivery_mode=2, # make message persistent
                    content_type='application/json'
                )
            )
            
            print(f"\n[✓] Message sent successfully to 'traffic-events-queue':")
            print(json.dumps(event, indent=2))
            
            # Sleep to simulate interval between events
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\n[!] Producer stopped by user.")
    finally:
        if connection.is_open:
            connection.close()

if __name__ == '__main__':
    main()
