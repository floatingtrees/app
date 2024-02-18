import torch
import math

class HopSkipJump:
	def __init__(self, model_query_fn, clip_min = None, clip_max = None, input_shape = torch.tensor([3, 224, 224]), targeted = False):
		self.model_query_fn = model_query_fn
		self.total_classes = 1000
		self.targeted = targeted
		self.theta = 0.01 / (torch.sqrt(torch.prod(input_shape)))
		self.clip_min = clip_min
		self.clip_max = clip_max

	def _clip(self, tensor):
		return torch.clip(tensor, self.clip_min, self.clip_max)

	def generate(self, initial_input, adversarial_sample, max_iter, num_evals = 32, target = None):
		self.target = target
		first_iter = True
		current_image = initial_input
		for i in range(max_iter):
			delta = self._compute_delta(current_image, adversarial_sample, first_iter)
			current_sample = self._clip(self._binary_search(current_image, initial_input, delta, target))
			dist = torch.linalg.norm(current_sample - initial_input)
			grads = self._approximate_gradient(current_image, initial_input, num_evals, target)


			first_iter = False

	def _approximate_gradient(current_image, initial_input, num_evals, target):
		shape = list(current_image.size())
		shape[0] = num_evals
		noise = torch.randn(shape)
		perturbed_sample = self._clip(current_sample.clone().detach() + delta * noise)
		noise = (perturbed_sample - current_sample) / delta
		decisions = self._validate_sample(perturbed)
		output_shape = decisions.size()

		fval = 2 * torch.reshape(decisions.float(), output_shape) - 1.0
		broadcast_dest = [1] * len(noise.size())
		broadcast_dest[0] = -1
		fval = torch.broadcast_to(fval.reshape(broadcast_dest), noise.size())
		if (int(torch.mean(fval)) == 1):
			gradf = torch.mean(noise, dim = 0)
		elif (int(torch.mean(fval)) == -1):
			gradf = - torch.mean(noise, dim = 0)
		else:
			fval = fval.detach().clone() - torch.mean(fval)
		gradf = torch.mean(fval * noise, dim = 0)

	gradf = gradf / (torch.linalg.norm(gradf) + self.stabilizer)
	return gradf


	def _compute_delta(self, current_image, initial_input, first_iter):
		if first_iter:
			return 0.1 * (self.clip_max - self.clip_min)

		distance = torch.linalg.norm(current_image - initial_input)
		return torch.sqrt(torch.prod(self.input_shape)) * self.theta * distance

	def _binary_search(self, current_image, initial_input, delta, target):
		au = 1
		al = 0 
		alpha = 0.5
		while math.abs(au - al) < self.theta:
			alpha = (au - al) / 2
			perturbed_sample = self._clip((1 - alpha) * initial_input + alpha * current_image)
			model_output = self._validate_sample(adjusted_input)
			if model_output == 1:
				self.cached_result = perturbed_sample
				au = alpha
			else:
				al = alpha

		return self.cached_result





	def _validate_sample(self, adjusted_input):
		model_output = self.model_query_fn(adjusted_input)
		return torch.where(model_output == self.target, 1, 0)


