class animal:
    fur_color = 'grey'
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

animal_1 = animal(80, 150)
animal_2 = animal(70, 130)
animal_3 = animal()

animal_1.print_height()
animal_2.print_height()

print(animal_1.friends, animal_2.friends)

animal_3.friends.append('Jerry')

print(animal_1.friends, animal_2.friends)

animal_3.print_height()

animal_3.set_height(69)

print(animal_3.height)
