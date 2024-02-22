import pygame

import constants
from components import Button
from fighter import Fighter


class FighterLayer:
    def __init__(self, fighter, position, rect, attack_rect):
        self.fighter: Fighter = fighter
        self.position = position
        self.font = pygame.font.Font(None, 36)
        self.rect: pygame.Rect = rect
        self.attack_rect = attack_rect
        self.attack_buttons = self.create_buttons()

    def draw_fighter_data(self, screen: pygame.Surface):
        # Draw the fighter's HP
        name_text = self.font.render(f"{self.fighter.name}", True, constants.WHITE)
        hp_text = self.font.render(
            f"HP: {self.fighter.stats.health}", True, constants.WHITE
        )
        defense_text = self.font.render(
            f"Defense: {self.fighter.stats.defense}", True, constants.WHITE
        )
        attack_text = self.font.render(
            f"Attack: {self.fighter.stats.attack}", True, constants.WHITE
        )

        first_center_rect = hp_text.get_rect(center=(self.rect.center[0], self.rect.y))
        screen.blit(name_text, first_center_rect)
        screen.blit(
            hp_text,
            (first_center_rect.x, first_center_rect.y + constants.MARGIN_DATA_ROWS),
        )
        screen.blit(
            defense_text,
            (first_center_rect.x, first_center_rect.y + constants.MARGIN_DATA_ROWS * 2),
        )
        screen.blit(
            attack_text,
            (first_center_rect.x, first_center_rect.y + constants.MARGIN_DATA_ROWS * 3),
        )

        # pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)

    def create_buttons(self):
        margin = 0
        buttons = []
        for attack_name, attack in self.fighter.attacks.items():
            button = Button(
                (0, 255, 0),
                self.attack_rect[0],
                self.attack_rect[1] + margin,
                self.attack_rect[2],
                self.attack_rect[3],
                attack_name,
            )
            buttons.append(button)
            margin += constants.MARGIN_ATTACK_BUTTONS

        return buttons

    def draw_attacks_buttons(self, screen):
        # pygame.draw.rect(screen, (0, 0, 255), self.attack_rect, 2)
        # Draw the fighter's attacks
        for button in self.attack_buttons:
            button.draw(screen)

    def draw(self, screen):
        self.draw_fighter_data(screen)
        self.draw_attacks_buttons(screen)
