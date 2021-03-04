def get_token(name):
    with open(f"tokens/{name}.token", "r") as file:
        return file.read()
