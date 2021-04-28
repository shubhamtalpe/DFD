import cv2
import sys
import torch
import numpy as np
from stats import stats
from torch.nn import Softmax
import matplotlib.pyplot as plt
from torchvision import transforms

def calculate_accuracy(outputs, targets):
    batch_size = targets.size(0)

    _, pred = outputs.topk(1, 1, True)
    pred = pred.t()
    correct = pred.eq(targets.view(1, -1))

    num_correct_elements = correct.float().sum().item()

    return 100 * num_correct_elements / batch_size

def load_model(model, checkpoint_path):

    try:
        if torch.cuda.is_available():
            model.load_state_dict(torch.load(checkpoint_path))
        else:
            model.load_state_dict(torch.load(checkpoint_path, map_location = torch.device('cpu')))            
    except Exception as e:
        print("Error while reading model state\n")
        print(e)

    return model

def train(epoch, num_epochs, data_loader, model, criterion, optimizer, checkpoint_path):
    
    model.train()
    
    losses = stats()
    accuracies = stats()
    
    for idx, (inputs, targets) in enumerate(data_loader):
        
        if torch.cuda.is_available():
            targets = targets.type(torch.cuda.LongTensor)
            inputs = inputs.cuda()
        
        _, outputs = model(inputs)
        
        if torch.cuda.is_available():
            loss  = criterion(outputs,targets.type(torch.cuda.LongTensor))
            acc = calculate_accuracy(outputs, targets.type(torch.cuda.LongTensor))
        else:
            loss  = criterion(outputs,targets.type(torch.LongTensor))
            acc = calculate_accuracy(outputs, targets.type(torch.LongTensor))


        losses.update(loss.item(), inputs.size(0))
        accuracies.update(acc, inputs.size(0))
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        sys.stdout.write(
                "\r[Epoch %d/%d] [Batch %d / %d] [Loss: %f, Acc: %.2f%%]"
                % (
                    epoch,
                    num_epochs,
                    idx,
                    len(data_loader),
                    losses.avg,
                    accuracies.avg))
    print("\n")
    
    torch.save(model.state_dict(), checkpoint_path)
    
    return losses.avg, accuracies.avg

def test(epoch, model, data_loader, criterion):
    
    model.eval()
    
    losses = stats()
    accuracies = stats()
    
    pred = []
    true = []
    
    with torch.no_grad():
        
        for idx, (inputs, targets) in enumerate(data_loader):
            
            if torch.cuda.is_available():
                targets = targets.cuda().type(torch.cuda.FloatTensor)
                inputs = inputs.cuda()
            
            _,outputs = model(inputs)
            
            if torch.cuda.is_available():
                loss = torch.mean(criterion(outputs, targets.type(torch.cuda.LongTensor)))
                acc = calculate_accuracy(outputs,targets.type(torch.cuda.LongTensor))
                true += (targets.type(torch.cuda.LongTensor)).detach().cpu().numpy().reshape(len(targets)).tolist()
            else:
                loss = torch.mean(criterion(outputs, targets.type(torch.LongTensor)))
                acc = calculate_accuracy(outputs,targets.type(torch.LongTensor))
                true += (targets.type(torch.LongTensor)).detach().cpu().numpy().reshape(len(targets)).tolist()
            
            _,p = torch.max(outputs,1) 
            pred += p.detach().cpu().numpy().reshape(len(p)).tolist()
            
            losses.update(loss.item(), inputs.size(0))
            accuracies.update(acc, inputs.size(0))
            
            sys.stdout.write(
                    "\r[Batch %d / %d]  [Loss: %f, Acc: %.2f%%]"
                    % (
                        idx,
                        len(data_loader),
                        losses.avg,
                        accuracies.avg
                        )
                    )
        
        print('\nAccuracy {}'.format(accuracies.avg))
    
    return true,pred,losses.avg,accuracies.avg