import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import Float32
from cv_bridge import CvBridge
from ultralytics import YOLO
import cv2

class ObjectTracker(Node):
    def __init__(self):
        super().__init__('object_tracker')
        
        # 1. Load your newly built GPU engine
        self.model = YOLO("/home/aden/yolov8s.engine", task="detect")
        
        # 2. ROS setup
        self.subscription = self.create_subscription(Image, '/image_raw', self.listener_callback, 10)
        self.publisher_ = self.create_publisher(Float32, '/target_offset', 10)
        self.bridge = CvBridge()
        
        self.target_class = 'person' # Change this to what you want to track
        self.get_logger().info('Tracker Node Started. Looking for: ' + self.target_class)

    def listener_callback(self, data):
        # Convert ROS image to OpenCV
        frame = self.bridge.imgmsg_to_cv2(data, 'bgr8')
        img_center_x = frame.shape[1] / 2
        
        # Run inference on GPU (device=0)
        results = self.model.predict(frame, device=0, verbose=False, conf=0.5)

        # --- VISUALIZATION LOGIC ---
        # annotated_frame will have all bounding boxes and labels drawn on it
        annotated_frame = results[0].plot()
        
        # Draw a blue vertical line to show the center of the camera
        #cv2.line(annotated_frame, (int(img_center_x), 0), (int(img_center_x), frame.shape[0]), (255, 0, 0), 2)
        
        # Pop up the window
        #cv2.imshow("YOLOv8 Orin Nano Tracking", annotated_frame)
        #cv2.waitKey(1) 
        # ---------------------------

        for r in results:
            for box in r.boxes:
                cls_id = int(box.cls[0])
                label = self.model.names[cls_id]
                
                if label == self.target_class:
                    x1, y1, x2, y2 = box.xyxy[0]
                    obj_center_x = (x1 + x2) / 2
                    
                    offset = obj_center_x - img_center_x
                    
                    msg = Float32()
                    msg.data = float(offset)
                    self.publisher_.publish(msg)
                    
                    self.get_logger().info(f'Target Found! Offset: {offset:.2f}')
                    return 

def main(args=None):
    rclpy.init(args=args)
    node = ObjectTracker()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        # Clean up windows when shutting down
        cv2.destroyAllWindows()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()