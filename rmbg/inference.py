from skimage import io as skio
from io import BytesIO
import torch, os
from rmbg.briarmbg import BriaRMBG
from rmbg.utilities import preprocess_image, postprocess_image
from PIL import Image
from huggingface_hub import hf_hub_download

net = BriaRMBG()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
net = BriaRMBG.from_pretrained("briaai/RMBG-1.4")
net.to(device)
net.eval()

def inference(img_bytes):
    # prepare input
    im_path = "/home/cchase/git/github/cfchase/rmbg-service/examples/example_input.jpg"
    model_input_size = [1024,1024]
    orig_im = skio.imread(im_path)
    orig_im_size = orig_im.shape[0:2]
    image = preprocess_image(orig_im, model_input_size).to(device)

    # inference
    result=net(image)

    # post process
    result_image = postprocess_image(result[0][0], orig_im_size)

    # save result
    pil_im = Image.fromarray(result_image)
    no_bg_image = Image.new("RGBA", pil_im.size, (0,0,0,0))
    orig_image = Image.open(im_path)
    no_bg_image.paste(orig_image, mask=pil_im)
    # no_bg_image.save("/home/cchase/git/github/cfchase/rmbg-service/examples/example_image_no_bg.png")

    no_bg_image_bytes = BytesIO()
    no_bg_image.save(no_bg_image_bytes, format='PNG')
    no_bg_image_bytes_value = no_bg_image_bytes.getvalue()
    # with open("/home/cchase/git/github/cfchase/rmbg-service/examples/example_image_no_bg_bytes.png", "wb") as binary_file:
    #     # Write bytes to file
    #     binary_file.write(no_bg_image_bytes_value)
    return no_bg_image_bytes_value
