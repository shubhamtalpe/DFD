import os
import cv2
import torch
from torch.utils.data.dataset import Dataset

## Class to handle dataset
class video_dataset(Dataset):

    def __init__(self, file_paths, labels, sequence_length = 60, transform = None):
        self.file_paths = file_paths
        self.labels = labels
        self.transform = transform
        self.sequence_length = sequence_length

    def __len__(self):
        return len(self.file_paths)

    def __getitem__(self, idx):
        f_path = self.file_paths[idx]
        frames = []     
        
        # for i in self.labels:
        #     if os.path.samefile(i[0], f_path):
        #         label = i[1]
        #         break

        temp_vid = os.path.basename(f_path)
        try:
            label = (self.labels.loc[self.labels['file'] == temp_vid]).label.item()
        except:
            print(temp_vid)
            print(self.labels.loc[self.labels['file'] == temp_vid])
        
        
        if label == 'FAKE':
            label = 0
        else:
            label = 1

        for i, frame in enumerate(self.get_frame(f_path, self.sequence_length)):
            frames.append(frame)
        
        frames = torch.stack(frames)

        return frames, label

    def get_frame(self, f_path, sequence_length):
        video_reader = cv2.VideoCapture(f_path)
        ret = 1
        
        while ret and sequence_length:
            ret, frame = video_reader.read()
            if ret:
                sequence_length -= 1
                yield torch.FloatTensor(frame)
        
        video_reader.release()