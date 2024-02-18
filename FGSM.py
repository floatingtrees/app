import torch

def _accuracy(a, b):
	a = torch.argmax(a, dim = 1)
	print(a.size())
	b = torch.argmax(b, dim = 1)
	values = torch.tensor([0], dtype = torch.int64)
	print("HERE", torch.sum(torch.heaviside(torch.abs(a - b), values))/a.size()[0])
	return torch.sum(torch.heaviside(torch.abs(a - b), values))/a.size()[0]

def FGSM_attack2(model, image, label, from_logits = True, loss_fn = torch.nn.CrossEntropyLoss(), epsilon = 0.001):

	labels = torch.zeros((1, 1000))
	labels[0, label] = 1

	data = image.clone().detach()
	original_preds = model(data)
	data.requires_grad = True
	outputs = model(data)
	if from_logits:
		outputs = torch.nn.functional.softmax(outputs, dim = 1)
	loss = loss_fn(outputs, labels)
	loss.backward()
	data_grad = data.grad.data
	perturbed_images = data + epsilon * data_grad.sign()

def targeted_attack2(model, image, label, from_logits = True, loss_fn = torch.nn.CrossEntropyLoss(), epsilon = 0.001):

	labels = torch.zeros((1, 1000))
	labels[0, label] = 1

	data = image.clone().detach()
	data.requires_grad = True
	optimizer = torch.optim.Adam(list([data, ]), maximize = False)


	for i in range(10):
		placeholder = torch.nn.functional.interpolate(data, 224)
		outputs = model(placeholder)
		if from_logits:
			outputs = torch.nn.functional.softmax(outputs, dim = 1)
		loss = loss_fn(outputs, labels)
		loss.backward()
		optimizer.step()

	return data

def FGSM_attack(model, dataloader, total_batches, from_logits = True, loss_fn = torch.nn.CrossEntropyLoss(), epsilon = 0.001):
	generated_images = []
	original_labels = []
	model.eval()
	percent_change = 0
	count = 0
	for batch in dataloader:
		x, y = batch
		data = x.clone().detach()
		original_preds = model(data)
		data.requires_grad = True
		outputs = model(data)
		if from_logits:
			outputs = torch.nn.functional.softmax(outputs, dim = 1)
		loss = loss_fn(outputs, y)
		loss.backward()
		data_grad = data.grad.data
		perturbed_images = data + epsilon * data_grad.sign()
		generated_images.append(perturbed_images)

		original_labels.append(y)
		count += 1

		new_preds = model(perturbed_images)

		if count >= total_batches:
			break
	return generated_images


def PGD_attack(model, dataloader, total_batches, iterations, from_logits = True, loss_fn = torch.nn.CrossEntropyLoss(), epsilon = 0.001):
	count = 0
	running_accuracy = 0

	generated_images = []
	original_labels = []
	for batch in dataloader:
		x, y = batch
		
		original_preds = model(x)
		accuracy = _accuracy(original_preds, y)

		for i in range(iterations):	
			data = x.clone().detach()
			data.requires_grad = True		
			outputs = model(data)
			if from_logits:
				outputs = torch.nn.functional.softmax(outputs, dim = 1)
			loss = loss_fn(outputs, y)

			loss.backward()
			data_grad = data.grad.data
			perturbed_images = data + epsilon * data_grad

		count += 1

		new_preds = model(perturbed_images)
		new_accuracy = _accuracy(new_preds, y)
		accuracy_change = torch.abs(new_accuracy - accuracy)
		print(running_accuracy)
		running_accuracy += accuracy_change

		generated_images.append(perturbed_images)
		original_labels.append(y)

		if count >= total_batches:
			break

	running_accuracy /= count

	return generated_images, original_labels, running_accuracy

def targeted_adversarial_attack(model, dataloader, total_batches, iterations, target_label, from_logits = True, loss_fn = torch.nn.CrossEntropyLoss()):
	count = 0
	percent_change = 0
	generated_images = []
	original_labels = []
	running_accuracy = 0
	for batch in dataloader:
		x, y = batch
		data = x.clone().detach()
		data.requires_grad = True
		original_preds = model(data)
		accuracy = _accuracy(original_preds, y)
		optimizer = torch.optim.Adam(list([data, ]), maximize = False)

		for i in range(iterations):
			optimizer.zero_grad()
			outputs = model(data)
			
			if from_logits:
				outputs = torch.nn.functional.softmax(outputs, dim = 1)
			labels = target_label
			loss = loss_fn(outputs, labels)
			loss.backward()
			optimizer.step()
			accuracy = _accuracy(original_preds, y)
		new_preds = model(data)
		new_accuracy = loss_fn(new_preds, labels)
		running_accuracy += torch.abs(new_accuracy - accuracy)
		count += 1
		generated_images.append(data)
		original_labels.append(y)
		if count >= total_batches:
			break
	running_accuracy /= count


	return generated_images, original_labels, running_accuracy



  



