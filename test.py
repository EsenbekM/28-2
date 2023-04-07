from decouple import config

name = config("NAME", default="Uniknown")
print(name)
