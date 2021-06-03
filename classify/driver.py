from classify import classify
import sys
import math
clf = classify('/home/soham/Downloads/checkpoint_80.pt')

#clf.get_prediction('/home/soham/Downloads/Disability Awareness Meeting - The Office US.mp4', True) 

#clf.get_prediction('/home/soham/Downloads/Bill Hader impersonates Arnold Schwarzenegger [DeepFake].mp4', True)


#print(sys.argv[1])
prediction = clf.get_prediction(sys.argv[1], True)
print(prediction[0])
if prediction[0] == 'REAL':
    print(math.ceil(100-prediction[1]))
else:
    print(math.ceil(prediction[1]))