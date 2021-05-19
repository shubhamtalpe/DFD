from classify import classify
import sys
clf = classify('/home/soham/Downloads/checkpoint_80.pt')

#clf.get_prediction('/home/soham/Downloads/Disability Awareness Meeting - The Office US.mp4', True) 

#clf.get_prediction('/home/soham/Downloads/Bill Hader impersonates Arnold Schwarzenegger [DeepFake].mp4', True)


print(sys.argv[1])
clf.get_prediction(sys.argv[1], True)