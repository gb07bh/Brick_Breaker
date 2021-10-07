#Created  on 23 May 2021


# Author : gb07bh


import tkinter as tk



# Class and Funtion for components

class PlayComponent(object):

    def __init__(self, canvas, item):

        self.item = item

        self.canvas = canvas


# Function for moving

    def move(self, x, y):

        self.canvas.move(self.item, x, y)


#function for position

    def position(self):

        return self.canvas.coords(self.item) 


# Funtion to delete

    def delete(self):

        self.canvas.delete(self.item)


#Creating Objects

# 1. Paddle

#Class Paddle

class Paddle(PlayComponent):

    def __init__(self, canvas, x, y):

        self.height = 5

        self.width = 100

        self.ball = None

        item = canvas.create_rectangle(x-self.width/2,      # The size of rectangle or the corners of the rectangle

                                        y-self.height/2,    # Try changing the height and width

                                        x+self.width/2,

                                        y+self.height/2,

                                        fill = 'green')

        super(Paddle, self).__init__(canvas, item)


    def set_ball(self, ball):

        self.ball = ball   
        

# Moving the Paddle 

    def move(self, distance):

        coord = self.position()

        width = self.canvas.winfo_width() # Keeps object safe from the window resizing

        if coord[2] + distance <= width and coord[0] + distance >= 0:

            super(Paddle,self).move(distance, 0)

            if self.ball is not None:

                self.ball.move(distance, 0)

# Class for Brick

class Brick(PlayComponent):

    colorArray = {1:'Lightsteelblue',2:'Royalblue', 3:'Blue'}


    def __init__(self, canvas, x, y, hits):

        self.width = 60

        self.height = 20
        self.hits = hits

        color = Brick.colorArray[hits]

        item = canvas.create_rectangle(x - self.width/2,

                                        y - self.height/2,

                                        x + self.width/2,

                                        y + self.height/2,

                                        fill = color, tag = 'brick')

        super(Brick,self).__init__(canvas, item)


    def hit(self):

        self.hits -= 1

        if self.hits == 0:
            self.delete()

        else:

            self.canvas.itemconfig(self.item, fill = Brick.colorArray[self.hits])

        



# Class for Ball

class Ball(PlayComponent):

    def __init__(self, canvas, x, y):

        self.radius = 6

        self.speed = 10

        self.direction = [-1,1]

        item = canvas.create_oval(x - self.radius,

                                y - self.radius,

                                x + self.radius,

                                y + self.radius,

                                fill = 'red')

        super(Ball,self).__init__(canvas, item)

    def update(self):

        coord = self.position()
        width = self.canvas.winfo_width()

        if coord[1] <= 0:                       #Balls direction changes and updates
            self.direction[1] *= -1

        if coord[2] >= width or  coord[0] <= 0:
            self.direction[0] *= -1


        x = self.direction[0] * self.speed
        y = self.direction[1] * self.speed
        self.move(x, y)


    def intersect(self, components):

        coord = self.position()
        x = (coord[0]+coord[2])*0.5

        if len(components) == 1:
            component = components[0]
            coord = component.position()
            if x < coord[0]:
                self.direction = -1  # When ball travels and hits then direction changes
            elif x > coord[2]:
                self.direction = 1
            else:
                self.direction[1] *= -1
        elif len(components) > 1:
            self.direction[1] *= -1


           # Collision 

        for component in components:

            if isinstance(component, Brick):

                component.hit()


######    MAIN FUNCTION    ########

class Game(tk.Frame):

    def __init__(self,master):

        super(Game,self).__init__(master)

    # Window Settings

        self.lives = 3
        self.brick_points = 25

        self.width = 1000

        self.height = 400

        self.canvas = tk.Canvas(self, bg = 'cornsilk',

                                width = self.width,

                                height = self.height) 

        # Positioning Elements in the window

        self.canvas.pack()

        self.pack()


        self.items = {}

        self.ball = None

        # below line represents the position of paddle try changing it to understand.

        self.paddle = Paddle(self.canvas,self.width/2, 320)

        self.items[self.paddle.item] = self.paddle


        #All Bricks to be displayed

        for x in range(100, self.width - 100 , 60):

            self.display_brick(x + 20, 50 , 2) #hits is 2 

            self.display_brick(x + 20, 70 , 1) #hits is 1

            self.display_brick(x + 20, 120, 1) #hits is 1
        

        # Moving the paddle


        self.hud = None

        self.init_game()

        self.canvas.focus_set()

        self.canvas.bind('<Left>',

                        lambda _:self.paddle.move(-30))

        self.canvas.bind('<Right>',

                        lambda _:self.paddle.move(+30))                   


    def init_game(self):

        self.update_lives_text()

        self.display_ball()

        self.text = self.draw_text(self.width/2, self.height/2, 'Press "S" to Start')

        self.canvas.bind('<s>',lambda _: self.start_game())
    

    # Display Ball

    def display_ball(self):

        if self.ball is not None:

            self.ball.delete()

        paddle_coords = self.paddle.position()

        x = (paddle_coords[0] + paddle_coords[2]) * 0.5

        self.ball = Ball(self.canvas, x , 310)

        self.paddle.set_ball(self.ball)


    # Displaying brick


    def display_brick(self, x, y ,hits):

        brick = Brick(self.canvas, x, y, hits)

        self.items[brick.item] = brick
    

    # SHowing on the screen

    def draw_text(self, x, y, text, size = '50'):

        font = ('Arial', size)

        return self.canvas.create_text(x , y, text = text , font = font)


    # Updating lives

    def update_lives_text(self):

        text = 'Lives: %s'%self.lives

        if self.hud is None:

            self.hud = self.draw_text(50, 20, text, 15) 

        else:

            self.canvas.itemconfig(self.hud,text = text)


    def start_game(self):

        self.canvas.unbind('<s>')

        self.canvas.delete(self.text)

        self.paddle.ball = None

        self.game_loop()


    def game_loop(self):

        self.verify_intersection()

        num_bricks = len(self.canvas.find_withtag('brick'))


        if num_bricks == 0:

            self.ball.speed = None

            self.draw_text(self.width/2, self.height/2," You Win!!")

        elif self.ball.position()[3] >= self.height:

            self.ball.speed = None

            self.lives -= 1

            if self.lives == 0:

                self.draw_text(self.width/2, self.height/2," Game Over")

            else:

                self.after(1000,self.init_game())

        else:

            self.ball.update()

            self.after(50,self.game_loop)


    # Confirming Collision
        

    def verify_intersection(self):

        ball_coords = self.ball.position()

        items = self.canvas.find_overlapping(*ball_coords)

        objects = [self.items[x] for x in items if x in self.items]
        self.ball.intersect(objects)
    
   

    



if __name__ == '__main__':

    root = tk.Tk()

    root.title('Brick Breaker')

    game = Game(root)

    game.mainloop()