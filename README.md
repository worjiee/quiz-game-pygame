# Mathify 🧮

A beautiful, interactive Python-based math quiz game built with Pygame!

## Features

- **🎮 Built with Pygame**: Smooth graphics and game-like experience
- **🎨 Beautiful Graphics**: Modern design with smooth animations
- **🧮 Random Questions**: Addition, subtraction, multiplication, and division
- **📊 10 Questions Per Game**: Quick quiz sessions
- **✨ Visual Feedback**: Emojis and colors (🎉 for correct, 😕 for incorrect)
- **⏱️ Auto-Progress**: Advances automatically after 1.5 seconds
- **⌨️ Keyboard Support**: Type answers and press Enter
- **🏆 Real-time Score**: Live score tracking during gameplay
- **🖱️ Interactive Buttons**: Smooth hover effects
- **💬 Performance Messages**: Encouraging feedback based on your score
- **🔄 Play Again**: Replay without restarting the program
- **🖼️ Custom Logo**: Uses your mathifylogo.png as the window icon

## Screenshots Description

### 🏠 Welcome Screen
- Large title with emoji "🧮 Math Quiz Game 🧮"
- Description of the game
- Big "Start Quiz" button with hover effects

### ❓ Question Screen
- Progress indicator (Question X of 10)
- Current score display
- Large, clear question display
- Input field for your answer
- Submit button (or press Enter)

### ✓ Feedback Screen
- Emoji feedback (🎉 for correct, 😕 for incorrect)
- Color-coded feedback message (green/red)
- Current score update
- Automatically advances after 1.5 seconds

### 🏆 Results Screen
- Final score with large numbers
- Percentage score
- Performance-based emoji and message:
  - 🌟 "Perfect! Outstanding work!" (100%)
  - ⭐ "Excellent! You're a math star!" (80%+)
  - 👍 "Good job! Keep practicing!" (60%+)
  - 📚 "Not bad! Room for improvement!" (40%+)
  - 💪 "Keep trying! Practice makes perfect!" (<40%)
- "Play Again" and "Exit" buttons

## Installation

### Step 1: Install Pygame

```bash
pip install pygame
```

Or install from requirements.txt:
```bash
pip install -r requirements.txt
```

See [INSTALL.md](INSTALL.md) for detailed installation instructions.

## How to Run

### Quick Start

**Windows:** Double-click `run_game.bat`

**Mac/Linux:** 
```bash
chmod +x run_game.sh
./run_game.sh
```

**Or run directly:**
```bash
python mathify_pygame.py
```

### Playing the Game

1. **Click "Start Quiz"** to begin

2. **Answer each question:**
   - Type your answer in the input field
   - Press Enter or click "Submit Answer"

3. **View instant feedback** after each question
   - Correct answers show green with 🎉
   - Incorrect answers show red with 😕 and the correct answer

4. **See your final score** and performance message

5. **Play again** or exit from the results screen

## Requirements

- **Python 3.6 or higher**
- **Pygame 2.5.0 or higher**
- Built-in modules: `random`, `sys`

## Why Pygame?

Pygame is a popular game development library for Python:

✅ **Smoother graphics** - Better rendering and animations  
✅ **Game-focused** - Built specifically for games  
✅ **Better control** - More control over graphics and input  
✅ **60 FPS gameplay** - Smooth, responsive experience  
✅ **Cross-platform** - Works great on Windows, Mac, and Linux  
✅ **Active community** - Large community and lots of resources

## Code Structure

### Main Files
- `mathify_pygame.py` - Main Pygame game
- `mathifylogo.png` - Custom logo/icon

### Key Classes
- **`MathifyGame`**: Main game class
  - `__init__()` - Initialize Pygame window and game variables
  - `generate_question()` - Create random math problems
  - `draw_welcome_screen()` - Welcome screen with start button
  - `draw_question_screen()` - Question display with input
  - `check_answer()` - Validate user's answer
  - `draw_feedback_screen()` - Visual feedback screen
  - `draw_results_screen()` - Final score and performance message
  - `handle_events()` - Process keyboard and mouse input
  - `run()` - Main game loop (60 FPS)

