import pygame
import sys
from ai_game.ai_logic import Game
from ai_game.simple_ai import SimpleAI
from ai_game.ai_pieces import PieceType  # Import PieceType

pygame.init()
BOARD_SIZE = 8
SQUARE_SIZE = 80
RIGHT_PANEL_WIDTH = 200
WIDTH, HEIGHT = SQUARE_SIZE * BOARD_SIZE, SQUARE_SIZE * BOARD_SIZE
screen = pygame.display.set_mode((WIDTH + RIGHT_PANEL_WIDTH, HEIGHT))

# Colors
BACKGROUND_COLOR = (220, 220, 220)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CHESS_GREEN = (118, 150, 86)
SELECTED_COLOR = (0, 255, 0)
GOLD = (255, 215, 0)
RED = (255, 0, 0)

# Pieces
assets = "assets/"
piece_images = {
    "white_king": pygame.image.load(assets + "white_king.png"),
    "black_king": pygame.image.load(assets + "black_king.png"),
    "white_farm": pygame.image.load(assets + "white_farm.png"),
    "black_farm": pygame.image.load(assets + "black_farm.png"),
    "white_pawn": pygame.image.load(assets + "white_pawn.png"),
    "black_pawn": pygame.image.load(assets + "black_pawn.png"),
    "white_turret": pygame.image.load(assets + "white_turret.png"),
    "black_turret": pygame.image.load(assets + "black_turret.png"),
    "white_shield": pygame.image.load(assets + "white_shield.png"),
    "black_shield": pygame.image.load(assets + "black_shield.png"),
}

game = Game()
ai = SimpleAI(game)

def draw_board():
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            color = WHITE if (row + col) % 2 == 0 else CHESS_GREEN
            pygame.draw.rect(screen, color, rect)

def draw_right_panel():
    pygame.draw.rect(screen, BACKGROUND_COLOR, pygame.Rect(WIDTH, 0, RIGHT_PANEL_WIDTH, HEIGHT))
    font = pygame.font.SysFont('Arial', 24)

    turn_text = font.render(f"Turn: {game.turn.replace('_', ' ').capitalize()}", True, BLACK)
    screen.blit(turn_text, (WIDTH + 20, 30))

    current_color = "white" if game.turn.lower().startswith("white") else "black"
    current_actions_text = font.render(f"{current_color.capitalize()} Actions: {game.actions[current_color]}", True, BLACK)
    screen.blit(current_actions_text, (WIDTH + 20, 80))

    white_action_points_text = font.render(f"White AP: {game.action_points['white']}", True, BLACK)
    screen.blit(white_action_points_text, (WIDTH + 20, 140))
    black_action_points_text = font.render(f"Black AP: {game.action_points['black']}", True, BLACK)
    screen.blit(black_action_points_text, (WIDTH + 20, 170))

    player1_score_text = font.render(f"P1 Score: {game.scores['Player 1']}", True, BLACK)
    screen.blit(player1_score_text, (WIDTH + 20, 210))
    player2_score_text = font.render(f"P2 Score: {game.scores['Player 2']}", True, BLACK)
    screen.blit(player2_score_text, (WIDTH + 20, 240))

    buttons = []

    if not game.initial_phase:
        place_pawn_button = pygame.Rect(WIDTH + 20, 300, 160, 40)
        button_color = (0, 255, 0)
        pygame.draw.rect(screen, button_color, place_pawn_button)
        pawn_button_text = font.render("Place Pawn", True, BLACK)
        screen.blit(pawn_button_text, (WIDTH + 40, 310))
        buttons.append(place_pawn_button)

        farm_button = pygame.Rect(WIDTH + 20, 350, 50, 50)
        turret_button = pygame.Rect(WIDTH + 75, 350, 50, 50)
        shield_button = pygame.Rect(WIDTH + 130, 350, 50, 50)

        pygame.draw.rect(screen, WHITE, farm_button)
        pygame.draw.rect(screen, WHITE, turret_button)
        pygame.draw.rect(screen, WHITE, shield_button)

        screen.blit(pygame.transform.scale(piece_images["white_farm"], (50, 50)), (WIDTH + 20, 350))
        screen.blit(pygame.transform.scale(piece_images["white_turret"], (50, 50)), (WIDTH + 75, 350))
        screen.blit(pygame.transform.scale(piece_images["white_shield"], (50, 50)), (WIDTH + 130, 350))

        buttons.extend([farm_button, turret_button, shield_button])

        fire_turret_button = pygame.Rect(WIDTH + 20, 410, 160, 40)
        pygame.draw.rect(screen, RED, fire_turret_button)
        fire_turret_text = font.render("Fire Turret", True, BLACK)
        screen.blit(fire_turret_text, (WIDTH + 40, 420))
        buttons.append(fire_turret_button)

        buy_action_button = pygame.Rect(WIDTH + 20, 460, 160, 40)
        pygame.draw.rect(screen, GOLD, buy_action_button)
        buy_action_text = font.render("Buy Action", True, BLACK)
        screen.blit(buy_action_text, (WIDTH + 40, 470))
        buttons.append(buy_action_button)

        cancel_button = pygame.Rect(WIDTH + 20, 510, 160, 40)
        pygame.draw.rect(screen, (155, 161, 157), cancel_button)
        cancel_text = font.render("Cancel", True, BLACK)
        screen.blit(cancel_text, (WIDTH + 40, 520))
        buttons.append(cancel_button)

        pass_turn_button = pygame.Rect(WIDTH + 20, 560, 160, 40)
        pygame.draw.rect(screen, (128, 128, 128), pass_turn_button)
        pass_turn_text = font.render("Pass Turn", True, BLACK)
        screen.blit(pass_turn_text, (WIDTH + 40, 570))
        buttons.append(pass_turn_button)

    return buttons

