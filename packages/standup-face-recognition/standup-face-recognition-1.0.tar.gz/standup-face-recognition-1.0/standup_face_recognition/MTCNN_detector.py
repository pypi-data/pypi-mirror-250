import cv2
import numpy as np
import torch
from facenet_pytorch import MTCNN
from utils import resize_images


class MTCNN_detector:
    def __init__(self):
        self.detector = MTCNN(thresholds=[0.6, 0.6, 0.6], keep_all=True, device='cuda').eval()
        self.results_list = []

    @staticmethod
    def _pre_processing_mtcnn(image):
        image = np.expand_dims(image, axis=0)
        image = np.float32(image)
        image = torch.from_numpy(image)
        image = image.to(torch.device("cuda"))
        return image

    def get_bbox_detection(self, image):
        input_img = self._pre_processing_mtcnn(image)
        faces, _, box, _, probs = self.detector(input_img)
        result_tuple = [faces, box, probs]
        return result_tuple

    @staticmethod
    def visualize_face_detection(frame, detected_faces):

        # Plot bounding boxes
        for index, faces in enumerate(detected_faces[1][0]):
            if faces is not None:
                # for face in faces[2][0]: # uncomment if all face boxes should be visualized
                face_x1, face_y1, face_x2, face_y2 = faces
                cv2.rectangle(frame, (round(face_x1), round(face_y1)), (round(face_x2), round(face_y2)), (0, 255, 0), 2)

            else:
                continue

        cv2.imwrite('/home/timo/face_recognition/webcam_images/' + 'detected_face_' + str(index) + '.png', frame)

