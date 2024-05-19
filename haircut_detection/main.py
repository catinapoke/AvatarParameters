import timm
import torch
import numpy as np
from PIL import Image
from torchvision import transforms
import argparse
from typing import List


# https://vitalflux.com/pytorch-load-predict-pretrained-resnet-model/
def prepare_image(img):
    #
    # Create a preprocessing pipeline
    #
    preprocess = transforms.Compose([
        transforms.Resize(288),
        # transforms.CenterCrop(288),# 224
        transforms.ToTensor(),
        transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )])
    #
    # Pass the image for preprocessing and the image preprocessed
    #
    img_cat_preprocessed = preprocess(img)
    #
    # Reshape, crop, and normalize the input tensor for feeding into network for evaluation
    #
    return torch.unsqueeze(img_cat_preprocessed, 0)


def print_prediction(predicted_result):
    with open('./labels.txt') as f:
        labels = [line.strip() for line in f.readlines()]
    #
    # Find the index (tensor) corresponding to the maximum score in the out tensor.
    # Torch.max function can be used to find the information
    #
    _, index = torch.max(predicted_result, 1)
    #
    # Find the score in terms of percentage by using torch.nn.functional.softmax function
    # which normalizes the output to range [0,1] and multiplying by 100
    #
    percentage = torch.nn.functional.softmax(predicted_result, dim=1)[0] * 100
    #
    # Print the name along with score of the object identified by the model
    #
    print(labels[index[0]], percentage[index[0]].item())
    #
    # Print the top 5 scores along with the image label. Sort function is invoked on the torch to sort the scores.
    #
    
    _, indices = torch.sort(predicted_result, descending=True)
    
    print([(labels[idx], percentage[idx].item()) for idx in indices[0][:len(labels)]])


def old_stuff(image, model):
    image = torch.as_tensor(np.array(image, dtype=np.float32)).transpose(2, 0)[None]
    feature_output = model.forward_features(image)
    print(feature_output)


def main(image_path: str):
    model = timm.create_model('efficientnet_b3a', checkpoint_path='./output/train/20230112-144828-efficientnet_b3a-288/checkpoint-6.pth.tar')

    image = Image.open(image_path)
    prepared = prepare_image(image)

    model.eval()
    print_prediction(model(prepared))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Extracting feature from trained model.")
    parser.add_argument("--img_path", required=True, help="The path of image on disk.")
    args = parser.parse_args()
    main(args.img_path) 
