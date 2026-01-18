import pygame
import sys
import time
import random
import unicodedataplus as ud

import pygame
import sys
import time
import random
import webbrowser
import unicodedataplus as ud

# -------------------- INIT --------------------
pygame.init()
TEMP_FONT = pygame.font.SysFont(None, 36)
TEMP_SMALL_FONT = pygame.font.SysFont(None, 24)
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Symbols!")
clock = pygame.time.Clock()

# -------------------- COLORS --------------------
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (40, 120, 255)
RED = (255, 80, 80)
GRAY = (160, 160, 160)

# -------------------- FONT LOADING --------------------
FONT = None
SMALL_FONT = None
BIG_FONT = None
FALLBACK_FONTS = []

def load_fonts():
    global FONT, SMALL_FONT, BIG_FONT, FALLBACK_FONTS
    try:
        FONT = pygame.font.Font("NotoSans-VariableFont_wdth,wght.ttf", 36)
        SMALL_FONT = pygame.font.Font("NotoSans-VariableFont_wdth,wght.ttf", 24)
        BIG_FONT = pygame.font.Font("NotoSans-VariableFont_wdth,wght.ttf", 72)
    except:
        FONT = pygame.font.SysFont(None, 36)
        SMALL_FONT = pygame.font.SysFont(None, 24)
        BIG_FONT = pygame.font.SysFont(None, 72)

    FALLBACK_FONTS = [
        BIG_FONT,
        pygame.font.SysFont("Segoe UI Symbol", 72),
        pygame.font.SysFont("Arial Unicode MS", 72),
        pygame.font.SysFont(None, 72),
    ]

# -------------------- DRAW HELPERS --------------------
def draw_text(text, x, y, font, color=WHITE, center=True):
    for i, line in enumerate(text.split("\n")):
        surf = font.render(line, True, color)
        rect = surf.get_rect(center=(x, y + i * 40)) if center else surf.get_rect(topleft=(x, y + i * 40))
        screen.blit(surf, rect)

def draw_button(rect, text, font=None):
    pygame.draw.rect(screen, BLUE, rect, border_radius=10)
    pygame.draw.rect(screen, WHITE, rect, 2, border_radius=10)

    if font is None:
        font = TEMP_SMALL_FONT if SMALL_FONT is None else SMALL_FONT

    draw_text(text, rect.centerx, rect.centery, font)


def render_symbol_safe(char):
    for f in FALLBACK_FONTS:
        try:
            surf = f.render(char, True, WHITE)
            if surf.get_width() > 0:
                return surf
        except:
            pass
    return BIG_FONT.render("□", True, RED)

# -------------------- UNICODE LOGIC --------------------
def get_char_info(ch):
    try:
        name = ud.name(ch)
    except:
        name = "No official Unicode name"
    return f"Symbol: {ch}\nName: {name}\nCodepoint: U+{ord(ch):04X}"

# -------------------- STATES --------------------
state = "START"
input_text = ""
output_text = ""

# -------------------- MINIGAME DATA --------------------
DIFFICULTIES = {
    "Easy": list("!;:()*&^-%$#@/"),
    "Medium": list("{}[]\\/_abcdefABCDEFG~`"),
    "Hard": ['"', "'", "ą", "ź", "<", ">", "|", "+", "=", "Æ", "æ", "§"],
    "Insane": ["★", "𖤐", "Δ", "𝞭", "λ", "〠", "ε", "Ξ"],
}

KNOWN = set(ch for v in DIFFICULTIES.values() for ch in v)
IMPOSSIBLE = []
for cp in range(0x21, 0x10FFFF):
    try:
        ch = chr(cp)
        if ch not in KNOWN:
            ud.name(ch)
            IMPOSSIBLE.append(ch)
    except:
        continue

DIFFICULTIES["Impossible"] = IMPOSSIBLE

mg_symbol = ""
mg_answer = ""
mg_diff = ""
mg_correct = False
mg_correct_time = 0

def new_symbol():
    global mg_symbol, mg_answer, mg_correct
    mg_symbol = random.choice(DIFFICULTIES[mg_diff])
    try:
        mg_answer = ud.name(mg_symbol)
    except:
        mg_answer = ""
    mg_correct = False

