import socketio
import time
import sys

sio = socketio.Client()

connected = False
messages_received = []

@sio.event
def connect():
    global connected
    connected = True
    print("Connected to Socket.io server")

@sio.event
def disconnect():
    print("Disconnected from Socket.io server")

@sio.event
def connected(data):
    print(f"Received connected event: {data}")
    messages_received.append('connected')

@sio.event
def waiting_for_opponent():
    print("Waiting for opponent...")
    messages_received.append('waiting')

@sio.event
def battle_start(data):
    print(f"Battle started: {data}")
    messages_received.append('battle_start')

@sio.event
def game_state(data):
    print(f"Game state update: {data}")
    messages_received.append('game_state')

def test_socket_connection():
    print("\n=== Testing Socket.io Connection ===\n")
    
    try:
        print("Connecting to ws://localhost:8000...")
        sio.connect('http://localhost:8000', socketio_path='/socket.io')
        
        time.sleep(1)
        
        if not connected:
            print("FAIL: Did not connect")
            return False
        
        print("  PASS: Connected successfully")
        
        test_data = {
            'battle_id': 'test_123',
            'user_id': 1,
            'team': [
                {'id': 1, 'hp': 220, 'name': 'Jibanyan'},
                {'id': 2, 'hp': 200, 'name': 'Whisper'},
                {'id': 3, 'hp': 240, 'name': 'Komasan'}
            ]
        }
        
        print("\nEmitting join_battle event...")
        sio.emit('join_battle', test_data)
        
        time.sleep(1)
        
        sio.disconnect()
        
        print("\n  PASS: Socket.io test complete")
        print(f"  Received {len(messages_received)} messages")
        
        return True
        
    except Exception as e:
        print(f"\n  FAIL: {e}")
        return False

if __name__ == "__main__":
    success = test_socket_connection()
    sys.exit(0 if success else 1)
