import pandas as pd
import numpy as np

# Define parameters
num_samples = 1000
np.random.seed(42)

# Generate synthetic data
data = {
    'Packet Size': np.random.uniform(50, 1500, num_samples),
    'Source IP': [f'{np.random.randint(1, 255)}.{np.random.randint(1, 255)}.{np.random.randint(1, 255)}.{np.random.randint(1, 255)}' for _ in range(num_samples)],
    'Destination IP': [f'{np.random.randint(1, 255)}.{np.random.randint(1, 255)}.{np.random.randint(1, 255)}.{np.random.randint(1, 255)}' for _ in range(num_samples)],
    'Source Port': np.random.randint(1024, 65535, num_samples),
    'Destination Port': np.random.randint(1024, 65535, num_samples),
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv('synthetic_network_traffic_dataset.csv', index=False)
print("Synthetic dataset generated and saved as 'synthetic_network_traffic_dataset.csv'.")
