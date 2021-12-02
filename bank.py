STATE_NORMAL = 0
STATE_CONFIRMATION = 1

def __init__(self):
	self.__state = STATE_NORMAL

def process(self, action, params):
	if self.__state == STATE_NORMAL:
		if action == "Bank_supprimer":
			faire_qqch()
			self.__state = STATE_CONFIRMATION

	elif self.__state == STATE_CONFIRMATION:
		if action == "Confirmer":
			self.__state = STATE_NORMAL
			pass

		elif action == "Refuser":
			self.__state = STATE_NORMAL
			pass
