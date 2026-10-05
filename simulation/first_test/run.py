
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
speed_samples = []
total_waiting_time = 0
max_vehicles = 0

try:
    print("TraCI connected successfully!")

    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()

        departed_total += traci.simulation.getDepartedNumber()
        arrived_total += traci.simulation.getArrivedNumber()

        vehicle_ids = traci.vehicle.getIDList()
        vehicle_count = len(vehicle_ids)

        max_vehicles = max(max_vehicles, vehicle_count)

        for vehicle_id in vehicle_ids:
            speed = traci.vehicle.getSpeed(vehicle_id)
            speed_samples.append(speed)

            if speed < 0.1:
                total_waiting_time += 1

        print(
            f"Time: {traci.simulation.getTime():.0f}s | "
            f"On road: {vehicle_count} | "
            f"Departed: {departed_total} | "
            f"Arrived: {arrived_total}"
        )

finally:
    traci.close()

average_speed = (
    sum(speed_samples) / len(speed_samples)
    if speed_samples else 0
)

print("\n--- SIMULATION SUMMARY ---")
print(f"Total departed: {departed_total}")
print(f"Total arrived: {arrived_total}")
print(f"Maximum vehicles on road: {max_vehicles}")
print(f"Average speed: {average_speed:.2f} m/s")
print(f"Average speed: {average_speed * 3.6:.2f} km/h")
print(f"Stationary vehicle-seconds: {total_waiting_time}")
print("Simulation finished.")
