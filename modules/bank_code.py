import crypto
import module

class Bankcode(module.Module):
	def __init__(self, rhasspy):
		super().__init__(rhasspy)

		self.__bankcode = None
		self.__passcode = None

		try:
			self.read()

		except FileNotFoundError:
			self.__encrypted_bankcode = None
			self.__hashed_passcode = None

	def read(self):
		self.__encrypted_bankcode, self.__hashed_passcode = read_user_data("bankcode")

	def write(self):
		write_user_data("bankcode", "\n".join((self.__encrypted_bankcode, self.__hashed_passcode)))

	def await_bankcode(self):
		while True:
			action, params = self.intent()

			if action == "Bankcode":
				self.__bankcode = sum(params[str(i)] for i in "abcd")
				break

	def await_passcode(self):
		while True:
			action, params = self.intent()

			if action == "Passcode":
				self.__passcode = sum(params[str(i)] for i in "abcd")
				break

	def verify_passcode(self):
		if self.__passcode:
			return True

		self.say("Enoncez votre mot de passe")
		self.await_passcode()

		if not crypto.hashing(self.__passcode) == self.__hashed_passcode:
			self.say("Mot de passe incorrect. Ha.")
			return False

		self.__bankcode = crypto.decode(self.__passcode, self.__encrypted_bankcode)
		return True

	def recall_bankcode(self, action, params):
		if not verify_passcode(self):
			return

		if self.__bankcode is None:
			self.say("Vous n'avez pas encore enregistré de code bancaire")
			return

		self.say(f"Votre code bancaire est {self.__bankcode}")

	def set_bankcode(self, action, params):
		if not verify_passcode(self):
			return

		if self.__bankcode is not None:
			if not self.confirm("Un code bancaire est déjà enregistré. Êtes-vous sûr de vouloir le remplacer?"):
				return

		self.say("Énoncez votre nouveau code bancaire")
		self.await_bankcode()

		self.__encrypted_bankcode = crypto.encode(self.__passcode, self.__bankcode)
		
		self.write()
		self.say("Votre code bancaire a bien été enregistré")

	def set_passcode(self, action, params):
		if not verify_passcode(self):
			return

		if self.__passcode is not None:
			if not self.confirm("Un mot de passe est déjà enregistré. Êtes-vous sûr de vouloir le remplacer?"):
				return

		self.say("Enoncez votre nouveau mot de passe")
		self.await_passcode()

		self.__hashed_passcode = crypto.hashing(self.__passcode)

		self.write()
		self.say("Votre mot de passe a bien été enregistré")

	def process(self, action, params):
		exported = {
			"Bankcode_recall": recall_bankcode,
			"Bankcode_set": set_bankcode,
			"Passcode_set": set_passcode,
		}

		if action in exported:
			exported[action](params)
