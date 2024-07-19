import pandas as pd
import joblib
import pydivert

# Load the pre-trained model and scaler
model = joblib.load('traffic_model.joblib')
scaler = joblib.load('scaler.joblib')

def packet_handler(packet):
    # Extract features
    packet_length = len(packet.raw)
    src_port = packet.src_port
    dst_port = packet.dst_port
    protocol = packet.protocol

    # Convert protocol to a string
    protocol_str = f"{protocol[0]}, {protocol[1]}"

    # Create a DataFrame with the packet features
    packet_df = pd.DataFrame([[packet_length, src_port, dst_port, protocol_str]], 
                             columns=['length', 'src_port', 'dst_port', 'protocol'])

    # One-hot encode the protocol values
    packet_df['protocol_6, 20'] = 0  # Initialize the protocol_6, 20 column
    packet_df.loc[packet_df['protocol'] == '6, 20', 'protocol_6, 20'] = 1  # Set protocol_6, 20 to 1 where applicable

    # Drop the original protocol column
    packet_df.drop(columns=['protocol'], inplace=True)

    # Scale the features
    packet_df_scaled = scaler.transform(packet_df)

    # Predict if unwanted
    is_unwanted = model.predict(packet_df_scaled)[0]

    # Drop the packet if unwanted
    if is_unwanted:
        print(f"Dropping packet: {packet}")
        return None

    return packet





try:
    print("Starting traffic optimization...")
    with pydivert.WinDivert() as w:
        for packet in w:
            modified_packet = packet_handler(packet)
            if modified_packet is not None:
                w.send(modified_packet)
except Exception as e:
    print(f"Error: {e}")
