import pickle

with open('ckdMLmodel.pkl', 'rb') as model_file:
    model = pickle.load(model_file)
model.summary()
