import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import argparse


ON: int = 255
OFF: int = 0


def random_grid(N: int = 3) -> np.ndarray:
    """Sets the initial state of the grid by randomly assigning 0 or 255 to each cell
    
    Parameters:
        N (int): The number of columns and rows in the grid. Default is 3.

    Returns:
        np.ndarray: The grid with the initial state of random 0s and 255s
    """
    return np.random.choice(
                [ON, OFF], 
                N**2, 
                p=[0.5, 0.5]
            ).reshape(N, N)
    

def add_glider(i: int, j: int, grid: np.ndarray) -> None:
    """Adds a gliding object at the cell (i, j) of the grid
    
    NOTE: In order for this to work as a glider, the grid must be empty except for the glider and at least 3x3 in size
    
    Parameters:
        i (int): The row number of the top left cell of the glider
        j (int): The column number of the top left cell of the glider
        grid (np.ndarray): The grid to add the glider to

    Returns:
        np.ndarray: The grid with the glider added
    """
    glider = np.array([[OFF, OFF, ON],
                       [ON, OFF, ON],
                       [OFF, ON, ON]])
    grid[i:i+3, j:j+3] = glider
    

def apply_rules(cell: int, total: int) -> int | None:
    """Applies the rules of Conway's Game of Life to a single cell
    
    Parameters:
        cell (int): The current state of the cell
        total (int): The total number of ON cells in the cell's neighbourhood
        
    Returns:
        int: The new state of the cell
    """
    if cell == ON:
        if (total < 2) or (total > 3):
            return OFF
    else:
        if total == 3:
            return ON


def initialize_simulation( glider: bool | None, N: int = 3) -> np.ndarray:
    """Initializes the simulation by setting the initial state of the grid

    Args:
        glider (bool): Whether or not to add a glider to the grid
        N (int, optional): The number of columns and rows in the grid. Defaults to 3.

    Returns:
        np.ndarray: The grid with the initial state of the simulation
    """
    if glider:
        grid = np.zeros(N*N).reshape(N, N)
        add_glider(1, 1, grid)
    else:
        grid = random_grid(N)
    
    return grid


def get_neighbourhood_sum(i: int, j: int, grid: np.ndarray, N: int = 3) -> int:
    """Calculates the sum of the cell's neighbourhood

    Args:
        i (int): The row number of the cell
        j (int): The column number of the cell
        grid (np.ndarray): The grid with the current state of the simulation
        N (int, optional): The number of columns and rows in the grid. Default is 3.

    Returns:
        int: The sum of the cell's neighbourhood
    """
    return int((
                    grid[i, (j-1)%N] + grid[i, (j+1)%N] +
                    grid[(i-1)%N, j] + grid[(i+1)%N, j] +
                    grid[(i-1)%N, (j-1)%N] + grid[(i-1)%N, (j+1)%N] +
                    grid[(i+1)%N, (j-1)%N] + grid[(i+1)%N, (j+1)%N]
                )/ON)


def update(frame_num: int, img, grid: np.ndarray, N: int = 3) -> None:
    """Calculates the next state of the grid and updates the image

    Args:
        frame_num (int): The current frame number
        img (plt.imshow): The image to update
        grid (np.ndarray): The grid with the current state of the simulation
        N (int, optional): The number of columns and rows in the grid. Default is 3.
    """
    new_grid = grid.copy()
    
    for i in range(N):
        for j in range(N):
            total = get_neighbourhood_sum(i, j, grid, N)
            
            new_cell = apply_rules(grid[i, j], total)
            
            if new_cell is not None:
                new_grid[i, j] = new_cell
            
    img.set_data(new_grid)
    grid[:] = new_grid[:] # The `[:]` are needed to update the grid in place and not create a new one
    
    return img


def animate_simulation(grid: np.ndarray, interval: int, file: str, N: int = 3) -> None:
    """Sets up the animation of the simulation
    
    Parameters:
        grid (np.ndarray): The grid with the initial state of the simulation
        interval (int): The interval between frames in milliseconds
        file (str): The name of the .mov file to save the animation to
        N (int): The number of columns and rows in the grid. Default is 3.
    """
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')
    
    anim = animation.FuncAnimation(fig, update,
                                      fargs=(img, grid, N),
                                      interval=interval,
                                      save_count=50
                                    )
    
    if file:
        anim.save(file) # FIXME: This will only accept .gif files. 
        # FIXME: Find a way to save a larger or smaller duration video file
        
    plt.show()
    

def main():
    parser = argparse.ArgumentParser(description="Runs Conway's Game of Life simulation")
    
    parser.add_argument('-g','--grid-size', dest='N', required=False, type=int, default=100, help='Specify the size of the grid (N x N)')
    parser.add_argument('-m','--mov-file', dest='movfile', required=False, help='Specify the name of the .mov file to save the animation to')
    parser.add_argument('-i','--interval', dest='interval', required=False, type=int, default=50, help='Specify the interval between frames in milliseconds')
    parser.add_argument('--glider', action='store_true', required=False, help='Add a glider with top left cell at (1, 1) to the grid')
    args = parser.parse_args()
    
    if args.N < 3:
        raise ValueError("The grid size must be at least 3x3")
    else:
        N = args.N
        
    update_interval = args.interval
    
    grid = initialize_simulation(args.glider, N)
    
    animate_simulation(grid, update_interval, args.movfile, N)

if __name__ == "__main__":
    main()