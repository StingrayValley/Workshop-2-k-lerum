"""
Modul 3: Hovedprogram (main.py)

Dette modul fungerer som indgangspunkt for programmet. Det initialiserer kølerummet, energiforbrug, madspild og 
simulation, og udfører Monte Carlo-simulationen. Resultaterne præsenteres i form af gennemsnitlige omkostninger 
samt visualiseringer af temperaturudvikling og elpriser.
"""

import matplotlib.pyplot as plt
import csv
import argparse
from kølerum import Kølerum, Energiforbrug, Madspild
from simulation import Simulation

# Læs elpriser fra CSV-fil
elpriser = []
try:
    with open("elpriser.csv", "r") as file:
        reader = csv.reader(file)
        next(reader)  # Spring overskrift over
        for row in reader:
            elpriser.append(float(row[1]))  # Anden kolonne indeholder elpriser
except FileNotFoundError:
    print("Fejl: 'elpriser.csv' filen blev ikke fundet. Sørg for, at filen er i samme mappe som programmet.")
    exit(1)
except ValueError:
    print("Fejl: Der er ikke gyldige tal i CSV-filen. Kontrollér filens indhold.")
    exit(1)

# CLI-argumenter for antal simulationer
parser = argparse.ArgumentParser()
parser.add_argument("--num_simulations", type=int, default=100, help="Antal Monte Carlo-simulationer")
args = parser.parse_args()

# Kør simulation for simpel termostat
kølerum_simple = Kølerum()
energiforbrug_simple = Energiforbrug()
madspild_simple = Madspild()
simulation_simple = Simulation(
    kølerum=kølerum_simple, 
    energiforbrug=energiforbrug_simple, 
    madspild=madspild_simple, 
    elpriser=elpriser, 
    num_simulations=args.num_simulations, 
    target_temp=5.0
)

simple_thermostat_cost = simulation_simple.run_monte_carlo()
print(f"Gennemsnitlig månedlig udgift (simpel termostat): {simple_thermostat_cost:.2f} kr.")

# Gem temperaturdata for simpel termostat
simulation_simple.run_single_simulation()
simple_thermostat_temps = kølerum_simple.udvikling

# Kør simulation for intelligent termostat
kølerum_intelligent = Kølerum()
energiforbrug_intelligent = Energiforbrug()
madspild_intelligent = Madspild()
simulation_intelligent = Simulation(
    kølerum=kølerum_intelligent, 
    energiforbrug=energiforbrug_intelligent, 
    madspild=madspild_intelligent, 
    elpriser=elpriser, 
    num_simulations=args.num_simulations, 
    target_temp=6.0
)

intelligent_thermostat_cost = simulation_intelligent.run_monte_carlo()
print(f"Gennemsnitlig månedlig udgift (intelligent termostat): {intelligent_thermostat_cost:.2f} kr.")

# Gem temperaturdata for intelligent termostat
simulation_intelligent.run_single_simulation()
intelligent_thermostat_temps = kølerum_intelligent.udvikling

# Plot 1: Temperaturudvikling (simpel vs. intelligent termostat)
plt.figure(figsize=(10, 6))
plt.plot(simple_thermostat_temps[:2016], label="Simpel Termostat")  # 1 uge = 2016 tidsintervaller
plt.plot(intelligent_thermostat_temps[:2016], label="Intelligent Termostat")
plt.title("Temperaturudvikling i kølerummet over en uge")
plt.xlabel("Tidsintervaller (5 min)")
plt.ylabel("Temperatur (°C)")
plt.axhline(y=5, color="red", linestyle="--", label="Mål for simpel termostat")
plt.axhline(y=6, color="blue", linestyle="--", label="Mål for intelligent termostat")
plt.legend()
plt.show()

# Plot 2: Udgifter til el og madspild over en uge (simpel termostat)
simple_energy_costs = []
simple_food_loss_costs = []
for elpris in elpriser[:2016]:  # Kun 1 uge
    kølerum_simple.toggle_door()
    C1 = 3e-5 if kølerum_simple.door_open else 5e-7
    C2 = 8e-6 if kølerum_simple.current_temp > 5.0 else 0
    kølerum_simple.update_temperature(C1, C2)
    compressor_on = C2 > 0
    simple_energy_costs.append(energiforbrug_simple.calculate_cost(elpris, compressor_on))
    simple_food_loss_costs.append(madspild_simple.calculate_cost(kølerum_simple.current_temp))

plt.figure(figsize=(10, 6))
plt.plot(simple_energy_costs, label="Elforbrug (simpel termostat)", alpha=0.7)
plt.plot(simple_food_loss_costs, label="Madspild (simpel termostat)", alpha=0.7)
plt.title("Udgifter til el og madspild over en uge (simpel termostat)")
plt.xlabel("Tidsintervaller (5 min)")
plt.ylabel("Omkostninger (kr.)")
plt.legend()
plt.show()

# Plot 3: Histogram over udgift per 5 minutter i september
simple_total_costs = [
    energiforbrug_simple.calculate_cost(elpris, True) + madspild_simple.calculate_cost(kølerum_simple.current_temp)
    for elpris in elpriser
]
intelligent_total_costs = [
    energiforbrug_intelligent.calculate_cost(elpris, True) + madspild_intelligent.calculate_cost(kølerum_intelligent.current_temp)
    for elpris in elpriser
]

plt.figure(figsize=(10, 6))
plt.hist(simple_total_costs, bins=50, alpha=0.5, label="Simpel Termostat")
plt.hist(intelligent_total_costs, bins=50, alpha=0.5, label="Intelligent Termostat")
plt.title("Histogram over udgift per 5 minutter i september")
plt.xlabel("Omkostning (kr.)")
plt.ylabel("Frekvens")
plt.legend()
plt.show()
