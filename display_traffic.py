# display_traffic.py
import pandas as pd

try:
    # Load captured traffic
    df = pd.read_csv('captured_traffic.csv')

    if df.empty:
        print("No traffic captured.")
    else:
        # Display the captured traffic
        print(df)
except FileNotFoundError:
    print("File 'captured_traffic.csv' not found.")
except pd.errors.EmptyDataError:
    print("File 'captured_traffic.csv' is empty.")
