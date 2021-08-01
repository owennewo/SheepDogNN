import os
import torch
from matplotlib.pyplot import imsave

# os.environ['LD_LIBRARY_PATH']="/usr/local/cuda/lib64"
# print("setting LD_LIBRARY_PATH")
print(torch.__version__)
a = torch.cuda.FloatTensor(2).zero_()
print(a)

from ui_common import ui_common
import nn_common as common
import numpy as np
from torchvision.utils import save_image


# PATH="/usr/local/cuda/bin:${PATH}"
# ENV LD_LIBRARY_PATH="/usr/local/cuda/lib64:${LD_LIBRARY_PATH}"



if not torch.cuda.is_available():
    print("torch says you have no cuda.  Aborting")
    exit(1)

os.makedirs('test/dummy', exist_ok=True)

transform = common.get_transform()
net = common.create_net(True)
device = common.get_device()

def predict_callback(owner, count):

    if count%3 == 0:
        filename = f"test/dummy/test.png"        
        # save 1 using save_image (problem seems to have noise - vertical strips)
        # save_image(torch.from_numpy(np.flip(owner.image_data,0).copy()),filename)
        
        # save 2 using savefig (problem - diffiful to set exact size e.g. 32x32)
        # owner.ax.set_axis_off()
        # owner.fig.savefig(filename,bbox_inches='tight', pad_inches=0)
        
        # save#3 using imsave (goldilocks!)
        imsave(filename, arr=np.flip(owner.image_data,0), cmap='gray', format='png')
                

        dataset_loader, _ = common.get_dataloader(transform, 'test')
        
        images, labels = next(iter(dataset_loader))
        # print(images.size())
        images, labels = images.to(device), labels.to(device)

        images = images.view(1, -1) # torch.Size([1, 784])
        # print(images.size())
        outputs = net(images)

        label = labels.cpu().detach().numpy()[0]
        output = outputs.cpu().detach().numpy()[0]
        class_index = np.argmax(output)
        ui.set_title(f"prediction = {classes[class_index]}")
        print(class_index)

def main():
    global classes, ui
    image_dir = 'images'
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
    _, classes = common.get_dataloader(transform, image_dir)
   

    while True:

                
        ui = ui_common(callback=predict_callback)
        # ui = ui_common(example_callback)
        device_id = ui.find_usb_device()
        ui.start(device_id)

        
if __name__ == "__main__":
    main()
