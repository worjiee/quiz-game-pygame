import random
import pygame
import sys
import math
import os

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Colors
BG_COLOR = (240, 244, 248)
PRIMARY_COLOR = (74, 144, 226)
PRIMARY_DARK = (53, 122, 189)
SUCCESS_COLOR = (76, 175, 80)
SUCCESS_DARK = (69, 160, 73)
ERROR_COLOR = (244, 67, 54)
ERROR_DARK = (211, 47, 47)
TEXT_COLOR = (44, 62, 80)
WHITE = (255, 255, 255)
DARK_GRAY = (100, 100, 100)
LIGHT_GRAY = (200, 200, 200)
SHADOW_COLOR = (0, 0, 0, 30)

# Fonts
TITLE_FONT = None
LARGE_FONT = None
MEDIUM_FONT = None
SMALL_FONT = None


class Particle:
    """A particle for celebration effects."""
    
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-8, -3)
        self.color = color
        self.size = random.randint(3, 7)
        self.lifetime = 60
        self.age = 0
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.3  # Gravity
        self.age += 1
    
    def draw(self, screen):
        alpha = max(0, 255 * (1 - self.age / self.lifetime))
        if alpha > 0:
            size = int(self.size * (1 - self.age / self.lifetime))
            if size > 0:
                s = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
                pygame.draw.circle(s, (*self.color, int(alpha)), (size, size), size)
                screen.blit(s, (int(self.x - size), int(self.y - size)))
    
    def is_dead(self):
        return self.age >= self.lifetime


class Button:
    """A clickable button with hover effects and animations."""
    
    def __init__(self, x, y, width, height, text, color, hover_color, text_color=WHITE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
        self.scale = 1.0
        self.target_scale = 1.0
    
    def update(self):
        """Update button animation."""
        self.target_scale = 1.05 if self.is_hovered else 1.0
        self.scale += (self.target_scale - self.scale) * 0.3
    
    def draw(self, screen):
        """Draw the button with shadow and animations."""
        # Calculate scaled dimensions
        scaled_width = int(self.rect.width * self.scale)
        scaled_height = int(self.rect.height * self.scale)
        scaled_rect = pygame.Rect(
            self.rect.centerx - scaled_width // 2,
            self.rect.centery - scaled_height // 2,
            scaled_width,
            scaled_height
        )
        
        # Draw shadow
        shadow_rect = scaled_rect.copy()
        shadow_rect.y += 4
        shadow_surface = pygame.Surface((shadow_rect.width, shadow_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surface, SHADOW_COLOR, shadow_surface.get_rect(), border_radius=10)
        screen.blit(shadow_surface, shadow_rect)
        
        # Draw button
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, scaled_rect, border_radius=10)
        
        # Draw text
        text_surface = MEDIUM_FONT.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=scaled_rect.center)
        screen.blit(text_surface, text_rect)
    
    def check_hover(self, mouse_pos):
        """Check if mouse is hovering over button."""
        self.is_hovered = self.rect.collidepoint(mouse_pos)
    
    def is_clicked(self, mouse_pos, mouse_clicked):
        """Check if button was clicked."""
        return self.rect.collidepoint(mouse_pos) and mouse_clicked


