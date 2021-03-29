import os
import shutil
import wget


def descargaImagen(url_img):
    folder = 'multimedia/imagenes'
    eliminarCarpeta(folder)
    wget.download(url_img, "multimedia/imagenes/img.png")


def descargaVideo(url_video):
    folder = 'multimedia/videos'
    eliminarCarpeta(folder)
    wget.download(url_video, "multimedia/videos/video.mp4")


def eliminarCarpeta(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
