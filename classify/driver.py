from classify import classify

clf = classify('/home/soham/Downloads/model_97_acc_80_frames_FF_data.pt')

clf.get_prediction('/home/soham/11/bcmrkgjtdq.mp4', False) 