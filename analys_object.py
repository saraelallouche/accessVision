import re
import subprocess

# Define the yolo detect command
command = "yolo detect predict source='http://10.31.54.251:4747/video' model=yolov8n.pt"

# Run the command and capture its live output
process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, text=True)
pattern = r'(\d+)x(\d+) (\d+ [a-zA-Z]+)'

# Process the live output as it becomes available
for line in process.stdout:
    print(line.strip())
    match = re.search(pattern, line)
    if match:
        width, height, objects = match.groups()
        objects = objects.split(', ')
        print(f'{width}x{height}: {objects}')