class MathifyGame:
    """Main game class for Mathify."""
    
    def __init__(self):
        """Initialize the game."""
        self.is_fullscreen = False
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Mathify")
        # Load custom logo if available (works in dev and when bundled)
        try:
            logo_path = self._resource_path("mathifylogo.png")
            logo = pygame.image.load(logo_path).convert_alpha()
            pygame.display.set_icon(logo)
        except:
            pass
        
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Game state
        self.state = "welcome"
        self.difficulty = None  # 'easy', 'medium', 'hard'
        self.total_questions = 10
        self.current_question = 0
        self.score = 0
        self.user_input = ""
        self.question_text = ""
        self.correct_answer = 0
        self.is_correct = False
        self.feedback_timer = 0
        
        # Timer
        self.time_limit = 15  # seconds per question
        self.question_start_time = 0
        self.time_remaining = self.time_limit
        self.time_bonus = 0
        
        # Animation
        self.fade_alpha = 0
        self.fade_in = True
        self.pulse = 0
        self.particles = []
        self.progress_width = 0
        self.target_progress_width = 0
        
        # Button click state
        self.mouse_clicked_last_frame = False
        
        # Initialize fonts
        global TITLE_FONT, LARGE_FONT, MEDIUM_FONT, SMALL_FONT
        TITLE_FONT = pygame.font.Font(None, 72)
        LARGE_FONT = pygame.font.Font(None, 56)
        MEDIUM_FONT = pygame.font.Font(None, 36)
        SMALL_FONT = pygame.font.Font(None, 28)

    def toggle_fullscreen(self):
        """Toggle fullscreen using safe flags to avoid renderer errors."""
        self.is_fullscreen = not self.is_fullscreen
        base_size = (WINDOW_WIDTH, WINDOW_HEIGHT)
        try:
            if self.is_fullscreen:
                # Standard fullscreen (driver-selected size)
                self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            else:
                # Windowed, resizable
                self.screen = pygame.display.set_mode(base_size, pygame.RESIZABLE)
        except pygame.error:
            # Final fallback: simple windowed mode
            self.is_fullscreen = False
            self.screen = pygame.display.set_mode(base_size)
    
    def generate_question(self):
        """Generate a random math question based on difficulty."""
        if self.difficulty == 'easy':
            operations = ['+', '-']
            num1 = random.randint(1, 20)
            num2 = random.randint(1, 20)
        elif self.difficulty == 'medium':
            operations = ['+', '-', '*']
            num1 = random.randint(1, 50)
            num2 = random.randint(1, 50)
        else:  # hard
            operations = ['+', '-', '*', '/']
            num1 = random.randint(1, 1000)
            num2 = random.randint(1, 1000)
        
        operation = random.choice(operations)
        
        if operation == '/':
            # Ensure division results in whole numbers
            num2 = random.randint(2, 12)
            answer = random.randint(1, 12)
            num1 = num2 * answer
        else:
            if operation == '-' and num1 < num2:
                num1, num2 = num2, num1
        
        if operation == '+':
            answer = num1 + num2
        elif operation == '-':
            answer = num1 - num2
        elif operation == '*':
            answer = num1 * num2
        else:
            answer = num1 // num2
        
        question = f"{num1} {operation} {num2}"
        return question, answer
    
    def draw_text_with_shadow(self, text, font, color, x, y, center=True):
        """Draw text with a subtle shadow."""
        # Shadow
        shadow_surface = font.render(text, True, DARK_GRAY)
        if center:
            shadow_rect = shadow_surface.get_rect(center=(x + 2, y + 2))
        else:
            shadow_rect = shadow_surface.get_rect(topleft=(x + 2, y + 2))
        
        shadow_with_alpha = pygame.Surface(shadow_surface.get_size(), pygame.SRCALPHA)
        shadow_with_alpha.blit(shadow_surface, (0, 0))
        shadow_with_alpha.set_alpha(50)
        self.screen.blit(shadow_with_alpha, shadow_rect)
        
        # Main text
        text_surface = font.render(text, True, color)
        if center:
            text_rect = text_surface.get_rect(center=(x, y))
        else:
            text_rect = text_surface.get_rect(topleft=(x, y))
        self.screen.blit(text_surface, text_rect)
    
    def draw_card(self, rect, color=WHITE):
        """Draw a card-like container with shadow."""
        # Shadow
        shadow_rect = rect.copy()
        shadow_rect.y += 6
        shadow_surface = pygame.Surface((shadow_rect.width, shadow_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surface, SHADOW_COLOR, shadow_surface.get_rect(), border_radius=15)
        self.screen.blit(shadow_surface, shadow_rect)
        
        # Card
        pygame.draw.rect(self.screen, color, rect, border_radius=15)
    
    def draw_progress_bar(self):
        """Draw an animated progress bar."""
        bar_width = 600
        bar_height = 20
        x = (WINDOW_WIDTH - bar_width) // 2
        y = 20
        
        # Background
        bg_rect = pygame.Rect(x, y, bar_width, bar_height)
        pygame.draw.rect(self.screen, LIGHT_GRAY, bg_rect, border_radius=10)
        
        # Progress
        progress = self.current_question / self.total_questions
        self.target_progress_width = int(bar_width * progress)
        self.progress_width += (self.target_progress_width - self.progress_width) * 0.1
        
        if self.progress_width > 0:
            progress_rect = pygame.Rect(x, y, int(self.progress_width), bar_height)
            pygame.draw.rect(self.screen, PRIMARY_COLOR, progress_rect, border_radius=10)
    
    def draw_welcome_screen(self):
        """Draw the welcome screen with animations."""
        self.screen.fill(BG_COLOR)
        
        # Animated background circles
        self.pulse += 0.05
        for i in range(3):
            radius = 100 + i * 80 + int(math.sin(self.pulse + i) * 20)
            alpha = 20 - i * 5
            surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(surface, (*PRIMARY_COLOR, alpha), (radius, radius), radius)
            self.screen.blit(surface, (WINDOW_WIDTH // 2 - radius, 150 - radius))
        
        # Title card
        title_card = pygame.Rect(150, 80, 500, 180)
        self.draw_card(title_card)
        
        # Title
        self.draw_text_with_shadow("Mathify", TITLE_FONT, PRIMARY_COLOR, 
                                   WINDOW_WIDTH // 2, 150)
        
        # Subtitle
        self.draw_text_with_shadow("Test Your Math Skills", MEDIUM_FONT, TEXT_COLOR,
                                   WINDOW_WIDTH // 2, 210)
        
        # Info text
        self.draw_text_with_shadow("Choose your difficulty level", 
                                   SMALL_FONT, DARK_GRAY, WINDOW_WIDTH // 2, 300)
        
        # Difficulty buttons
        easy_button = Button(WINDOW_WIDTH // 2 - 320, 360, 180, 60, 
                            "Easy", SUCCESS_COLOR, SUCCESS_DARK)
        medium_button = Button(WINDOW_WIDTH // 2 - 90, 360, 180, 60, 
                              "Medium", (255, 152, 0), (230, 137, 0))
        hard_button = Button(WINDOW_WIDTH // 2 + 140, 360, 180, 60, 
                            "Hard", ERROR_COLOR, ERROR_DARK)
        
        # Difficulty descriptions
        self.draw_text_with_shadow("1-20", SMALL_FONT, TEXT_COLOR,
                                   WINDOW_WIDTH // 2 - 230, 450)
        self.draw_text_with_shadow("+  -", SMALL_FONT, DARK_GRAY,
                                   WINDOW_WIDTH // 2 - 230, 475)
        
        self.draw_text_with_shadow("1-50", SMALL_FONT, TEXT_COLOR,
                                   WINDOW_WIDTH // 2, 450)
        self.draw_text_with_shadow("+  -  ×", SMALL_FONT, DARK_GRAY,
                                   WINDOW_WIDTH // 2, 475)
        
        self.draw_text_with_shadow("1-100", SMALL_FONT, TEXT_COLOR,
                                   WINDOW_WIDTH // 2 + 230, 450)
        self.draw_text_with_shadow("+  -  ×  ÷", SMALL_FONT, DARK_GRAY,
                                   WINDOW_WIDTH // 2 + 230, 475)
        
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        mouse_clicked = mouse_pressed and not self.mouse_clicked_last_frame
        
        easy_button.check_hover(mouse_pos)
        medium_button.check_hover(mouse_pos)
        hard_button.check_hover(mouse_pos)
        
        easy_button.update()
        medium_button.update()
        hard_button.update()
        
        easy_button.draw(self.screen)
        medium_button.draw(self.screen)
        hard_button.draw(self.screen)
        
        if easy_button.is_clicked(mouse_pos, mouse_clicked):
            self.difficulty = 'easy'
            self.state = "question"
            self.current_question = 0
            self.score = 0
            self.start_new_question()
        
        if medium_button.is_clicked(mouse_pos, mouse_clicked):
            self.difficulty = 'medium'
            self.state = "question"
            self.current_question = 0
            self.score = 0
            self.start_new_question()
        
        if hard_button.is_clicked(mouse_pos, mouse_clicked):
            self.difficulty = 'hard'
            self.state = "question"
            self.current_question = 0
            self.score = 0
            self.start_new_question()
    
    def start_new_question(self):
        """Start a new question."""
        self.current_question += 1
        self.user_input = ""
        self.question_text, self.correct_answer = self.generate_question()
        self.question_start_time = pygame.time.get_ticks()
        self.time_remaining = self.time_limit
    
    def draw_question_screen(self):
        """Draw the question screen with enhanced visuals."""
        self.screen.fill(BG_COLOR)
        
        # Update time remaining
        elapsed_time = (pygame.time.get_ticks() - self.question_start_time) / 1000
        self.time_remaining = max(0, self.time_limit - elapsed_time)
        
        # Check if time ran out
        if self.time_remaining <= 0 and self.state == "question":
            self.is_correct = False
            self.state = "feedback"
            self.feedback_timer = pygame.time.get_ticks()
            return
        
        # Progress bar
        self.draw_progress_bar()
        
        # Stats card
        stats_card = pygame.Rect(50, 60, 700, 50)
        self.draw_card(stats_card)
        
        # Progress text
        progress_text = f"Question {self.current_question} of {self.total_questions}"
        self.draw_text_with_shadow(progress_text, SMALL_FONT, TEXT_COLOR, 
                                   WINDOW_WIDTH // 2 - 150, 85)
        
        # Score (show raw points only)
        score_text = f"Score: {self.score} pts"
        self.draw_text_with_shadow(score_text, SMALL_FONT, PRIMARY_COLOR, 
                                   WINDOW_WIDTH // 2 + 150, 85)
        
        # Timer display with color coding
        timer_y = 130
        if self.time_remaining > 10:
            timer_color = SUCCESS_COLOR
        elif self.time_remaining > 5:
            timer_color = (255, 152, 0)  # Orange
        else:
            timer_color = ERROR_COLOR
            # Pulse effect when time is running out
            if int(self.time_remaining * 2) % 2 == 0:
                timer_y += 2
        
        # Timer background circle
        timer_radius = 40
        timer_center = (WINDOW_WIDTH // 2, timer_y)
        
        # Draw timer circle background
        pygame.draw.circle(self.screen, WHITE, timer_center, timer_radius)
        pygame.draw.circle(self.screen, timer_color, timer_center, timer_radius, 4)
        
        # Draw timer arc (progress)
        if self.time_remaining > 0:
            progress_angle = (self.time_remaining / self.time_limit) * 360
            points = [timer_center]
            for angle in range(int(progress_angle) + 1):
                rad = math.radians(angle - 90)
                x = timer_center[0] + (timer_radius - 8) * math.cos(rad)
                y = timer_center[1] + (timer_radius - 8) * math.sin(rad)
                points.append((x, y))
            if len(points) > 2:
                pygame.draw.polygon(self.screen, (*timer_color, 50), points)
        
        # Timer text
        timer_text = f"{int(self.time_remaining)}"
        self.draw_text_with_shadow(timer_text, LARGE_FONT, timer_color,
                                   timer_center[0], timer_center[1])
        
        # Question card
        question_card = pygame.Rect(100, 200, 600, 250)
        self.draw_card(question_card)
        
        # Question label
        self.draw_text_with_shadow("What is:", MEDIUM_FONT, TEXT_COLOR, 
                                   WINDOW_WIDTH // 2, 240)
        
        # Question with pulse effect
        pulse_scale = 1.0 + math.sin(self.pulse * 2) * 0.02
        question_font = pygame.font.Font(None, int(56 * pulse_scale))
        self.draw_text_with_shadow(self.question_text, question_font, PRIMARY_COLOR, 
                                   WINDOW_WIDTH // 2, 300)
        
        # Input box
        input_box = pygame.Rect(WINDOW_WIDTH // 2 - 120, 360, 240, 60)
        pygame.draw.rect(self.screen, WHITE, input_box, border_radius=10)
        pygame.draw.rect(self.screen, PRIMARY_COLOR, input_box, 3, border_radius=10)
        
        # User input
        input_text = self.user_input if self.user_input else "?"
        input_surface = MEDIUM_FONT.render(input_text, True, TEXT_COLOR if self.user_input else LIGHT_GRAY)
        input_rect = input_surface.get_rect(center=input_box.center)
        self.screen.blit(input_surface, input_rect)
        
        # Submit button
        submit_button = Button(WINDOW_WIDTH // 2 - 100, 490, 200, 50, 
                              "Submit", PRIMARY_COLOR, PRIMARY_DARK)
        
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        mouse_clicked = mouse_pressed and not self.mouse_clicked_last_frame
        
        submit_button.check_hover(mouse_pos)
        submit_button.update()
        submit_button.draw(self.screen)
        
        if submit_button.is_clicked(mouse_pos, mouse_clicked) and self.user_input:
            self.check_answer()
    
    def check_answer(self):
        """Check if the user's answer is correct."""
        try:
            user_answer = int(self.user_input)
            self.is_correct = (user_answer == self.correct_answer)
            
            # Calculate time bonus (up to 5 bonus points for fast answers)
            self.time_bonus = 0
            if self.is_correct:
                time_percentage = self.time_remaining / self.time_limit
                if time_percentage > 0.8:  # Answered in first 20% of time
                    self.time_bonus = 5
                elif time_percentage > 0.6:
                    self.time_bonus = 3
                elif time_percentage > 0.4:
                    self.time_bonus = 1
                
                self.score += 1 + self.time_bonus
                
                # Create celebration particles
                for _ in range(30):
                    self.particles.append(Particle(
                        WINDOW_WIDTH // 2,
                        WINDOW_HEIGHT // 2,
                        random.choice([SUCCESS_COLOR, (255, 215, 0), PRIMARY_COLOR])
                    ))
            
            self.state = "feedback"
            self.feedback_timer = pygame.time.get_ticks()
        except ValueError:
            pass
    
    def draw_feedback_screen(self):
        """Draw the feedback screen with animations."""
        self.screen.fill(BG_COLOR)
        
        # Update and draw particles
        for particle in self.particles[:]:
            particle.update()
            particle.draw(self.screen)
            if particle.is_dead():
                self.particles.remove(particle)
        
        # Feedback card
        feedback_card = pygame.Rect(150, 100, 500, 400)
        self.draw_card(feedback_card)
        
        if self.is_correct:
            emoji = None
            feedback_text = "GALING!"
            color = SUCCESS_COLOR
            
            # Show time bonus if earned
            if self.time_bonus > 0:
                bonus_text = f"+{self.time_bonus} Time Bonus!"
                self.draw_text_with_shadow(bonus_text, SMALL_FONT, (255, 215, 0),
                                          WINDOW_WIDTH // 2, 180)
        else:
            emoji = None
            if self.time_remaining <= 0:
                feedback_text = "BOBO"
            else:
                feedback_text = "HAHA TANGA"
            color = ERROR_COLOR
        
        # Big feedback word (replaces emoji)
        scale = 1.0 + math.sin(self.pulse * 3) * 0.1
        word_font = pygame.font.Font(None, int(72 * scale))
        self.draw_text_with_shadow(feedback_text, word_font, TEXT_COLOR,
                                   WINDOW_WIDTH // 2, 220)
        
        # Subtext line for additional clarity (Correct!/Incorrect detail)
        subtext = "Correct!" if self.is_correct else ("Time's Up!" if self.time_remaining <= 0 else "Incorrect")
        self.draw_text_with_shadow(subtext, LARGE_FONT, color,
                                   WINDOW_WIDTH // 2, 310)
        
        if not self.is_correct:
            answer_text = f"The correct answer was {self.correct_answer}"
            self.draw_text_with_shadow(answer_text, MEDIUM_FONT, TEXT_COLOR, 
                                       WINDOW_WIDTH // 2, 370)
        
        # Current score
        score_text = f"Current Score: {self.score} pts"
        self.draw_text_with_shadow(score_text, MEDIUM_FONT, PRIMARY_COLOR, 
                                   WINDOW_WIDTH // 2, 440)
        
        # Auto-advance after 1.5 seconds
        if pygame.time.get_ticks() - self.feedback_timer > 1500:
            if self.current_question < self.total_questions:
                self.state = "question"
                self.start_new_question()
            else:
                self.state = "results"
    
    def draw_results_screen(self):
        """Draw the final results screen."""
        self.screen.fill(BG_COLOR)
        
        # Calculate percentage out of maximum possible points (6 per question)
        max_points_total = self.total_questions * 6
        percentage = (self.score / max_points_total) * 100 if max_points_total > 0 else 0
        
        # Determine message and emoji
        if percentage == 100:
            message = "Perfect! Outstanding work!"
            emoji = "★"
            color = (255, 215, 0)
        elif percentage >= 80:
            message = "Excellent! You're a math star!"
            emoji = "★"
            color = SUCCESS_COLOR
        elif percentage >= 60:
            message = "Good job! Keep practicing!"
            emoji = "+"
            color = PRIMARY_COLOR
        elif percentage >= 40:
            message = "Not bad! Room for improvement!"
            emoji = "•"
            color = (255, 152, 0)
        else:
            message = "Keep trying! Practice makes perfect!"
            emoji = "↑"
            color = ERROR_COLOR
        
        # Results card
        results_card = pygame.Rect(100, 50, 600, 400)
        self.draw_card(results_card)
        
        # Title
        self.draw_text_with_shadow("Quiz Complete!", LARGE_FONT, PRIMARY_COLOR, 
                                   WINDOW_WIDTH // 2, 100)
        
        # Emoji
        emoji_scale = 1.0 + math.sin(self.pulse * 2) * 0.05
        emoji_font = pygame.font.Font(None, int(72 * emoji_scale))
        self.draw_text_with_shadow(emoji, emoji_font, TEXT_COLOR, 
                                   WINDOW_WIDTH // 2, 180)
        
        # Score (raw points only)
        score_text = f"{self.score} pts"
        self.draw_text_with_shadow(score_text, LARGE_FONT, color, 
                                   WINDOW_WIDTH // 2, 260)
        
        # Percentage
        percentage_text = f"{percentage:.1f}%"
        self.draw_text_with_shadow(percentage_text, MEDIUM_FONT, TEXT_COLOR, 
                                   WINDOW_WIDTH // 2, 320)
        
        # Message
        self.draw_text_with_shadow(message, SMALL_FONT, color, 
                                   WINDOW_WIDTH // 2, 380)
        
        # Buttons
        play_again_button = Button(WINDOW_WIDTH // 2 - 220, 480, 180, 50, 
                                   "Play Again", SUCCESS_COLOR, SUCCESS_DARK)
        exit_button = Button(WINDOW_WIDTH // 2 + 40, 480, 180, 50, 
                            "Exit", ERROR_COLOR, ERROR_DARK)
        
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        mouse_clicked = mouse_pressed and not self.mouse_clicked_last_frame
        
        play_again_button.check_hover(mouse_pos)
        exit_button.check_hover(mouse_pos)
        
        play_again_button.update()
        exit_button.update()
        
        play_again_button.draw(self.screen)
        exit_button.draw(self.screen)
        
        if play_again_button.is_clicked(mouse_pos, mouse_clicked):
            self.state = "welcome"
            self.difficulty = None
            self.current_question = 0
            self.score = 0
            self.progress_width = 0
            self.target_progress_width = 0
        
        if exit_button.is_clicked(mouse_pos, mouse_clicked):
            self.running = False
    
    def handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            # Resize window safely without SCALED to avoid renderer issues
            if event.type == pygame.VIDEORESIZE and not self.is_fullscreen:
                new_size = (max(400, event.w), max(300, event.h))
                self.screen = pygame.display.set_mode(new_size, pygame.RESIZABLE)
            
            if self.state == "question" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and self.user_input:
                    self.check_answer()
                elif event.key == pygame.K_BACKSPACE:
                    self.user_input = self.user_input[:-1]
                elif event.unicode.isdigit() or (event.unicode == '-' and not self.user_input):
                    if len(self.user_input) < 10:
                        self.user_input += event.unicode
            # Global keys
            if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                self.toggle_fullscreen()

    def _resource_path(self, relative_path):
        """Return absolute path for resource both in dev and PyInstaller bundle."""
        if hasattr(sys, "_MEIPASS"):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)
    
    def run(self):
        """Main game loop."""
        while self.running:
            # Track mouse click state
            mouse_pressed = pygame.mouse.get_pressed()[0]
            
            self.handle_events()
            
            # Update animations
            self.pulse += 0.05
            
            # Draw current state
            if self.state == "welcome":
                self.draw_welcome_screen()
            elif self.state == "question":
                self.draw_question_screen()
            elif self.state == "feedback":
                self.draw_feedback_screen()
            elif self.state == "results":
                self.draw_results_screen()
            
            pygame.display.flip()
            self.clock.tick(FPS)
            
            # Update mouse click state for next frame
            self.mouse_clicked_last_frame = mouse_pressed
        
        pygame.quit()
        sys.exit()


def main():
    """Main entry point."""
    game = MathifyGame()
    game.run()


if __name__ == "__main__":
    main()