
class Bullet:
    bullets = []

    def __init__(self, x, y, velocity_vector, colour):
        self.x = x
        self.y = y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.colour = colour

        bullets.append(self)

    def update():
        self.x += self.velocity_x
        self.y += self.velocity_y
    
    def display(self)


    @staticmethod
    def display_all():
        for bullet in bullets:
            bullet.display()
