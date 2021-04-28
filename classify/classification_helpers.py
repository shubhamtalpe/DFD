import sys
import torch
from torch import nn

def predict(model, img):
    
    sm = nn.Softmax()
    
    if torch.cuda.is_available():
        fmap, logits = model(img.to('cuda'))
    else:
        fmap, logits = model(img)

    logits = sm(logits)
    _, prediction = torch.max(logits, 1)

    confidence = logits[:, int(prediction.item())].item() * 100

    if int(prediction.item()) == 0:
        prediction = 'FAKE'
    else:
        prediction = 'REAL'

    return (prediction, confidence)

def load_model(model, checkpoint_path):

    try:
        if torch.cuda.is_available():
            model.load_state_dict(torch.load(checkpoint_path))
        else:
            model.load_state_dict(torch.load(checkpoint_path, map_location = torch.device('cpu')))            
    except Exception as e:
        print("Error while reading model state\n")
        print(e)
        sys.exit(1)

    return model