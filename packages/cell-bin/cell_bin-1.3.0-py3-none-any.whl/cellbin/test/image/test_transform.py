import numpy as np
from cellbin.image.transform import ImageTransform


def rotate_skimage(angle, scale, im):
    import skimage
    im_dtype = im.dtype
    if im.ndim == 3:
        out_im = skimage.transform.rescale(im, (scale[1], scale[0]), multichannel=True)
    elif im.ndim == 2:
        out_im = skimage.transform.rescale(im, (scale[1], scale[0]))
    else:
        raise Exception("Not Supported")
    out_im = skimage.transform.rotate(out_im, angle, resize=True)
    # BUG: skimage will transform image to float64, convert back to match input image dtype
    max_val = 256 ** im_dtype.type(1).itemsize
    out_im = out_im * (max_val - 1)
    out_im.astype(im_dtype)
    return out_im


class TestImageTransform():
    def __init__(self):
        self.itf = ImageTransform()

    def test_rot_scale(self, x_scale: float, y_scale: float, angle: float, img: np.ndarray):
        self.itf.set_image(img)
        trans_itf = self.itf.rot_scale(x_scale=x_scale, y_scale=y_scale, angle=angle)
        trans_sk = rotate_skimage(angle=-angle, scale=(x_scale, y_scale), im=img)
        print(trans_sk)
        print(trans_itf)
        np.allclose(trans_sk, trans_itf)


if __name__ == '__main__':
    im = np.random.randint(low=0, high=255, size=(3, 5), dtype='uint8')
    print(f"original\n{im}")
    angle = 45
    scale = [1, 1]
    # trans_im = rotate_skimage(angle, scale, im)
    # print(f"transform\n{trans_im}")
    tit = TestImageTransform()
    tit.test_rot_scale(x_scale=scale[0], y_scale=scale[1], angle=angle, img=im)
