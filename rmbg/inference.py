import numpy as np
import io
import torch, os
from rmbg.briarmbg import BriaRMBG
from rmbg.utilities import preprocess_image, postprocess_image
from PIL import Image

net = BriaRMBG()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
net = BriaRMBG.from_pretrained("briaai/RMBG-1.4")
net.to(device)
net.eval()


def inference(img_bytes):
    # prepare input
    model_input_size = [1024, 1024]
    # orig_im = np.array(Image.open(im_path))
    orig_im = np.array(Image.open(io.BytesIO(img_bytes)))
    orig_im_size = orig_im.shape[0:2]
    image = preprocess_image(orig_im, model_input_size).to(device)

    # inference
    result = net(image)

    # post process
    result_image = postprocess_image(result[0][0], orig_im_size)

    # save result
    pil_im = Image.fromarray(result_image)
    no_bg_image = Image.new("RGBA", pil_im.size, (0, 0, 0, 0))
    orig_image = Image.open((io.BytesIO(img_bytes)))
    no_bg_image.paste(orig_image, mask=pil_im)

    no_bg_image_bytes = io.BytesIO()
    no_bg_image.save(no_bg_image_bytes, format='PNG')
    no_bg_image_bytes_value = no_bg_image_bytes.getvalue()
    print(type(no_bg_image_bytes_value))

    return no_bg_image_bytes_value
