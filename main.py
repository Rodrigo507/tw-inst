from instabot import bot, Bot
import tweepy
import downloadFiles as download
import cambiarTamaño as cambioTama
import credential


# funcion de login para cuenta de instagram
def loginAcount(user, password):
    # usuario = 'test.dev'
    # password = '123'
    bot = Bot()
    bot.login(username=user, password=password)
    return bot


# Funcion para mostrar solo los Tweet originales (no respuestas / RT)
def from_creator(status):
    if hasattr(status, 'retweeted_status'):
        return False
    elif status.in_reply_to_status_id != None:
        return False
    elif status.in_reply_to_screen_name != None:
        return False
    elif status.in_reply_to_user_id != None:
        return False
    else:
        return True


class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        if from_creator(status):  # solo para procesar los tweet de la cuenta y no otros datos (RT, fav, Respuestas)
            texto = ""  # variable para almacenar el texto del tweet
            # opcion 1 tipo de tweet Extended
            if hasattr(status, 'extended_tweet'):  # comprobamos si ocupa gran numero de caracteres el tweet
                # capturamos el texto
                texto = status.extended_tweet['full_text'][
                        status.extended_tweet['display_text_range'][0]:status.extended_tweet['display_text_range'][
                            1]] + ' @' + status.user.screen_name.lower() + "\n.\n.\n.\n.\n #Huracanlota #Nicaragua #Kappa #Centroamérica #clima #CostaRica  #Panama #Pronostico #ClimaPanama #Veraguas #Cocle #Chiriqui #Santiago #Penonome"  # Optenemos el texto del tweet
                try:
                    if 'extended_entities' in status.extended_tweet:  # si existe las extended_entities para fotos o videos (multimedia)
                        # capturamos el tipo de multimedia(foto, video o gif)
                        tipoMultimediaExtended_tweet = status.extended_tweet['extended_entities']['media'][0]['type']
                        if tipoMultimediaExtended_tweet == 'photo':  # fotos
                            # obtenemos la url para luego ser descargada
                            urlDown = status.extended_tweet['extended_entities']['media'][0]['media_url']
                            download.descargaImagen(urlDown)  # descargamos la imagen
                            cambioTama.cambioTamanno()  # cambiamos la resolucion para poder subirla a instagram
                            # uploadImagen(bot, texto)  # subimos la foto
                        else:  # para descargar videos (BETA)
                            video = 1
                            urlDown = \
                                status.extended_tweet['extended_entities']['media'][0]['video_info']['variants'][0][
                                    'url']
                            download.descargaVideo(urlDown)
                except AttributeError:
                    print("Datos")
            if hasattr(status, 'extended_entities'):  # Tweet que sean normales(Texto cortos) pero con multiemedia
                # Varia la estructura del JSON
                # Capturamos el texto
                texto = status.text[status.display_text_range[0]:status.display_text_range[
                    1]] + ' @' + status.user.screen_name.lower() + "\n.\n.\n.\n.\n #Huracanlota #Nicaragua #Kappa #Centroamérica #clima #CostaRica  #Panama #Pronostico #ClimaPanama #Veraguas #Cocle #Chiriqui #Santiago #Penonome"  # Optenemos el texto del tweet
                # capturamos el tipo de multimedia(foto, video o gif)
                tipoMultimedia = status.extended_entities['media'][0][
                    'type']  # Optenemos el tipo de multimedia del tweet
                if tipoMultimedia == 'photo':  # fotos
                    # obtenemos la url para luego ser descargada
                    urlDown = status.extended_entities['media'][0]['media_url']
                    download.descargaImagen(urlDown)  # descargamos la imagen
                    cambioTama.cambioTamanno()  # cambiamos la resolucion para poder subirla a instagram
                    # uploadImagen(bot, texto)  # subimos la foto
                elif tipoMultimedia == 'video':  # videos
                    urlDown = status.extended_entities['media'][0]['video_info']['variants'][1]['url']
                    download.descargaVideo(urlDown)
                else:  # GIFF
                    video = 1
                    urlDown = status.extended_entities['media'][0]['video_info']['variants'][0]['url']
                    download.descargaVideo(urlDown)

    def on_error(self, status_code):
        print("Error ", status_code)


consumer_token = credential.consumer_token
consumer_secret = credential.consumer_secret
accessToken = credential.accessToken
accessTokenSecret = credential.accessTokenSecret

auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
auth.set_access_token(accessToken, accessTokenSecret)
# StreamListener
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
myStream.filter(follow=['2552946000', '2434125131', '398875471', '354529506', '1131729401366929425', '2225466931'],
                is_async=True)
# myStream.filter(follow=['2552946000','2434125131','398875471','354529506','1131729401366929425','2225466931'], is_async=True)
# bot = loginAcount(credential.user,credential.password)
print("Hola")

# if __name__ == '__main__':
# autenticacion
# consumer_token = credential.consumer_token
# consumer_secret = credential.consumer_secret
# accessToken = credential.accessToken
# accessTokenSecret = credential.accessTokenSecret
#
# auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
# auth.set_access_token(accessToken, accessTokenSecret)
# # StreamListener
# api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
# myStreamListener = MyStreamListener()
# myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
# print("Hola")
