class animal:
    friends = []

    def __init__(self,height=120, weight=200):
        self.height = height
        self.weight = weight


    def print_height(self):  # The self here indicates that that it takes in all the self attributes as a parameter
        print(f'{self.height}')


    def return_fur_color(self):
        return self.fur_color
    

    def set_height(self, height):
        self.height = height

    def return_friends(self):
        return self.friends
    

class Dog(animal):
    def __init__(self,height, weight, fur_color):
         super().__init__(height, weight)
         self.fur_color = fur_color

    @staticmethod
    def greet():
        print('Woof woof')

    @classmethod
    def farewell(self):
        print('Bark')


dog1 = Dog(100,150,'red')

print(dog1.fur_color)
dog1.greet()
dog1.farewell()
Dog.farewell()

print(dog1.friends)
dog1.friends.append('Freddy')
print(dog1.friends)
print(Dog.friends)

