from decouple import config
print(repr(config('DEBUG', default=False, cast=bool)))
print(repr(config('ALLOWED_HOSTS', default='localhost,127.0.0.1,bollo.onrender.com')))
