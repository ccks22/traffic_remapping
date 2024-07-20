import pandas as pd

# Load the dataset
data = pd.read_csv("flow_stats.csv")

# Feature engineering
data['PacketLossRate'] = data['LostPackets'] / data['TxPackets']
data['AverageDelay'] = data['DelaySum'] / data['RxPackets']
data['AverageJitter'] = data['JitterSum'] / data['RxPackets']
data['Throughput'] = data['RxBytes'] / (data['TxPackets'] * 1024) # in KB

# Selecting features for the model
features = data[['TxPackets', 'RxPackets', 'Throughput', 'PacketLossRate', 'AverageDelay', 'AverageJitter']]
labels = data['Label'] # assuming you have a 'Label' column with normal/fraudulent labels
