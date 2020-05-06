class PlayerCharacter:

    def __init__(self, user, character_name: str):
        self.user = str(user)
        self.character_name = character_name
        self.friend = None
        self.enemy = None

    def __repr__(self):
        return "{} ({})".format(self.character_name, self.user)

    def __str__(self):
        return "{} ({})".format(self.character_name, self.user)


class NonPlayerCharacter:

    def __init__(self, user, character_name: str):
        self.user = str(user)
        self.character_name = character_name

    def __repr__(self):
        return "{} was created by {}.\n".format(self.character_name, self.user.name)