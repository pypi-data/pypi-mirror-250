def emailverii(email):
    if email.endswith("@gmail.com"):
        return print(f"{email} is a valid Gmail address.")
    else:
        return print(f"{email} is not a valid Gmail address.")