"""Modul 2: Monte Carlo-simulation (simulation.py)
Dette modul skal:

Indeholde situationen af kølerummets drift, herunder beregning af temperaturudvikling, energiforbrug og madspild. 
Det inkluderer både enkeltsimulation og Monte Carlo-simulation for at evaluere kølerummets økonomiske ydeevne.

Klasser og deres ansvar
Simulation: 
Håndterer simulationen af kølerummets drift.
Beregner totale udgifter baseret på energiforbrug og madspild.
Understøtter Monte Carlo-simulation for at bestemme gennemsnitlige omkostninger."""

from kølerum import Kølerum, Energiforbrug, Madspild
import random

class Simulation:
    def __init__(self, kølerum, energiforbrug, madspild, elpriser, num_simulations=1000, target_temp=5.0):
        """
        Initialiserer simulationen.
        - attribut kølerum: Instans af Kølerum.
        - attribut energiforbrug: Instans af Energiforbrug.
        - attribut madspild: Instans af Madspild.
        - attribut elpriser: Liste over elpriser i 5-minutters intervaller.
        - attribut num_simulations: Antal simulationer i Monte Carlo.
        - attribut target_temp: Måltemperaturen for termostaten.
        """
        self.kølerum = kølerum
        self.energiforbrug = energiforbrug
        self.madspild = madspild
        self.elpriser = elpriser
        self.num_simulations = num_simulations
        self.target_temp = target_temp
    
    def run_single_simulation(self, debug=False):
        """
        Kører en enkelt simulation og returnerer totaludgiften.
        """
        total_cost = 0
        for elpris in self.elpriser:
            self.kølerum.toggle_door()  # Opdater dørstatus
            C1 = 3e-5 if self.kølerum.door_open else 5e-7
            C2 = 8e-6 if self.kølerum.current_temp > self.target_temp else 0
            self.kølerum.update_temperature(C1, C2)
            compressor_on = C2 > 0
            energy_cost = self.energiforbrug.calculate_cost(elpris, compressor_on)
            food_loss_cost = self.kølerum.calculate_food_loss()
            total_cost += energy_cost + food_loss_cost
            if debug:
                food_loss_cost = self.madspild.calculate_cost(self.kølerum.current_temp)
                print(f"Temp: {self.kølerum.current_temp:.2f}, Food Loss Cost: {food_loss_cost:.2f} kr.")
                termostat_status = "tændt" if compressor_on else "slukket"
                print(f"Elpris: {elpris:.2f} kr./kWh, Termostat: {termostat_status}, Energy Cost: {energy_cost:.2f} kr.")
        return total_cost

    def run_single_simulation_intelligent(self):
        """
        Kører en enkelt simulation med en intelligent termostat.
        """
        total_cost = 0
        avg_elpris = sum(self.elpriser) / len(self.elpriser)  # Gennemsnitlig elpris
        for elpris in self.elpriser:
            self.kølerum.toggle_door()  # Opdater dørstatus
            C1 = 3e-5 if self.kølerum.door_open else 5e-7

            # Intelligent logik: Tænd kompressor kun ved lave elpriser eller kritisk temperatur
            if elpris <= avg_elpris or self.kølerum.current_temp > 6.5:
                C2 = 8e-6 if self.kølerum.current_temp > self.target_temp else 0
            else:
                C2 = 0

            self.kølerum.update_temperature(C1, C2)
            compressor_on = C2 > 0
            energy_cost = self.energiforbrug.calculate_cost(elpris, compressor_on)
            food_loss_cost = self.kølerum.calculate_food_loss()
            total_cost += energy_cost + food_loss_cost
        return total_cost


    def run_monte_carlo(self):
        """
        Kører Monte Carlo-simulation og returnerer gennemsnitlige udgifter.
        """
        total_costs = [self.run_single_simulation() for _ in range(self.num_simulations)]
        return sum(total_costs) / self.num_simulations

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    # Eksempel på simulation
    elpriser = [random.uniform(1.5, 5.0) for _ in range(288 * 30)]  # Tilfældige priser for en måned
    kølerum = Kølerum()
    energiforbrug = Energiforbrug()
    madspild = Madspild()
    simulation = Simulation(kølerum, energiforbrug, madspild, elpriser, num_simulations=100)
    avg_cost = simulation.run_monte_carlo()
    print(f"Gennemsnitlig udgift: {avg_cost:.2f} kr.")
