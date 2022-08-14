from django.core.exceptions import ValidationError


def password_validate(param):
    special_symbols = ['!', '@', '#', '%']

    if len(param) < 8:
        raise ValidationError("Hasło musi składać się przynajmniej z 8 znaków.")
    elif not any(char.isupper() for char in param):
        raise ValidationError("Hasło powinno zawierać przynajmniej jedną wielką literę.")
    elif not any(char.isdigit() for char in param):
        raise ValidationError("Hasło powinno zawierać przynajmniej jedną cyfrę.")
    elif not any(char.islower() for char in param):
        raise ValidationError("Hasło powinno zawierać przynajmniej jedną małą literę.")
    elif not any(char in special_symbols for char in param):
        raise ValidationError("Hasło powinno zawierać przynajmniej jeden ze znaków !, @, #, %.")