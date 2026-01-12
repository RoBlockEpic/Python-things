import pygame
import unicodedataplus as ud
import time
import sys
import webbrowser
import os

# -------------------- INIT --------------------
pygame.init()
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Symbols!")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (200, 0, 0)
GREEN = (0, 160, 0)

clock = pygame.time.Clock()

# ---- SAFE FALLBACK FONTS (CRITICAL FIX) ----
FONT = pygame.font.SysFont(None, 36)
SMALL_FONT = pygame.font.SysFont(None, 26)

def load_noto_font():
    global FONT, SMALL_FONT
    if os.path.exists("NotoSans-VariableFont_wdth,wght.ttf"):
        FONT = pygame.font.Font("NotoSans-VariableFont_wdth,wght.ttf", 36)
        SMALL_FONT = pygame.font.Font("NotoSans-VariableFont_wdth,wght.ttf", 26)

# -------------------- STATE --------------------
current_screen = "STARTER"
tutorial_step = 0
input_text = ""
output_text = ""
exit_start = None
live_valid = None

# -------------------- DRAW HELPERS --------------------
def draw_text(text, x, y, font=FONT, color=BLACK, center=False):
    lines = text.split("\n")
    for i, line in enumerate(lines):
        surf = font.render(line, True, color)
        rect = surf.get_rect()
        if center:
            rect.center = (x, y + i * 34)
        else:
            rect.topleft = (x, y + i * 34)
        screen.blit(surf, rect)

def draw_button(rect, text):
    pygame.draw.rect(screen, GRAY, rect)
    pygame.draw.rect(screen, BLACK, rect, 2)
    draw_text(text, rect.centerx, rect.centery - 16, center=True)

# -------------------- UNICODE LOGIC --------------------
def get_char_info(ch):
    try:
        name = ud.name(ch)
    except ValueError:
        name = "No official Unicode name"
    cp = f"U+{ord(ch):04X}"
    age = ud.age(ch)
    ver = f"{age[0]}.{age[1]}" if age else "Unknown"
    return f"Symbol: {ch}\nName: {name}\nCodepoint: {cp}\nUnicode version: {ver}"

def parse_u_input(text):
    try:
        cp = int(text[2:], 16)
        if cp < 0x20 or cp == 0x7F:
            return "Control characters cannot be displayed."
        if cp > 0x10FFFF:
            return "Invalid Unicode codepoint."
        return get_char_info(chr(cp))
    except ValueError:
        return "Invalid codepoint."

def find_extreme(longest=True):
    best_len = 0 if longest else 9999
    best = None
    for cp in range(0x110000):
        try:
            ch = chr(cp)
            name = ud.name(ch)
            ln = len(name)
            if (longest and ln > best_len) or (not longest and ln < best_len):
                best_len = ln
                best = get_char_info(ch)
        except ValueError:
            continue
    return best

def find_by_name(query):
    query = query.upper()
    for cp in range(0x110000):
        try:
            ch = chr(cp)
            if ud.name(ch) == query:
                return get_char_info(ch)
        except ValueError:
            continue
    return "No character with that exact name found."

# -------------------- LIVE VALIDATION --------------------
def update_live_validation(text):
    if not text:
        return None
    if text.lower() in ("longest", "shortest", "exit"):
        return True
    if text.upper().startswith("U+"):
        try:
            cp = int(text[2:], 16)
            return 0x20 <= cp <= 0x10FFFF and cp != 0x7F
        except ValueError:
            return False
    if len(text) == 1:
        return True
    return True

