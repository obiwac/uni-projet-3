#!/usr/bin/python3
# -*- coding: utf-8 -*

"""
Librairie de cryptographie rendue disponible pour le P3 du cours de LINFO1001.

Attention: Cette librairie a été réalisée à des fins purement didactiques et ne peut en aucun cas être considérée comme une solution cryptographique viable pour un programme en dehors du contexte du cours LINFO1001.
"""
import rhasspy
class Security :
    __STATE_NORMAL=0
    __STATE_CONFIRMATION=1
    def __init__(self,rhasspy, key="cle"):
        self.__state=Security.__STATE_NORMAL
        self.__rhasspy = rhasspy
        self.__key= key
        self.__nbrhash= None
        self.__cdehash= None
        
    def encode(self,key, plain_text):
        """
        Chiffre un texte en utilisant une clé de chiffrement.
        Les deux arguments sont fournis sous la forme d'une chaine de caractères.
        L'algorithme utilisé est le chiffrement de Vigenère.
        Attention : cette méthode est "craquée" depuis longtemps, mais elle illustre le fonctionnement d'un algorithme de chiffrement.

        :param (str) key: la clé symétrique
        :param (str) plain_text: le texte à chiffrer
        :return (str): le texte chiffré
        """
        enc = []
        for i, e in enumerate(plain_text):
            key_c = key[i % len(key)]
            enc_c = chr((ord(e) + ord(key_c)) % 256)
            enc.append(enc_c)
        return "".join(enc)

    def decode(self,key, cipher_text):
        """
        Déchiffre le texte en utilisant la clé de déchiffrement.
        Les deux arguments sont fournis sous la forme d'une chaine de caractères.
        L'algorithme utilisé est le (dé)chiffrement de Vigenère.
        Attention : cette méthode est "craquée" depuis longtemps, mais elle illustre le fonctionnement d'un algorithme de (dé-)chiffrement.

        :param (str) key: la clé symétrique
        :param (str) cipher_text: le texte crypté
        :return (str): le texte décrypté
        """
        dec = []
        for i, e in enumerate(cipher_text):
            key_c = key[i % len(key)]
            dec_c = chr((256 + ord(e) - ord(key_c)) % 256)
            dec.append(dec_c)
        return str("".join(dec))

    def hashing(self,string):
        """
        Hachage d'une chaîne de caractères fournie en paramètre.
        Le résultat est une chaîne de caractères.
        Attention : cette technique de hachage n'est pas suffisante (hachage dit cryptographique) pour une utilisation en dehors du cours.

        :param (str) string: la chaîne de caractères à hacher
        :return (str): le résultat du hachage
        """
        def to_32(value):
            """
            Fonction interne utilisée par hashing.
            Convertit une valeur en un entier signé de 32 bits.
            Si 'value' est un entier plus grand que 2 ** 31, il sera tronqué.

            :param (int) value: valeur du caractère transformé par la valeur de hachage de cette itération
            :return (int): entier signé de 32 bits représentant 'value'
            """
            value = value % (2 ** 32)
            if value >= 2**31:
                value = value - 2 ** 32
            value = int(value)
            return value

        if string:
            x = ord(string[0]) << 7
            m = 1000003
            for c in string:
                x = to_32((x*m) ^ ord(c))
            x ^= len(string)
            if x == -1:
                x = -2
            return str(x)
        return ""

        


    def input_numero(self,nbr,enter=None):
        if  self.__nbrhash== None:
            __nbr= nbr
            if not __nbr.isnumeric():
                self.__rhasspy.text_to_speech("votre numero est vide ou ne contient pas uniquement des chiffres")
            self.__nbrhash=self.hashing(self.encode(self.__key, __nbr))
        else:
            __enter= enter
            if not __enter.isnumeric():
                self.__rhasspy.text_to_speech("votre numero est vide ou ne contient pas que des chiffres")
            else:    
                __enterhash=self.hashing(self.encode(self.__key, __enter))
                if self.__nbrhash != enterhash:
                    self.__rhasspy.text_to_speech("numero incorrecte")
                else :
                    return True

    def input_code(self,cde,enter=None):
        if self.__cdehash== None:
            __cde= cde
            if not __cde.isalpha():
                self.__rhasspy.text_to_speech("votre code est vide ou ne contient pas uniquement des lettres")
            else:
                self.__cdehash=self.hashing(self.encode(self.__key, __cde))
        else:
            __enter= enter
            if not __enter.isalpha():
                self.__rhasspy.text_to_speech("votre code est vide ou ne contient pas uniquement des lettres")
            else :    
                __enterhash=self.hashing(self.encode(self.__key, __enter))
                if __enterhash != self.__nbrhash:
                    self.__rhasspy.text_to_speech("code incorrect")
                else :
                    return True

    def delete_nbrhash(self,action):
        """supprime le hasking du numero
        """
        if self.__state==State_normal:
            self.__rhasspy.text_to_speech("voullez-vous vraoment supprimer le numero")
            self.__state=State_confirmation
        elif self.__state==State_confirmation:
            if action=="confirmer":
                self.__rhasspy.text_to_speech("numero supprimé")
                self.__nbrhash=None
            else:
                self.__state=State_normal
        
    def delete_cdehash(self,action):
        """supprime le hashing du code
        """
        if self.__state==State_normal:
            self.__rhasspy.text_to_speech("voullez-vous vraoment supprimer le code")
            self.__state=State_confirmation
        elif self.__state==State_confirmation:
            if action=="confirmer":
                text_to_speech("code supprimé")
                self.__cdehash=None
            else:
                self.__state=State_normal
    
    

