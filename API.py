import asyncio
import websockets
import pymysql
import json
from pymysql.cursors import DictCursor
from datetime import datetime

# Set to store connected WebSocket clients
connected_clients = set()

# Configuration for connecting to the MySQL database
sqlconfig = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'pranit@69',  # Replace with your actual MySQL password
    'db': 'hms',  # Database name
    'cursorclass': DictCursor  # Use DictCursor to get query results as dictionaries
}

# Function to establish a new database connection
def get_connection():
    return pymysql.connect(**sqlconfig)

# Helper function to convert datetime objects to string
def convert_datetime_to_string(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = value.isoformat()
            elif isinstance(value, (dict, list)):
                convert_datetime_to_string(value)
    elif isinstance(data, list):
        for item in data:
            convert_datetime_to_string(item)
    return data

# Asynchronously notify all connected WebSocket clients with a message
async def notify_clients(message):
    if connected_clients:
        print(f"Notifying clients: {message}")
        await asyncio.gather(*(client.send(message) for client in connected_clients))
    else:
        print("No connected clients to notify.")

# Asynchronously fetch the last 10 entries from the 'workers' table in the database
async def fetch_last_10_entries(connection):
    with connection.cursor() as cursor:
        cursor.execute("SELECT SrNo, ID, Name, Symptoms, created_at FROM workers ORDER BY SrNo DESC LIMIT 10")
        result = cursor.fetchall()
        result = convert_datetime_to_string(result)
        print(f"Fetched last 10 entries: {result}")  # Debug: Print fetched data
        return result

# Asynchronously monitor the 'workers' table for new entries, updates, and deletions
async def monitor_database():
    last_srno = None
    last_snapshot = []

    while True:
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT SrNo FROM workers ORDER BY SrNo DESC LIMIT 1")
                result = cursor.fetchone()

                if result and (last_srno is None or result['SrNo'] > last_srno):
                    last_srno = result['SrNo']
                    
                    cursor.execute("SELECT * FROM workers WHERE SrNo = %s", (last_srno,))
                    new_entry = cursor.fetchone()
                    new_entry = convert_datetime_to_string(new_entry)
                    print(f"New entry detected: {new_entry}")
                    await notify_clients(json.dumps({
                        'type': 'INSERT',
                        'data': new_entry,
                        'timestamp': new_entry.get('created_at', 'No timestamp')
                    }))
                    
                    last_10_entries = await fetch_last_10_entries(connection)
                    await notify_clients(json.dumps({'type': 'LAST_10', 'data': last_10_entries}))

                cursor.execute("SELECT * FROM workers ORDER BY SrNo ASC")
                current_snapshot = cursor.fetchall()
                current_snapshot = convert_datetime_to_string(current_snapshot)

                last_snapshot_dict = {entry['SrNo']: entry for entry in last_snapshot}
                current_snapshot_dict = {entry['SrNo']: entry for entry in current_snapshot}

                # Detect deletions
                for srno, old_entry in last_snapshot_dict.items():
                    if srno not in current_snapshot_dict:
                        print(f"Deletion detected for SrNo: {srno}. Deleted Data: {old_entry}")
                        await notify_clients(json.dumps({
                            'type': 'DELETE',
                            'data': old_entry,
                            'query': f"DELETE FROM workers WHERE SrNo = {srno};",
                            'timestamp': old_entry.get('created_at', 'No timestamp')
                        }))

                # Detect updates
                for srno, new_entry in current_snapshot_dict.items():
                    if srno in last_snapshot_dict:
                        old_entry = last_snapshot_dict[srno]
                        if old_entry != new_entry:
                            print(f"Update detected for SrNo: {srno}. Old Data: {old_entry}. New Data: {new_entry}")
                            update_query = (
                                f"UPDATE workers SET "
                                f"ID = '{new_entry['ID']}', "
                                f"Name = '{new_entry['Name']}', "
                                f"Symptoms = '{new_entry['Symptoms']}' "
                                f"WHERE SrNo = {srno};"
                            )
                            await notify_clients(json.dumps({
                                'type': 'UPDATE',
                                'data': {
                                    'old': old_entry,
                                    'new': new_entry,
                                    'query': update_query
                                },
                                'timestamp': new_entry.get('created_at', 'No timestamp')
                            }))
                            
                last_snapshot = current_snapshot

        finally:
            connection.close()

        await asyncio.sleep(1)

# Handler for managing WebSocket connections
async def handler(websocket, path):
    connected_clients.add(websocket)
    print(f"New client connected: {websocket.remote_address}")
    try:
        connection = get_connection()
        try:
            last_10_entries = await fetch_last_10_entries(connection)
            await websocket.send(json.dumps({'type': 'LAST_10', 'data': last_10_entries}))
        finally:
            connection.close()

        await websocket.wait_closed()
    finally:
        print(f"Client disconnected: {websocket.remote_address}")
        connected_clients.remove(websocket)

# Main function to start the WebSocket server and database monitor
async def main():
    print("Starting WebSocket server...")
    server = await websockets.serve(handler, 'localhost', 9870)
    print("WebSocket server started. Monitoring database...")
    await asyncio.gather(monitor_database(), server.wait_closed())

if __name__ == "__main__":
    asyncio.run(main())







