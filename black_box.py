import torch

class HopSkipJump:
	def __init__(self, model_query_fn, max_eval, clip_min = None, clip_max = None, input_shape = torch.tensor([3, 224, 224]), targeted = False):
		self.model_query_fn = model_query_fn
		self.total_classes = 1000
		self.targeted = targeted
		self.theta = 0.01 / (torch.sqrt(torch.prod(input_shape)))
		self.clip_min = clip_min
		self.clip_max = clip_max

	