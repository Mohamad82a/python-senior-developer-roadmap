
def show_profile(**kwargs):
    for key, value in kwargs.items():
        print(f"{key} = {value}")

show_profile(name="A", age=20, city="Beijing")
