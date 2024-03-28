import subprocess
import time
import argparse

# Set up command line argument parsing
parser = argparse.ArgumentParser(description='Start MQTT publishers for various rooms.')
parser.add_argument('--terminal', action='store_true', help='Launch in separate terminals')
args = parser.parse_args()

# List of rooms in the building
rooms = ['lobby', 'office1', 'office2', 'conference_room']

# Launch a publisher.py process for each room
for room in rooms:
    if args.terminal:
        # Launch in a new terminal window
        subprocess.Popen(['gnome-terminal', '--', 'python', 'publisher.py', room])
    else:
        # Launch in the background
        subprocess.Popen(['python', 'publisher.py', room])
    
    # Wait for 0.1 seconds before launching the next one
    time.sleep(0.1)