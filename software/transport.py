# ==========================================================
# TRANSPORT LAYER
#
# Right now packets are printed for simulation.
# Later this is where RS-422 transmission will happen.
# ==========================================================


def print_packet(packet):
    print("VISCA:", end=" ")

    for value in packet:
        print(f"{value:02X}", end=" ")

    print()


def send_packet(packet):
    # SIMULATION ONLY FOR NOW
    print_packet(packet)
