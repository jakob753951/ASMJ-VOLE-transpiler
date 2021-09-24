class Type:
	int = 1
	float = 2


class Variable:
	def __init__(self, name: str, type_: Type):
		self.Name = name
		self.Type_: Type = type_