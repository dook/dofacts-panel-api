AUTH_USER_MODEL = "users.User"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
    {"NAME": "dook.users.validators.UppercaseValidator",},
    {"NAME": "dook.users.validators.LowercaseValidator",},
    {"NAME": "dook.users.validators.SymbolValidator",},
]

PASSWORD_RESET_TIMEOUT_DAYS = 1
