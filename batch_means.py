import matplotlib.pyplot as plt
import numpy as np

# Sample data:
# 1, 0.1, 0.2, 73
# 1, 0.11, 0.1, 101
# 2, 0.23, -0.01, 17
# 2, 0.9, 0.82, 23
#
# Pretend this is taken from two (or more) different experiments:
# batch 1 and batch 2.

            
# This function reads in a CSV file with four columns (batch, x, y, and val) and returns a dictionary where each key is a batch number and the corresponding value is a list of tuples containing the x, y, and val values for that batch.
def read_data(filename):
    data = {}
    with open(filename, 'r') as file:
        for line in file:
            try:
                batch, x, y, val = map(float, line.split(','))
            except ValueError:
                print(f"Warning: wrong input format for entry: {line}")
                continue
            if batch not in data:
                data[batch] = []
            data[batch].append((x, y, val))
    return data

# This function takes the dictionary of data from read_data and computes the average of the val values for each batch. It returns a new dictionary where each key is a batch number and the corresponding value is the average val for that batch.
def compute_average(data):
    result = {}
    for batch, samples in data.items():
        n = 0
        x_sum = 0
        for x, y, val in samples:
            if x**2 + y**2 <= 1:
                x_sum += val
                n += 1
        result[batch] = x_sum / n if n > 0 else 0
    return result

# This function takes the dictionary of data from read_data and generates a scatter plot of the data. It also annotates each point with its val value and adds a unit circle to the plot.
def plot_data(data,f):
    x = [point[0] for batch in data.values() for point in batch]
    y = [point[1] for batch in data.values() for point in batch]
    val = [point[2] for batch in data.values() for point in batch]
    
    fig, ax = plt.subplots()

    cmap = plt.get_cmap("viridis")
    color_list = cmap(np.linspace(0, 1, len(data.keys())))
    
    # Define the colors for each batch
    color_dict = {1: "blue", 2: "green", 3: "red", 4: "black", 5: "yellow"}
    
    # Plot the data points
    for i, (batch_key, batch) in enumerate(data.items()):
        if batch_key not in color_dict:
            continue
        color = color_dict[batch_key]
        batch_x = [point[0] for point in batch]
        batch_y = [point[1] for point in batch]
        ax.scatter(batch_x, batch_y, c=color, label=batch_key)

    # Annotate each point with its val value
    for i, txt in enumerate(val):
        ax.annotate(txt, (x[i]+0.0175, y[i]+0.0175), fontsize=7)

    # Add the circle
    circle = plt.Circle((0,0), 1, color='black', fill=False)
    ax.add_artist(circle)

    # Add buffer on each side of the x and y axes
    x_buffer = 0.05 * (1 - (-1))
    y_buffer = 0.05 * (1 - (-1))
    plt.xlim(-1 - x_buffer, 1 + x_buffer)
    plt.ylim(-1 - y_buffer, 1 + y_buffer)

    plt.xticks(np.arange(-1, 1.25, 0.25))
    plt.yticks(np.arange(-1, 1.25, 0.25))
    
    # Saves it as a PDF file
    plt.savefig(f.replace("csv", "pdf"))
    plt.show()


# Define a function called "main" to perform the following tasks:
def main():
    # Ask the user to input a filename for a CSV file to be analyzed.
    filename = input("Which csv file should be analyzed? ")
    try:
        # Try to read the data from the specified file using the "read_data" function.
        data = read_data(filename)
    except FileNotFoundError:
        # If the file is not found, print an error message and exit the function.
        print("Could not find file.")
        return
    # Compute the averages of each batch from the data using the "compute_average" function.
    averages = compute_average(data)
    # Print the batch and average values in sorted order (if the average is greater than 0) to the console.
    print("Batch\tAverage")
    s_a = sorted(averages.items())
    sort_average = dict(s_a)
    for batch, average in sort_average.items():
        if average > 0:
            print(batch, "\t", average)
    # Plot the data using the "plot_data" function.
    plot_data(data, filename)
    # Print a message indicating that the file was created and exit the function.
    print("File created, Goodbye!")

# Check for the special variable "__name__" to determine whether the "main" function should be executed.
if __name__ == '__main__':
    # If the code is run as a script, execute the "main" function.
    main()


# The idea with this idiom is that if this code is loaded as a module,
# then the __name__ variable (internal to Python) is not __main__ and
# the body of the program is not executed. Consider what would happen
# if the main function was not in a function: an import statement (for
# example "import o4") would load the functions and then executed
# "filename = input(...)" and that is probably not what you want. The
# idiom is simply an easy way of ensuring that some code is only
# executed when run as an actual program.
#
# Try it out by importing this file into another project!
    
