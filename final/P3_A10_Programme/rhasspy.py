import requests
import json
import configparser

"""
Librairie d'accès d'utilisation de Rhasspy (https://rhasspy.readthedocs.io/en/latest/) rendue disponible pour le P3 du cours de LINFO1001.
"""

def text_to_speech(payload):
    """
	Exprime une chaine de caractère par synthèse vocale

	:param: (str) payload: la chaîne de caractères à experimer
	:return: True en cas de succès, sinon False.
	"""
    response = requests.post('http://localhost:12101/api/text-to-speech', payload.encode())
    if response.status_code==200:
        return True
    else:
        print("Erreur lors de l'appel à Rhasspy")
        return False


def speech_to_intent():
    """

    Indique à Rhasspy qu'une commande vocale va être lancée. Il s'ensuit un signal sonore qui indique que Rhasspy écoute. Après ce signal sonore, une phrase
    peut être enregistrée par Rhasspy. Une fois la phrase énoncée (après un silence, donc), un second signal sonore survient et le résultat est renvoyé.

	:param:/
	:return: un dictionnaire contenant les champs suivants :
        name: une chaîne de caractères contenant le nom de l'intent auquel Rhasspy fait référence.
	    variables: un dictionnaire comportant toutes les variables reconnues ainsi que leurs valeurs.
        raw_tokens: un tableau contenant les mots (tokens) que Rhasspy a reconnu
        tokens: un tableau contenant les mots de l'intent auxquels Rhasspy fait référence
	"""
    r = requests.post('http://localhost:12101/api/listen-for-command')
    if r.status_code!=200:
        print("Erreur lors de l'appel à Rhasspy")
        return None

    json_resp = r.json()
    dictionary = {}
    dictionary["raw_tokens"], dictionary["tokens"], dictionary["name"], dictionary["variables"] = list(map(str,json_resp["raw_tokens"])) ,list(map(str,json_resp["tokens"])), str(json_resp["intent"]["name"]), json_resp['slots']
    return  dictionary


def train_intent_files(filename="sentences.ini"):
    """
    Remplace la série de commandes vocales que Rhasspy va reconnaitre. Consultez le document Instructions Rhasspy pour plus d'informations sur sa structure.
    :param: filename: (facultatif) le nom du fichier sentences.ini
    :return: True si l'envoi et l'apprentissage ont réussi, False dans les autres cas. 
    """
    file = open(filename,'r')
    lines = file.readlines()
    new_query = "".join(lines)
    send_response = requests.post('http://localhost:12101/api/sentences',new_query.encode())
    train_response = requests.post("http://localhost:12101/api/train")
    if train_response.status_code == 200 and send_response.status_code == 200:
        print("Training worked perfectly.")
        return True
    elif train_response.status_code!=200:
        print("Training could not work.")
        return False
    elif  send_response.status_code != 200:
        print("Sending the .ini file could not work.")
        return False

