
import random
from time import sleep, time
from math import ceil
from tabulate import tabulate
from statistics import mean



# Change this to do a different number of sim solves. 
number_solves = 10000  

# Change this to alter how many U-face centres must be solved before
# starting to use U-face centre avoidance (not including buffer). 
# Put 4 for no centre avoidance at all.
u_face_ignore = 0

# Choose whether or not to put the cube in optimal orientation.
does_optimal_orientation = True

cube = []
grounded_count = []

# 4 centres of each colour are on each one of the 6 sides.  
cube_solved = [
    0, 0, 0, 0,
    1, 1, 1, 1, 
    2, 2, 2, 2, 
    3, 3, 3, 3, 
    4, 4, 4, 4, 
    5, 5, 5, 5
]

def print_cube(input = ' '):
    # Print cube formatted in 6 blocks of 4 for ease of reading
    # Can recieve user input if anything wants to be added after
    for i in range(6):
            print(cube[(i*4):(i*4+4)], end='')
    print(input, end='')


def swap(a, b):
    cube[a], cube[b] = cube[b], cube[a]



def face_swap(a, b):
    # Here, 'a' and 'b' correspond to the faces being swapped.
    # Example: '3' would be the 12th index of the cube.
    #
    #                   ooo
    #                 o ### o
    #                 o #0# o
    #                 o ### o
    #             ooo   ooo   ooo   ooo
    #           o ### o ### o ### o ### o
    #           o #4# o #1# o #2# o #3# o
    #           o ### o ### o ### o ### o
    #             ooo   ooo   ooo   ooo
    #                 o ### o
    #                 o #5# o
    #                 o ### o
    #                   ooo
    #
    cube[(a*4):(a*4 + 4)], cube[(b*4):(b*4 + 4)] = \
    cube[(b*4):(b*4 + 4)], cube[(a*4):(a*4 + 4)]


def scramble_cube():
    # Generates list of integers 0-23 in random order
    cube.clear()
    cube.extend(random.sample(range(24), 24))
    # For each integer, takes floor of that integer divided by 4.
    # Since there are 4 centres of each colour, this will allow us to
    # map each integer to its respective colour.
    for i in range(24): cube[i] = int(cube[i] / 4)


def rotation_x():
    # Performs a clockwise rotation along the x-axis of this imaginary cube.
    # This is essentially done by doing a 4-cycle of faces.
    face_swap(0, 3)
    face_swap(0, 5)
    face_swap(0, 1)


def rotation_y():
    # Performs a clockwise rotation along the y-axis of this imaginary cube.
    face_swap(1, 4)
    face_swap(1, 3)
    face_swap(1, 2)


def rotation_z(): 
    # Performs a clockwise rotation along the z-axis of this imaginary cube.
    face_swap(0, 2)
    face_swap(0, 5)
    face_swap(0, 4)

def optimal_orientation():
    # Temporary cube to store the original cube state after the scramble,
    # since many manipulations will be done to find the optimal orientation.
    temp_cube = cube

    # Cube to store the best orientation so far.
    max_swap_cube = []
    max_swap_cube = [piece for piece in cube]

    max_solved_pieces = 0
    # Loop through 4 top colours, doing an x rotation each time.
    for top_colour_i in range(4):
        # Loop through 4 possible front colours for each top colour.
        for front_colour_i in range(4):
            solved_piece_counter = 0
            # Do not count U-face stickers in the total pieces solved.
            for search_sticker in range(4,24):
                # A Fancy-ish check to see if the piece in question is solved.
                if int(cube[search_sticker]) == int(search_sticker / 4):
                    solved_piece_counter += 1
            
            # Update the max counter and max cube when needed.
            if solved_piece_counter > max_solved_pieces:
                max_solved_pieces = solved_piece_counter
                for i in range(24):
                    max_swap_cube[i] = cube[i]
            
            # Rotate to set up new orientation.
            rotation_y()
        # Rotate to set up 4 more new orientations.
        rotation_x()
    # Since U, F, B, D top colours are taken care of, do a z to move on
    # to the L side.
    rotation_z()

    # Same shenanigans as the previous loops
    for front_colour_i in range(4):
        solved_piece_counter = 0
        for search_sticker in range(4,24):
            if int(cube[search_sticker]) == int(search_sticker / 4):
                solved_piece_counter += 1
    
        if solved_piece_counter > max_solved_pieces:
            max_solved_pieces = solved_piece_counter
            for i in range(24):
                    max_swap_cube[i] = cube[i]

    # Perform 2 z rotations to get to the final possible U-face colour,
    # the R colour.
    rotation_z()
    rotation_z()

    # Same stuff
    for front_colour_i in range(4):
        solved_piece_counter = 0
        for search_sticker in range(4,24):
            if int(cube[search_sticker]) == int(search_sticker / 4):
                solved_piece_counter += 1
            
        if solved_piece_counter > max_solved_pieces:
            max_solved_pieces = solved_piece_counter
            for i in range(24):
                    max_swap_cube[i] = cube[i]

    # Clear cube and put in the max cube state. This is the "optimal"
    # orientation.
    cube.clear
    for i in range(24):
        cube[i] = max_swap_cube[i]