# -------------------- MAIN LOOP --------------------
running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if state in ("SYMBOLS", "MINIGAME_PLAY"):
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]

                elif event.key == pygame.K_RETURN:
                    text = input_text.strip()

                    if state == "SYMBOLS":
                        if len(text) == 1:
                            output_text = get_char_info(text)
                        else:
                            output_text = "Enter exactly one character."

                    elif state == "MINIGAME_PLAY" and not mg_correct:
                        if text.upper() == mg_answer:
                            output_text = "Correct!"
                            mg_correct = True
                            mg_correct_time = time.time()

                    input_text = ""

                else:
                    input_text += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN:
            if state == "START":
                if start_btn.collidepoint(event.pos):
                    load_fonts()
                    state = "HOME"
                if noto_btn.collidepoint(event.pos):
                    webbrowser.open("https://fonts.google.com/noto/specimen/Noto+Sans")

            elif state == "HOME":
                if sym_btn.collidepoint(event.pos):
                    state = "SYMBOLS"
                if mg_btn.collidepoint(event.pos):
                    state = "MINIGAMES"

            elif state == "MINIGAMES":
                for d, r in diff_buttons.items():
                    if r.collidepoint(event.pos):
                        mg_diff = d
                        new_symbol()
                        output_text = ""
                        state = "MINIGAME_PLAY"

            elif state in ("SYMBOLS", "MINIGAME_PLAY"):
                if back_btn.collidepoint(event.pos):
                    state = "HOME"

    # -------------------- DRAW --------------------
    if state == "START":
        draw_text(
            "WARNING!!! WARNING!!!\n\n"
            "This script requires:\n"
            "pip install pygame unicodedataplus\n\n"
            "You must also install Noto Sans\n"
            "(recommended for symbol support)",
            WIDTH // 2, 150, pygame.font.SysFont(None, 26)
        )
        start_btn = pygame.Rect(350, 400, 200, 50)
        noto_btn = pygame.Rect(300, 470, 300, 40)
        draw_button(start_btn, "Start")
        draw_button(noto_btn, "Open Noto Sans Download")

    elif state == "HOME":
        draw_text("Symbols!", WIDTH // 2, 120, FONT)
        sym_btn = pygame.Rect(350, 240, 200, 60)
        mg_btn = pygame.Rect(350, 320, 200, 60)
        draw_button(sym_btn, "Symbols")
        draw_button(mg_btn, "Minigames")

    elif state == "SYMBOLS":
        back_btn = pygame.Rect(20, 20, 100, 40)
        draw_button(back_btn, "Back")
        draw_text("Enter one character:", WIDTH // 2, 140, SMALL_FONT)
        pygame.draw.rect(screen, WHITE, (200, 180, 500, 40), 2)
        draw_text(input_text, WIDTH // 2, 200, SMALL_FONT)
        draw_text(output_text, WIDTH // 2, 280, SMALL_FONT)

    elif state == "MINIGAMES":
        draw_text("Guess the symbol's name!", WIDTH // 2, 120, FONT)
        diff_buttons = {}
        y = 200
        for d in DIFFICULTIES:
            r = pygame.Rect(300, y, 300, 45)
            draw_button(r, d)
            diff_buttons[d] = r
            y += 55

    elif state == "MINIGAME_PLAY":
        back_btn = pygame.Rect(20, 20, 100, 40)
        draw_button(back_btn, "Back")

        draw_text("Symbol:", WIDTH // 2, 90, SMALL_FONT)
        surf = render_symbol_safe(mg_symbol)
        screen.blit(surf, surf.get_rect(center=(WIDTH // 2, 150)))

        pygame.draw.rect(screen, WHITE, (200, 240, 500, 40), 2)
        draw_text(input_text, WIDTH // 2, 260, SMALL_FONT)
        draw_text(output_text, WIDTH // 2, 320, SMALL_FONT)

        if mg_correct and time.time() - mg_correct_time > 2:
            output_text = ""
            new_symbol()

    pygame.display.flip()
    clock.tick(60)
