import torch
from classification_dataset import classification_dataset
from Classification_model import Classification_model
import classification_helpers
from torchvision import transforms

class classify():

    def __init__(self, checkpoint_path = '/'):
        if torch.cuda.is_available():
            self.model = Classification_model(2).cuda()
        else:
            self.model = Classification_model(2)
        self.model = classification_helpers.load_model(self.model, checkpoint_path)
        self.model.eval()
        mean = [0.485, 0.456, 0.406]
        std = [0.229, 0.224, 0.225]
        IMG_WIDTH = 112
        IMG_HEIGHT = 112

        self.transform = transforms.Compose([
            transforms.ToPILImage(),
            transforms.Resize((IMG_WIDTH, IMG_HEIGHT)),
            transforms.ToTensor(),
            transforms.Normalize(mean, std)
        ])

    def get_prediction(self, video_path, sequence_length = 60, crop_face = False):

        dataset = classification_dataset(video_path, sequence_length = 60, transform = self.transform, crop_face = crop_face)
        pred = classification_helpers.predict(self.model, dataset[0])
        print(pred)
        return pred