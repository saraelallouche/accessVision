from ultralytics import YOLO

# Load a COCO-pretrained YOLOv8n model
model = YOLO('yolov8n.pt')

# Display model information (optional)
model.info()



# Run inference with the YOLOv8n model on the 'bus.jpg' image
results = model('images.jpeg')

