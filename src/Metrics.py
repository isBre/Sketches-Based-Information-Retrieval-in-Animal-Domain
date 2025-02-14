import torch
from torch.nn import Module
from torch.utils.data import DataLoader
from torch import device
from typing import Tuple
from EmbeddingSpace import EmbeddingSpace


def k_precision(
  model: Module,
  sketches_val_loader: DataLoader,
  embedding_space: EmbeddingSpace,
  k: int,
  device: device,
) -> Tuple[float, float]:
    # Corrected Labeled samples
    correct = 0.0
    samples_val = 0
    # IMPORTANT: from now on, since we will introduce batch norm, 
    # we have to tell PyTorch if we are training or evaluating our model
    model = model.eval()
    # Context-manager that disabled gradient calculation
    with torch.no_grad():
      # Loop inside the data_loader
      # The batch size is definited inside the data_loader
      for idx_batch, (sketches, labels) in enumerate(sketches_val_loader):
        sketches, labels = sketches.to(device), labels.to(device)
        distances, topk_indexes = embedding_space.top_k_batch(sketches, k)
        for list_idx, i in zip(topk_indexes, range(len(topk_indexes))):
            # Check if the predicted class matches the actual label
            correct_predictions += sum(embedding_space.classes[idx] == labels[i] for idx in list_idx)
        # Convert to a tensor, compute the mean over k, and update the correct count
        correct += torch.tensor(correct_predictions).float() / k
        samples_val += len(sketches)
    accuracy = 100. * correct / samples_val
    return accuracy