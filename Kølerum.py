"""Modul 1: Core Simulation (kølerum.py)
Dette modul skal:

Indeholde klasser og metoder til at simulere temperaturudviklingen i kølerummet.
Beregne forbrug, madspild og samlede udgifter

Klasser og deres ansvar:
Kølerum:
    Holder styr på temperatur, kompressorstatus og dørsituation.
    Beregner temperaturudvikling i hvert tidsinterval.
    Håndterer døren (åben/lukket) og kompressoren (tændt/slukket).
Energiforbrug:
    Beregner energiforbruget baseret på kompressorstatus og elpriser.
Madspild:
    Beregner omkostninger forbundet med madspild, afhængigt af temperaturen"""

import random
import math

class Kølerum:
    def __init__(self, start_temp=5.0, tidsinterval=300, door_probability=0.1):
        """
        Initialiserer kølerummet.
        - attribut start_temp: Starttemperaturen i grader Celsius.
        - attribut tidsinterval: Tid pr. interval i sekunder (standard 5 minutter).
        - attribut door_probability: Sandsynlighed for, at døren er åben.
        """
        self.current_temp = start_temp
        self.tidsinterval = tidsinterval
        self.door_probability = door_probability
        self.door_open = False
        self.udvikling = [start_temp]

    def toggle_door(self):
        """Opdaterer dørsituationen (åben/lukket) baseret på sandsynligheder."""
        self.door_open = random.random() < self.door_probability

    def update_temperature(self, C1, C2, Trum=20.0, Tkomp=-5.0):
        """
        Opdaterer temperaturen i kølerummet.
        - attribut C1: Frekvens for varmeledning.
        - attribut C2: Frekvens for køling.
        - attribut Trum: Temperaturen udenfor kølerummet.
        - attribut Tkomp: Køletemperatur fra kompressoren.

        >>> k = Kølerum(start_temp=5.0)
        >>> k.update_temperature(C1=5e-7, C2=8e-6)
        >>> round(k.current_temp, 3)  # Temperaturen efter opdatering
        4.998
        """
        delta_temp = (C1 * (Trum - self.current_temp) + 
                      C2 * (Tkomp - self.current_temp)) * self.tidsinterval
        self.current_temp += delta_temp
        self.udvikling.append(self.current_temp)

    def calculate_energy_cost(self, price_per_kWh, compressor_on, power_usage=1.0):
        """
        Beregner omkostninger for energiforbrug.
        - attribut price_per_kWh: Elpris i kr/kWh.
        - attribut compressor_on: Boolean om kompressoren er tændt.
        - attribut power_usage: Energiforbrug pr. 5 minutter.
        return: Omkostningerne for strømforbruget.
        """
        return price_per_kWh * power_usage if compressor_on else 0.0

    def calculate_food_loss(self):
        """
        Beregner madspild baseret på temperaturen.
        return: Omkostningerne for madspild.
        """
        temp = self.current_temp
        if temp < 3.5:
            return 4.39 * math.exp(-0.49 * temp)
        elif 3.5 <= temp < 6.5:
            return 0.0
        else:
            return 0.11 * math.exp(0.31 * temp)

class Energiforbrug:
    """
    Repræsenterer energiforbruget i kølerummet.
    """
    def __init__(self, power_usage=1.0): # Realistisk forbrug i kWh pr. 5 minutter
        """
        Initialiserer energiforbruget.
        - attribut power_usage: Strømforbrug i kWh pr. 5 minutter.
        """
        self.power_usage = power_usage

    def calculate_cost(self, price_per_kWh, compressor_on):
        """
        Beregner elomkostninger baseret på kompressorstatus.
        - attribut price_per_kWh: Elpris i kr. pr. kWh.
        - attribut compressor_on: Boolean, der angiver om kompressoren er tændt.
        >>> ef = Energiforbrug(power_usage=1.0)
        >>> ef.calculate_cost(3.0, True)
        3.0
        >>> ef.calculate_cost(3.0, False)
        0.0
        """
        return price_per_kWh * self.power_usage if compressor_on else 0.0

class Madspild:
    """
    Beregner omkostninger for madspild baseret på temperaturen.
    """
    @staticmethod
    def calculate_cost(temp):
        """
        Beregner madspild baseret på temperaturen.
        - attribut temp: Temperaturen i grader Celsius.
        return: Omkostninger for madspild.
        
        >>> Madspild.calculate_cost(3.0)
        1.582
        >>> Madspild.calculate_cost(5.0)
        0.0
        >>> Madspild.calculate_cost(7.0)
        1.27
        """
        if temp < 3.5:
            return round(4.39 * math.exp(-0.49 * temp), 3)
        elif 3.5 <= temp < 6.5:
            return 0.0
        else:
            return round(0.11 * math.exp(0.31 * temp), 3)
