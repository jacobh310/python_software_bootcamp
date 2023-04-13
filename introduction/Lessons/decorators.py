def response_to_mailman(func):
    def wrapper(*args, **kwargs):
        print("The mailman is coming")
        response = func(*args, **kwargs)
        return response

    return wrapper


def bark():
    print("woof")

bark()
wrapped = response_to_mailman(bark)
wrapped()

@response_to_mailman  # the decorator does what response_to_mailman(bark) does
def bark():
    print("woof")

@response_to_mailman
def cat_response():
    print('meow')

bark()
cat_response()

@response_to_mailman
def make_sound(sound):  # need *args, and **kwargs to run this
    print(sound *2)

make_sound('Hey')

def conjure_sound(sound):  
    return sound *2


# ------------------------------------------------

def response_to_approacher(name, apporaching=True):
    def inner_response(func):    
        def wrapper(*args, **kwargs):
            if apporaching:
                print(f"The {name} is coming")
            else:
                print(f"The {name} is leaving")
            response = func(*args, **kwargs)
            
            return response
        return wrapper
    return inner_response

@response_to_approacher('Milkman', False)
def conjure_sound(sound):  
    print(sound *2)

conjure_sound('Munch')
