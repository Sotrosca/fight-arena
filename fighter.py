import os
import sys

import pygame


class Stats:
    def __init__(self, health, defense, attack):
        self.health = health
        self.defense = defense
        self.attack = attack

    def __str__(self):
        return (
            f"Health: {self.health} - Defense: {self.defense} - Attack: {self.attack}"
        )

    def __sum__(self, other):
        return Stats(
            self.health + other.health,
            self.defense + other.defense,
            self.attack + other.attack,
        )


class Attack:
    def __init__(self, name, target, stats):
        self.name = name
        self.target = target
        self.stats = stats

    def __str__(self):
        return f"{self.name} - {self.target} - {self.stats}"

    def action(self, fighter, enemies, allies):
        pass


class Punch(Attack):
    def __init__(self):
        super().__init__("Punch", "enemy", Stats(10, 0, 0))

    def action(self, fighter, enemies, allies):
        damage = fighter.stats.attack + self.stats.health
        events = {}
        for enemy in enemies:
            enemy_defense = enemy.stats.defense
            damage = max(0, damage - enemy_defense)
            enemy.takes_damage(damage)
            events[enemy] = damage
        return events


class Barrier(Attack):
    def __init__(self):
        super().__init__("Barrier", "self", Stats(0, 1, 0))

    def action(self, fighter, enemies, allies):
        fighter.stats.defense += self.stats.defense
        new_defense = fighter.stats.defense

        return {fighter: f"Defense increased to {new_defense}"}


class Fear(Attack):
    def __init__(self):
        super().__init__("Fear", "enemy", Stats(0, 0, 5))

    def action(self, fighter, enemies, allies):
        events = {}
        for enemy in enemies:
            enemy.stats.attack -= self.stats.attack
            new_attack = enemy.stats.attack
            events[enemy] = f"Attack decreased to {new_attack}"
        return events


class Enrage(Attack):
    def __init__(self):
        super().__init__("Enrage", "self", Stats(5, 0, 10))

    def action(self, fighter, enemies, allies):
        fighter.stats.attack += self.stats.attack
        new_attack = fighter.stats.attack
        fighter.stats.health -= self.stats.health
        return {
            fighter: f"Attack increased to {new_attack} and health decreased to {fighter.stats.health}"
        }


class Fighter:
    def __init__(self, name, health, defense):
        self.name = name
        self.stats = Stats(health, defense, 1)
        self.attacks = {
            "Punch": Punch(),
            "Barrier": Barrier(),
            "Fear": Fear(),
            "Enrage": Enrage(),
        }

    def attack(self, attack_name):
        return self.attacks[attack_name]

    def takes_damage(self, damage):
        self.stats.health -= damage
        return self.stats.health

    def image(self):
        image = pygame.image.load(os.path.join(os.getcwd(), "assets/inu.jpg"))
        resized_image = pygame.transform.scale(image, (100, 100))
        return resized_image
