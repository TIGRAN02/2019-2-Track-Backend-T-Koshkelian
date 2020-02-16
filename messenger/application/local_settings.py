DEBUG = True

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'messenger',
    'USER': 'tigran',
    'PASSWORD': 'tigrkoshka',
    'HOST': 'localhost',
    'PORT': '5432',
  }
}