# -------------------- MAIN LOOP --------------------
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if current_screen in ("SYMBOLS", "TUTORIAL"):
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key == pygame.K_RETURN:
                    text = input_text.strip()

                    if current_screen == "TUTORIAL":
                        if tutorial_step == 0 and text.lower() == "longest":
                            output_text = find_extreme(True)
                            tutorial_step = 1
                        elif tutorial_step == 1 and text.lower() == "shortest":
                            output_text = find_extreme(False)
                            tutorial_step = 2
                        elif tutorial_step == 2 and text.lower() == "exit":
                            exit_start = time.time()
                            current_screen = "EXIT"
                        else:
                            output_text = "Please type the requested word."
                    else:
                        if text.lower() == "longest":
                            output_text = find_extreme(True)
                        elif text.lower() == "shortest":
                            output_text = find_extreme(False)
                        elif text.lower() == "exit":
                            exit_start = time.time()
                            current_screen = "EXIT"
                        elif text.upper().startswith("U+"):
                            output_text = parse_u_input(text)
                        elif len(text) == 1:
                            output_text = get_char_info(text)
                        else:
                            output_text = find_by_name(text)

                    input_text = ""
                    live_valid = None

                else:
                    input_text += event.unicode
                    live_valid = update_live_validation(input_text)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if current_screen == "STARTER":
                if start_btn.collidepoint(event.pos):
                    load_noto_font()
                    current_screen = "HOME"
                if noto_btn.collidepoint(event.pos):
                    webbrowser.open("https://fonts.google.com/noto/specimen/Noto+Sans")

            elif current_screen == "HOME":
                if sym_btn.collidepoint(event.pos):
                    current_screen = "SYMBOLS"
                if tut_btn.collidepoint(event.pos):
                    current_screen = "TUTORIAL"
                    tutorial_step = 0
                    input_text = ""
                    output_text = ""

            elif current_screen == "TUTORIAL" and tutorial_step == 3:
                if ok_btn.collidepoint(event.pos):
                    current_screen = "HOME"

    # -------------------- DRAW --------------------
    if current_screen == "STARTER":
        draw_text(
            'print("WARNING!!! WARNING!!!")\n'
            'print("pip install pygame unicodedataplus")\n'
            'print("AND INSTALL NOTO SANS")',
            WIDTH // 2, 120, center=True
        )
        start_btn = pygame.Rect(350, 300, 200, 60)
        noto_btn = pygame.Rect(250, 380, 400, 60)
        draw_button(start_btn, "Start")
        draw_button(noto_btn, "Open Noto Sans Download Page")

    elif current_screen == "HOME":
        draw_text("Symbols!", WIDTH // 2, 100, center=True)
        sym_btn = pygame.Rect(350, 250, 200, 60)
        tut_btn = pygame.Rect(350, 330, 200, 60)
        draw_button(sym_btn, "Symbols")
        draw_button(tut_btn, "Tutorial")

    elif current_screen == "SYMBOLS":
        draw_text("Enter input here:", 30, 200)
        pygame.draw.rect(screen, BLACK, (30, 240, 840, 40), 2)
        draw_text(input_text, 40, 250)

        if live_valid is not None:
            icon = "✔️" if live_valid else "❌"
            color = GREEN if live_valid else RED
            draw_text(icon, 850, 245, SMALL_FONT, color)

        draw_text(output_text, 30, 310, SMALL_FONT)

    elif current_screen == "TUTORIAL":
        steps = [
            'Type "Longest"',
            'Now type "Shortest"',
            'Now type "Exit"',
            'Tutorial complete!'
        ]
        draw_text(steps[tutorial_step], WIDTH // 2, 120, center=True)

        if tutorial_step < 3:
            draw_text("Enter input here:", 30, 240)
            pygame.draw.rect(screen, BLACK, (30, 280, 840, 40), 2)
            draw_text(input_text, 40, 290)
        else:
            ok_btn = pygame.Rect(400, 350, 100, 50)
            draw_button(ok_btn, "OK")

    elif current_screen == "EXIT":
        elapsed = time.time() - exit_start
        dots = "." * (int(elapsed * 2) % 3 + 1)
        draw_text(dots, WIDTH // 2, HEIGHT // 2, center=True)
        if elapsed >= 1.5:
            pygame.quit()
            sys.exit()

    pygame.display.flip()
    clock.tick(60)
