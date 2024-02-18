import torch
import math
import black_box
from PIL import Image
from torchvision import transforms



class model_query_fn:
	def __init__(self, model):
		self.model = model
		self.model.eval()

	def __call__(self, img):
		preds = self.model(img)
		value = torch.argmax(preds, dim = 1)
		return value

model = torch.hub.load('pytorch/vision:v0.10.0', 'resnet18', pretrained=True)
model.eval()
image = Image.open("rabbit.png")

preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])])

image = torch.unsqueeze(preprocess(image), 0)
adv_image = Image.open("samoyed.jpg")
adv_image = torch.unsqueeze(preprocess(adv_image), 0)


attack = black_box.HopSkipJump(model_query_fn(model), clip_min = -2.5, clip_max = 2.5, targeted = True)
image = attack.generate(image, max_iter = 10000, num_evals = 64, target = 331, adversarial_sample = adv_image)
