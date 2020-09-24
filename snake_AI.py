import random
import curses

s = curses.initscr()
curses.curs_set(0)
sh, sw = s.getmaxyx()
w = curses.newwin(sh, sw, 0, 0)
w.keypad(1)
w.timeout(1)

snk_x = int(sw/4)
snk_y = int(sh/2)
snake = [
    [snk_y, snk_x],
    [snk_y, snk_x-1],
    [snk_y, snk_x-2]
]

food = [int(sh/2), int(sw/2)]
w.addch(int(food[0]), int(food[1]), curses.ACS_PI)




# return the same head if no wall around
# return the new position crossing the wall on the right otherwise
def cross_wall(snake_head):
    if snake_head[1]>=sw-2: # only right border because snake never goes left
        # touching right so appears left (same height)
        return [snake_head[0], 2]
    else:
        return snake_head


# Never go left
# always up (to the top) or down (to the bottom)
# if too close to tail
# move toward center of screen or food otherwise

def AI(snake):
    X_snake = snake[0][0]
    Y_snake = snake[0][1]

    # keep going right if no snake tail at least 2 y-axis points further away
    # and if food also away

    # gather all Y to check if current Y further away for Ys
    Y_snakes = []
    for pos in snake:
        Y_snakes.append(pos[1])

    # set the current Y to what it would be if 1/2/3 y-axis points more
    Y_potential1 = Y_snake + 1
    Y_potential2 = Y_snake + 2
    Y_potential3 = Y_snake + 3

    # in case the Y_potential are crossing the wall
    if Y_potential3 >= sw-3 and Y_potential2 < sw-3 and Y_potential1 < sw-3:
        Y_potential3 = 3
    elif Y_potential3 >= sw-3 and Y_potential2 >= sw-3 and Y_potential1 < sw-3:
        Y_potential2 = 3
        Y_potential3 = 4
    elif Y_potential3 >= sw-3 and Y_potential1 >= sw-3 and Y_potential2 >= sw-3:
        Y_potential1 = 3
        Y_potential2 = 4
        Y_potential3 = 5



    # if food further away and no tail within the next 3 y-axis points
    if Y_snake != food[1] and Y_potential1 not in Y_snakes and Y_potential2 not in Y_snakes and Y_potential3 not in Y_snakes:
        
        # move snake toward middle of screen if not already there 
        # move up or down toward center (if possible) otherwise
        if X_snake in [sh/2 -1, sh/2, sh/2 +1]:
            snake_new_head = [X_snake, Y_snake + 1]
        elif X_snake < sh/2:
            snake_new_head = [X_snake + 1, Y_snake]
            if snake_new_head in snake:
                snake_new_head = [X_snake, Y_snake + 1]
        elif X_snake > sh/2:
            snake_new_head = [X_snake -1, Y_snake]
            if snake_new_head in snake:
                snake_new_head = [X_snake, Y_snake + 1]

    # if snake already on same y-axis
    elif Y_snake == food[1]:
        # move toward the food if possible, move right otherwise
        if food[0] > X_snake:
            snake_new_head = [X_snake + 1, Y_snake]
            if snake_new_head in snake[:]:
                snake_new_head = [X_snake, Y_snake + 1]
        elif food[0] < X_snake:
            snake_new_head = [X_snake - 1, Y_snake]
            if snake_new_head in snake[:]:
                snake_new_head = [X_snake, Y_snake + 1]
    
    # if food further away but tail is close (within the next 3 y-axis points)
    else: 
        # snake was going up 
        if X_snake == snake[1][0] + 1: 
            # if wall coming, move right
            if X_snake == sh-3 and snake[1][1] == Y_snake:
                snake_new_head = [X_snake, Y_snake + 1]
            # if wall coming, and already moved right, go down
            elif X_snake == sh-3 and snake[1][1] == Y_snake + 1:
                snake_new_head = [X_snake - 1, Y_snake]
            # if no wall coming, keep going up
            else:
                snake_new_head = [X_snake + 1, Y_snake]
                if snake_new_head in snake:
                    snake_new_head = [X_snake, Y_snake + 1]
        # snake was going down 
        elif X_snake == snake[1][0] - 1: 
            # if wall coming, move right
            if X_snake == 3 and snake[1][1] == Y_snake:
                snake_new_head = [X_snake, Y_snake + 1]
            # if wall coming, and already moved right, go up
            elif X_snake == 3 and snake[1][1] == Y_snake + 1:
                snake_new_head = [X_snake + 1, Y_snake]
            # if no wall coming, keep going down
            else:
                snake_new_head = [X_snake - 1, Y_snake]
                if snake_new_head in snake:
                    snake_new_head = [X_snake, Y_snake + 1]
        # snake was moving right
        else: 
            # snake at the bottom so move up
            if X_snake == 3:
                snake_new_head = [X_snake + 1, Y_snake]
            # snake move down (could have been up)
            else:
                snake_new_head = [X_snake - 1, Y_snake]

    return snake_new_head   





key = curses.KEY_RIGHT

while True:
    next_key = w.getch()
    key = key if next_key == -1 else next_key

    # Check if snake is touching wall or itself
    if snake[0][0] in [0, sh] or snake[0][1]  in [0, sw] or snake[0] in snake[1:]:
        curses.endwin()
        print("Success!")

    # AI chooses the next move
    snake_new_head = AI(snake)
    # snake cross the right wall if necessary
    snake_new_head = cross_wall(snake_new_head)


    # Make the move
    snake.insert(0, snake_new_head)

    if snake[0] == food:
        food = None
        while food is None:
            nf = [
                random.randint(3, sh-3),
                random.randint(3, sw-3)
            ]
            food = nf if nf not in snake else None
        w.addch(food[0], food[1], curses.ACS_PI)
    else:
        tail = snake.pop()
        w.addch(int(tail[0]), int(tail[1]), ' ')

    w.addch(int(snake[0][0]), int(snake[0][1]), curses.ACS_CKBOARD)