- **`Button`**: Interactive button class
  - Hover effects
  - Click detection
  - Customizable colors

### Design Highlights
- **Pygame Engine**: 60 FPS smooth gameplay
- **800x600 Window**: Spacious, modern layout
- **Color Scheme**: Professional blues, greens, and reds
- **Smooth Animations**: Visual transitions and effects
- **Smart Questions**: 
  - Division ensures whole number results
  - Subtraction ensures positive results
  - Appropriate number ranges (1-50 for most operations)

## Future Improvements

Here are some great enhancements you could add:

### 1. ⏱️ Timer Feature
Add a time limit for each question or track total completion time:
- Timer countdown per question
- Bonus points for quick answers
- Total time tracking
- Time-based achievements

### 2. 🎯 Difficulty Levels
Let players choose Easy, Medium, or Hard before starting:
- **Easy**: Numbers 1-10
- **Medium**: Numbers 1-50
- **Hard**: Numbers 1-100, include decimals or negative numbers

### 3. 🏆 High Score System
Save high scores to a file and display leaderboard:
- Enter player name
- Save top 10 scores with timestamps
- Display leaderboard on welcome screen
- Personal best tracking

### 4. 📊 Statistics Tracking
Track performance by operation type:
- Accuracy by operation (+, -, ×, ÷)
- Average time per question
- Progress over time (graph)
- Identify weak areas for practice

### 5. 🎮 Game Modes
Different ways to play:
- **Lives Mode**: 3 lives, lose one per wrong answer
- **Streak Mode**: Consecutive correct answers for bonus points
- **Time Attack**: Answer as many as possible in 60 seconds
- **Endless Mode**: Keep playing until you make a mistake

### 6. 🎨 Themes & Customization
Visual customization options:
- Dark mode / Light mode toggle
- Color scheme selector
- Font size options
- Background patterns

### 7. 🔊 Sound Effects
Audio feedback for better engagement:
- Correct answer sound (ding!)
- Wrong answer sound (buzz)
- Victory music for high scores
- Background music toggle

### 8. 📈 Visual Enhancements
Better visual elements:
- Animated progress bar
- Confetti animation for perfect scores
- Smooth transitions between screens
- Chart/graph of performance

### 9. ⚙️ Settings Menu
Customization options:
- Number of questions (5, 10, 15, 20)
- Choose which operations to practice
- Sound on/off
- Auto-advance speed
- Difficulty setting

### 10. 🌐 Multiplayer Mode
Compete with others:
- Two-player mode (same computer)
- Online leaderboard
- Challenge friends
- Tournament mode

## Troubleshooting

### Pygame Installation Issues

**"No module named 'pygame'" error:**
```bash
pip install pygame
# Or try:
python -m pip install pygame
```

**Permission errors on Mac/Linux:**
```bash
pip3 install --user pygame
```

**Linux missing dependencies:**
```bash
sudo apt-get install python3-pygame
# OR install dependencies manually:
sudo apt-get install python3-dev libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev
pip3 install pygame
```

### Game Not Starting
- Make sure Pygame is installed: `pip list | grep pygame`
- Check Python version: `python --version` (need 3.6+)
- Try running: `python -m pygame.examples.aliens` to test Pygame
- Make sure `mathifylogo.png` is in the same folder

### Performance Issues
- Close other applications to free up resources
- Update your graphics drivers
- Pygame runs at 60 FPS - this is normal and smooth

## License

This project is free to use and modify for educational purposes.

## Contributing

Feel free to fork this project and add your own improvements! Some ideas:
- Add the suggested features above
- Improve the UI/UX design
- Add new question types (exponents, square roots, etc.)
- Create difficulty levels
- Add sound effects

---

**Enjoy the game and happy learning! 🎉**

