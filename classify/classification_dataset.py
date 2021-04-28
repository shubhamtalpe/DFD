import cv2
import torch
import numpy as np
import face_recognition
from torch.utils.data.dataset import Dataset

class classification_dataset(Dataset):
    
    def __init__(self, video_names, sequence_length = 60, transform = None, crop_face = False):
        self.video_names = video_names
        self.transform = transform
        self.count = sequence_length
        self.crop_face = crop_face
    
    def __len__(self):
        return len(self.video_names)
    
    def __getitem__(self,idx):
        video_path = self.video_names
        frames = [] 
        for i,frame in enumerate(self.frame_extract(video_path)):
            if self.crop_face:
                frame = self.extract_face(frame)
            frames.append(self.transform(frame))
            if(len(frames) == self.count):
                break
        
        frames = torch.stack(frames)
        frames = frames[:self.count]
        return frames.unsqueeze(0)
    
    def frame_extract(self,path):
      vidObj = cv2.VideoCapture(path) 
      success = 1
      while success:
          success, image = vidObj.read()
          if success:
              yield image

    def extract_face(self, frame):
        faces = face_recognition.face_locations(frame)
        try:
            top, right, bottom, left = faces[0]
            frame = frame[top:bottom, left:right, :]
        except:
            pass
        return frame