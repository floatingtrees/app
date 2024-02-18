import torch
import math
import HSJA

class model_query_fn(model):
	def __init__(self, model):
		self.model = model
		self.model.eval()

	def __call__(self, img):
		preds = self.model(img)
		value = torch.argmax(preds, dim = 1)
		return value

model = torch.hub.load('pytorch/vision:v0.10.0', 'resnet18', pretrained=True)
model.eval()