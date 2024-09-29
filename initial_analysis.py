import pandas as pd
import numpy as np

#Path to control and treatment trajectory files 
controls = [r"data\session_Control4thRun1\trajectories\with_gaps_csv\trajectories.csv", 
            r"data\session_Control4thRun2\trajectories\with_gaps_csv\trajectories.csv", 
            r"data\session_Control4thRun3\trajectories\with_gaps_csv\trajectories.csv"]

treatment = [r"data\session_Treatment4thRun1\trajectories\with_gaps_csv\trajectories.csv", 
             r"data\session_Treatment4thRun2\trajectories\with_gaps_csv\trajectories.csv", 
             r"data\session_Treatment4thRun3\trajectories\with_gaps_csv\trajectories.csv"]


def calculate_velocity_and_length(filename):
    # Load the data
    data = pd.read_csv(filename)
    
    # Initialize results
    results = {}
    
    # Frames per second
    fps = 30
    time_interval = 1 / fps
    
    # Iterate over each pair of columns (x, y) for each animal
    for i in range(1, len(data.columns)//2 + 1):
        x_col = f'x{i}'
        y_col = f'y{i}'
        
        # Drop rows with NaN values for this animal
        animal_data = data[[x_col, y_col]].dropna()
        
        if len(animal_data) < 2:
            continue
        
        # Calculate differences between consecutive points
        dx = np.diff(animal_data[x_col])
        dy = np.diff(animal_data[y_col])
        
        # Calculate velocities (distance per time_interval)
        distances = np.sqrt(dx**2 + dy**2)
        velocities = distances / time_interval
        
        # Calculate total trajectory length
        total_length = np.sum(distances)
        
        # Store results
        results[f'animal_{i}'] = {
            'velocities': velocities,
            'total_length': total_length
        }
    
    return results

#Create dictionary for control results 
control_dict = {}
for i, file in enumerate(controls):
    control_dict[f'Control_{i}'] = calculate_velocity_and_length(file)


#Create dictionary for treatment dictionary. 
treatment_dict = {}
for i, file in enumerate(treatment): 
    treatment_dict[f'Treatment_{i}'] = calculate_velocity_and_length(file)




# Print results
print("For the control we see: ")
for number, results in control_dict.items(): 
    print(f"{number}: ")
    for animal, metrics in results.items():
        print(f"{animal}: Total Length = {metrics['total_length']:.2f}, Avg Velocity = {np.mean(metrics['velocities'])}")

print("\nFor the treatment we see: ")
for number, results in treatment_dict.items(): 
    print(f"{number}: ")
    for animal, metrics in results.items(): 
        print(f"{animal}: Total Length = {metrics['total_length']:.2f}, Avg Velocity = {np.mean(metrics['velocities'])}")