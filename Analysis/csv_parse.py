import pandas as pd

# This script parses the csv we get from the mario kart simulator and returns MATLAB-readable tables for each of the 8 agents
# This WILL overwrite everything in .\parsed_agent_data

# Read into pandas df
# NOTE: need to add col headers to converter dict! 
# This tells it that we're passing a list to the pd dataframe and not a string
# The csv file MUST be in the Data folder!
df = pd.read_csv('.\Data\mario_kart_data_6FEB25_v2.csv', converters={'x_position': eval, 
                                                    'y_position': eval})
# Confirm it looks ok
print(df)

# Save off the step numbers first
ts = df['step']
ts = list(ts)

# Get pandas series of the desired data - should match dict above!
x_pos = df['x_position']
y_pos = df['y_position']

# Na ==  num agents. Nt == num time steps
Na = len(x_pos[0])
Nt = len(ts)

# Loop over each agent
for j in range(Na):

    # For the j'th agent only
    x_pos_series, y_pos_series = [], []
    for i in range(Nt):
        # Extract out the list of all agents' positions at time i
        # Should be consistent with above!
        x_pos_agents = x_pos[i]
        x_pos_series.append(x_pos_agents[j]) # read off the first agent
        
        # Now do for other positions as well
        y_pos_agents = y_pos[i]
        y_pos_series.append(y_pos_agents[j])

    data = {} # clear from previous j
    data = {'x_position': x_pos_series,
            'y_position': y_pos_series}
    agent_j = pd.DataFrame(data)
    print(agent_j)
    
    # get the j'th name
    csv_name = 'parsed_agent_data\mario_kart_data_agent' + str(j+1) + '.csv'
    agent_j.to_csv(csv_name)


