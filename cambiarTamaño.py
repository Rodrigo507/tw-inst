from PIL import Image
import cv2


def cambioTamanno():
    im = Image.open("multimedia/imagenes/img.png")
    # convertimos a JPG
    rgb_im = im.convert('RGB')
    # cambio de tamaño
    # im_resized = rgb_im.resize((640,640))
    im_resized = rgb_im.resize((978, 515))
    # im_resized = rgb_im.resize((1080, 1920))
    # guardamos la imagen
    im_resized.save('multimedia/imagenes/cambio.jpg')


def cambioTamannoVideo():
    vidcap = cv2.VideoCapture("multimedia/videos/video.mp4")
    success, image = vidcap.read()
    count = 0

    while success:
        height, width, layers = image.shape
        new_h = 1080
        new_w = 1080
        resize = cv2.resize(image, (new_w, new_h))
        cv2.imwrite("%03d.jpg" % count, resize)
        success, image = vidcap.read()
        count += 1