def solve_cube(alg_count_count):

    
    alg_count = 0

    # Count the number of solved "u-face" centres. This will be useful to
    # Determine whether or not to allow the program to shoot to a U-face 
    # centre voluntarily. This tries to somewhat-replicate my thinking
    # process during 4bld.
    u_solved_count = cube[1:3].count(0)



    # Let the first piece of this sequence be the "buffer". 
    # The buffer is always first piece of the cycle.
    while cube != cube_solved:

        # If the buffer isn't solved:
        if cube[0] != 0:
            # Search for a non-U face sticker on the four possible
            # places where the piece in the buffer could go
                # Create a variable that corresponds to the first and last of 
                # the 4 targets of the face where the piece in the buffer must
                # go. Also create a variable to know when shooting to a buffer
                # colour target is inevitable
                target_face_start = cube[0] * 4
                target_face_end = target_face_start + 4
                do_skip = 0

                if u_solved_count >= u_face_ignore:
                    for search_sticker, search_piece in \
                        enumerate(cube[target_face_start:target_face_end]):
                        # Search for a piece that is not solved or U colour
                        if (search_piece != cube[0] and
                            search_piece != 0):
                            swap(0, target_face_start + search_sticker)
                            # Change variable to bypass the next loop 
                            do_skip = 1
                            break
                        
                    # Shoot to the buffer when it is inevitable.        
                    if do_skip != 1:
                        swap(0, cube[target_face_start:
                                     target_face_end].index(0) 
                             + target_face_start)
                        

                elif u_solved_count <= u_face_ignore:
                    for search_sticker, search_piece in \
                            enumerate(cube[target_face_start:target_face_end]):
                        # Search for any piece that isn't solved
                        if (search_piece != cube[0]):
                            swap(0, target_face_start + search_sticker)
                            if cube[0] == 0:
                                u_solved_count += 1
                            break

        # If all "U-face" stickers are solved, search for an unsolved
        # piece to shoot to. Once again likely inefficient programming.
        elif cube[0:4].count(0) == 4:
            for search_sticker, search_piece in enumerate(cube[4:24]):
                if search_piece != int((search_sticker + 4) / 4):
                    swap(0, search_sticker + 4)
                    break    
        # If there is a "U-face" piece unsolved, shoot there      
        else:
            for search_piece in range(1,4):
                if cube[search_piece] != 0:
                    swap(0, search_piece)
                    break
        
        # Since we are doing 2swaps, only add 0.5
        alg_count += 0.5
    # If there is an odd number of swaps, you would normally shoot U face
    # to U face for the last target of the last comm, but programming this
    # is just the same as rounding up. Append to the list of algcounts.
    alg_count_count.append(ceil(alg_count))
    if ((len(alg_count_count) % 10000) == 0): 
        print(f"{len(alg_count_count)} out of {number_solves}, \
              {int(len(alg_count_count) * 100 / number_solves)} % Done")

def make_table(a):
    # Makes a table of results, containing each alg count and the
    # number of times it shows up, as well as the percentage.
    table = []
    # Get a single one of every alg count that appears in the list.
    alg_counts = sorted(set(a))
    # Count the number of times a specific alg count shows up.
    for unique_alg_count in alg_counts:
        counter = 0
        for algcount in a:
            if algcount == unique_alg_count:
                counter += 1
        # Add info to the table.
        table.append([unique_alg_count, counter, round((counter * 100 / number_solves), 2)])
    # Add Total and Average.
    table.append(["Total", number_solves, "100.00"])
    table.append(["Average", mean(grounded_count), '---'])
    # Print out table with some breathing room around it.
    print('\n')
    print(tabulate(table, headers=("Alg Count", "Amount", "Percent (%)"),
          tablefmt="fancy_grid", numalign="left"))
    print('\n')
    pass

def main():
 
    for i in range(number_solves):
        scramble_cube()
        if does_optimal_orientation == True:
            optimal_orientation()
        solve_cube(grounded_count)
    make_table(grounded_count)

main()