def draw_pieces():
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            piece = game.board.get_piece_at(row, col)
            if piece:
                piece_image_key = f"{piece.color}_{piece.piece_type.value}"
                piece_image = piece_images.get(piece_image_key)
                if piece_image:
                    piece_image = pygame.transform.scale(piece_image, (SQUARE_SIZE, SQUARE_SIZE))
                    screen.blit(piece_image, (col * SQUARE_SIZE, row * SQUARE_SIZE))

def handle_mouse_button_down(event, buttons):
    for button in buttons:
        if button.collidepoint(event.pos):
            if button == buttons[0]:  # Place Pawn
                if not game.upgrade_mode and not game.firing_mode:
                    game.initiate_pawn_placement()
            elif button == buttons[1]:  # Farm
                if not game.firing_mode and not game.pawn_placement_mode:
                    game.initiate_pawn_upgrade("farm")
            elif button == buttons[2]:  # Turret
                if not game.firing_mode and not game.pawn_placement_mode:
                    game.initiate_pawn_upgrade("turret")
            elif button == buttons[3]:  # Shield
                if not game.firing_mode and not game.pawn_placement_mode:
                    game.initiate_pawn_upgrade("shield")
            elif button == buttons[4]:  # Fire Turret
                if not game.upgrade_mode and not game.pawn_placement_mode:
                    game.initiate_turret_firing()
            elif button == buttons[5]:  # Buy Action
                if not game.upgrade_mode and not game.firing_mode and not game.pawn_placement_mode:
                    game.buy_action()
            elif button == buttons[6]:  # Cancel
                game.cancel_action()
            elif button == buttons[7]:  # Pass Turn
                if not game.upgrade_mode and not game.firing_mode and not game.pawn_placement_mode:
                    game.pass_turn()
            return

    row, col = event.pos[1] // SQUARE_SIZE, event.pos[0] // SQUARE_SIZE
    if game.firing_mode:
        if game.selected_turret:
            if game.validate_turret_target(row, col):
                turret_row, turret_col = game.selected_turret
                game.fire_turret(turret_row, turret_col, row, col)
            else:
                print("Invalid target for turret firing.")
        else:
            game.select_turret_to_fire(row, col)
    else:
        game.handle_click(row, col)

def start_ai_game_display():
    pygame.display.set_caption('Territory - Play vs AI')  # Set caption for AI mode
    running = True
    while running:
        screen.fill((0, 0, 0))
        draw_board()
        buttons = draw_right_panel()
        draw_pieces()

        if game.turn.startswith("white"):  # Human player's turn
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    handle_mouse_button_down(event, buttons)
        else:  # AI player's turn
            ai.make_move()

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    start_ai_game_display()