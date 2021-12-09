import crypto
import module

class Bankcode(module.Module):
	def __init__(self):
		super().__init__()

		self.__bankcode = None
		self.__passcode = None

		try:
			self.read()

		except FileNotFoundError:
			self.__encrypted_bankcode = None
			self.__hashed_passcode = None

	def read(self):
		data = self.read_user_data("bankcode")

		if len(data) == 2:
			self.__encrypted_bankcode, self.__hashed_passcode = data
			return

		raise FileNotFoundError("Invalid bankcode file")

	def write(self):
		if self.__hashed_passcode is None or self.__encrypted_bankcode is None:
			return

		self.write_user_data("bankcode", "\n".join((self.__encrypted_bankcode, self.__hashed_passcode)))

	def await_bankcode(self):
		while True:
			action, params = self.await_speech()

			if action == "Bankcode":
				self.__bankcode = " ".join(str(params[i]) for i in "abcd")
				break

	def await_passcode(self):
		while True:
			action, params = self.await_speech()

			if action == "Passcode":
				self.__passcode = " ".join(str(params[i]) for i in "abcd")
				break

	def verify_passcode(self):
		if self.__passcode:
			return True

		if self.__hashed_passcode is None:
			self.say("Vous n'avez pas encore défini de mot de passe")
			return False

		self.say("Enoncez votre mot de passe")
		self.await_passcode()

		if not crypto.hashing(self.__passcode) == self.__hashed_passcode:
			self.say("Mot de passe incorrect. Ha.")
			return False

		self.__bankcode = crypto.decode(self.__passcode, self.__encrypted_bankcode)
		return True

	def recall_bankcode(self, params):
		if not self.verify_passcode():
			return

		if self.__bankcode is None:
			self.say("Vous n'avez pas encore enregistré de code bancaire")
			return

		self.say(f"Votre code bancaire est {self.__bankcode}")

	def set_bankcode(self, params):
		if not self.verify_passcode():
			return

		if self.__bankcode is not None:
			if not self.confirm("Un code bancaire est déjà enregistré. Êtes-vous sûr de vouloir le remplacer?"):
				return

		self.say("Énoncez votre nouveau code bancaire")
		self.await_bankcode()

		self.__encrypted_bankcode = crypto.encode(self.__passcode, self.__bankcode)
		
		self.write()
		self.say(f"Votre code bancaire, {self.__bankcode}, a bien été enregistré")

	def set_passcode(self, params):
		if self.__passcode is not None and not self.verify_passcode():
			return

		if self.__passcode is not None:
			if not self.confirm("Un mot de passe est déjà enregistré. Êtes-vous sûr de vouloir le remplacer?"):
				return

		self.say("Enoncez votre nouveau mot de passe")
		self.await_passcode()

		self.__hashed_passcode = crypto.hashing(self.__passcode)

		self.write()
		self.say(f"Votre mot de passe, {self.__passcode}, a bien été enregistré")

	def process(self, action, params):
		exported = {
			"Bankcode_recall": self.recall_bankcode,
			"Bankcode_set": self.set_bankcode,
			"Passcode_set": self.set_passcode,
		}

		if action in exported:
			exported[action](params)
