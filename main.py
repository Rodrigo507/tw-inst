from instabot import Bot
import tweepy
import downloadFiles
import cambiarTamaño
import credenciales
import time

tagsTexto = "\n.\n.\n.\n.\n #Centroamérica #clima #CostaRica  #Pronostico #ClimaPanama #Veraguas #Cocle #Chiriqui " \
            "#Santiago #Penonome #panama #pty #panamacity #travel #pty507 #chiriqui #visitpanama "


def uploadImagen(botInsta, txt):
    # parametros
    # bot: bot logeado de instagram
    # txt: Mensaje del post
    botInsta.upload_photo('multimedia/imagenes/cambio.jpg', caption=txt)


# Subir video al feed de la cuenta de instagram
def uploadVideo(botInsta, caption):
    botInsta.upload_video('multimedia/videos/video.mp4', caption=caption, thumbnail=None)
    time.sleep(30)

# funcion de login para cuenta de instagram
def loginAcount(user, password):
    # usuario = 'test.dev'
    # password = '123'
    botInsta = Bot()
    botInsta.login(username=user, password=password)
    return botInsta


# Funcion para mostrar solo los Tweet originales (no respuestas / RT)
def from_creator(status):
    if hasattr(status, 'retweeted_status'):
        return False
    elif status.in_reply_to_status_id is not None:
        return False
    elif status.in_reply_to_screen_name is not None:
        return False
    elif status.in_reply_to_user_id is not None:
        return False
    else:
        return True


class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        if from_creator(status):  # solo para procesar los tweet de la cuenta y no otros datos (RT, fav, Respuestas)
            # opcion 1 tipo de tweet Extended
            if hasattr(status, 'extended_tweet'):  # comprobamos si ocupa gran numero de caracteres el tweet
                # capturamos el texto
                texto = status.extended_tweet['full_text'][
                        status.extended_tweet['display_text_range'][0]:status.extended_tweet['display_text_range'][
                            1]] + ' @' + status.user.screen_name.lower() + tagsTexto
                try:
                    if 'extended_entities' in status.extended_tweet:  # si existe las extended_entities para fotos o
                        # videos (multimedia)
                        # capturamos el tipo de multimedia(foto, video o gif)
                        tipoMultimediaExtended_tweet = status.extended_tweet['extended_entities']['media'][0]['type']
                        if tipoMultimediaExtended_tweet == 'photo':  # fotos
                            # obtenemos la url para luego ser descargada
                            urlDown = status.extended_tweet['extended_entities']['media'][0]['media_url']
                            downloadFiles.descargaImagen(urlDown)  # descargamos la imagen
                            cambiarTamaño.cambioTamanno()  # cambiamos la resolucion para poder subirla a instagram
                            uploadImagen(bot, texto)  # subimos la foto
                        else:  # para descargar videos (BETA)
                            urlDown = \
                                status.extended_tweet['extended_entities']['media'][0]['video_info']['variants'][0][
                                    'url']
                            downloadFiles.descargaVideo(urlDown)
                            uploadVideo(bot, texto)
                except AttributeError:
                    print("Datos")
            if hasattr(status, 'extended_entities'):  # Tweet que sean normales(Texto cortos) pero con multiemedia
                # Varia la estructura del JSON
                # Capturamos el texto
                texto = status.text[status.display_text_range[0]:status.display_text_range[
                    1]] + ' @' + status.user.screen_name.lower() + tagsTexto
                # capturamos el tipo de multimedia(foto, video o gif)
                tipoMultimedia = status.extended_entities['media'][0][
                    'type']  # Optenemos el tipo de multimedia del tweet
                if tipoMultimedia == 'photo':  # fotos
                    # obtenemos la url para luego ser descargada
                    urlDown = status.extended_entities['media'][0]['media_url']
                    downloadFiles.descargaImagen(urlDown)  # descargamos la imagen
                    cambiarTamaño.cambioTamanno()  # cambiamos la resolucion para poder subirla a instagram
                    uploadImagen(bot, texto)  # subimos la foto
                elif tipoMultimedia == 'video':  # videos
                    urlDown = status.extended_entities['media'][0]['video_info']['variants'][1]['url']
                    downloadFiles.descargaVideo(urlDown)
                    uploadVideo(bot, texto)
                else:  # GIFF
                    urlDown = status.extended_entities['media'][0]['video_info']['variants'][0]['url']
                    downloadFiles.descargaVideo(urlDown)
                    uploadVideo(bot, texto)

    def on_error(self, status_code):
        print("Error ", status_code)


if __name__ == '__main__':
    folder = 'config'
    downloadFiles.eliminarCarpeta(folder)
    # autenticacion
    consumer_token = credenciales.consumer_token
    consumer_secret = credenciales.consumer_secret
    accessToken = credenciales.accessToken
    accessTokenSecret = credenciales.accessTokenSecret

    auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
    auth.set_access_token(accessToken, accessTokenSecret)
    # StreamListener
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
    myStream.filter(follow=['2552946000', '398875471', '354529506', '2225466931','298651418'], is_async=True)

    # cuenta Insta
    bot = loginAcount(credenciales.user, credenciales.password)
