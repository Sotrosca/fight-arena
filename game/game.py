import pygame

import constants
from fighter import Fighter
from layers import FighterLayer


class GameEvent:
    def __init__(self, type, from_fighter, to_fighter, **kwargs):
        self.type = type
        self.from_fighter = from_fighter
        self.to_fighter = to_fighter
        self.kwargs = kwargs

    def get_event_text(self):
        if self.type == "attack":
            return f"{self.from_fighter.name} attacked {self.to_fighter.name} with {self.kwargs['attack_name']} and caused {self.kwargs['damage']} damage"

        elif self.type == "damage":
            return f"{self.to_fighter.name} took {self.kwargs['damage']} damage"

        else:
            return "No event"


class GameLogic:
    def __init__(self):
        self.fighters: list[Fighter] = []
        self.fighter_qty = 0

    def add_fighter(self, fighter):
        self.fighters.append(fighter)
        self.fighter_qty += 1

    def attack(self, fighter, attack_name):
        attack = fighter.attack(attack_name)
        enemies = [f for f in self.fighters if f != fighter]
        damages = attack.action(fighter, enemies, self.fighters)

        return damages


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode(
            (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
        )
        self.background = pygame.image.load("forest.jpg")
        self.background = pygame.transform.scale(
            self.background, (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
        )
        self.clock = pygame.time.Clock()
        self.running = True
        self.fighter_positions: list[tuple[int, int]] = []
        self.fighter_layers: list[FighterLayer] = []
        self.buttons = []
        self.game_logic = GameLogic()
        self.fighters = []
        self.fighter_qty = 0
        self.last_events = []

    def get_new_fighter_position(self):
        position = constants.FIGHTER_POSITIONS[self.fighter_qty]
        return position

    def get_new_fighter_data_rect(self):
        position = constants.FIGHTER_DATA_POSITIONS[self.fighter_qty]

        rect = pygame.Rect(
            0, 0, constants.FIGTHER_DATA_WIDTH, constants.FIGTHER_DATA_HEIGHT
        )
        rect.center = position
        return rect

    def get_new_fighter_attack_rect(self):
        position = constants.FIGTHER_ATTACK_POSITIONS[self.fighter_qty]

        rect = pygame.Rect(
            0, 0, constants.ATTACK_BUTTON_WIDTH, constants.ATTACK_BUTTON_HEIGHT
        )
        rect.center = position
        return rect

    def add_fighter(self, fighter):
        self.game_logic.add_fighter(fighter)
        position = self.get_new_fighter_position()
        rect_data = self.get_new_fighter_data_rect()
        attack_rect = self.get_new_fighter_attack_rect()
        self.fighter_positions.append(position)
        layer = FighterLayer(fighter, position, rect_data, attack_rect)
        self.fighter_layers.append(layer)
        self.buttons.append(layer.attack_buttons)
        self.fighters.append(fighter)
        self.fighter_qty += 1

    def handle_fighter_attack(self, fighter, attack_name):
        damages = self.game_logic.attack(fighter, attack_name)

        for enemy, damage in damages.items():
            event = GameEvent(
                "attack",
                fighter,
                enemy,
                attack_name=attack_name,
                damage=damage,
            )
            self.last_events.append(event)

    def draw_figthers(self):
        for fighter, position, layer in zip(
            self.fighters, self.fighter_positions, self.fighter_layers
        ):
            centered_position = (
                position[0] - fighter.image().get_width() / 2,
                position[1] - fighter.image().get_height() / 2,
            )
            self.screen.blit(fighter.image(), centered_position)
            layer.draw(self.screen)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.last_events = []
                for i, player_buttons in enumerate(self.buttons):
                    for button in player_buttons:
                        if button.is_over(pos):
                            self.handle_fighter_attack(self.fighters[i], button.text)

    def draw_game_events_board(self):
        # Draw the game events board, for example the attacks and the damage taken

        font = pygame.font.Font(None, 24)
        margin = 20
        for event in self.last_events:
            text = font.render(event.get_event_text(), True, constants.WHITE)
            text_rect = text.get_rect(center=(constants.SCREEN_WIDTH / 2, margin))
            self.screen.blit(text, text_rect)

    def run(self):
        while self.running:
            self.clock.tick(constants.FPS)
            self.screen.blit(self.background, (0, 0))
            self.draw_figthers()
            self.handle_events()
            self.draw_game_events_board()
            pygame.display.flip()
        pygame.quit()


if __name__ == "__main__":
    pygame.init()  # Initialize all pygame modules
    pygame.font.init()  # Initialize the font module

    # Crear luchadores
    fighter1 = Fighter("Baba Yaya", 100, 10)
    fighter2 = Fighter("Inu culado", 120, 12)

    # Crear juego
    game = Game()

    # Agregar luchadores al juego
    game.add_fighter(fighter1)
    game.add_fighter(fighter2)

    # Correr el juego
    game.run()
