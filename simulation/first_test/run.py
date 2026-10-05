
import os
import traci

SUMO_HOME = r"M:\Tools\SUMO"
PROJECT_DIR = r"M:\InfrastructureDigitalTwin\simulation\first_test"

sumo_binary = os.path.join(SUMO_HOME, "bin", "sumo-gui.exe")
config_file = os.path.join(PROJECT_DIR, "simulation.sumocfg")

print("Starting SUMO simulation...")

traci.start([sumo_binary, "-c", config_file])

departed_total = 0
arrived_total = 0

try:
    print("TraCI connected successfully!")

    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()

        departed_total += traci.simulation.getDepartedNumber()
        arrived_total += traci.simulation.getArrivedNumber()

        vehicles = traci.vehicle.getIDList()

        print(
            f"Time: {traci.simulation.getTime():.0f}s | "
            f"On road: {len(vehicles)} | "
            f"Departed: {departed_total} | "
            f"Arrived: {arrived_total}"
        )

finally:
    traci.close()

print("\n--- SIMULATION SUMMARY ---")
print(f"Total departed: {departed_total}")
print(f"Total arrived: {arrived_total}")
print("Simulation finished.")
