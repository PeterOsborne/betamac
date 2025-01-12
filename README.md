
# Betamac Math Game

## Overview
Betamac is a simple math game designed to enhance your arithmetic skills. Players solve randomly generated math questions within a set duration. The game records performance data, including total scores and question-specific details, to track progress over time.

---

## Features
- **Customizable Parameters:**
  - Set ranges for addition and multiplication questions.
  - Subtraction and division use ranges derived from addition and multiplication.
  - Adjustable game duration.
- **Performance Tracking:**
  - Saves question-level results to `math_game_results.csv`.
  - Records total score and game parameters to `math_game_summary.csv`.
- **Graphical User Interface:**
  - Built with `Tkinter` for a user-friendly experience.
- **Data Visualization:**
  - Analyze performance trends using Seaborn plots for scores and moving averages.

---

## Installation

1. **Clone the Repository:**
   ```bash
   git clone <repository_url>
   cd betamac
   ```

2. **Install Python Dependencies:**
   Ensure you have Python 3 installed. No external libraries are required for running the game. For visualization, install the following libraries:
   ```bash
   pip install pandas seaborn matplotlib
   ```

3. **Set Up Directories:**
   Ensure the `betamac.py` script has permission to write to the directory
<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->
 where it is located.

---

## Usage

### Running the Game
1. Open the terminal and navigate to the game directory:
   ```bash
   cd /path/to/betamac
   ```

2. Execute the game script:
   ```bash
   python3 betamac.py
   ```

3. Answer math questions displayed in the GUI. The game will end when the timer runs out.

### Customizing Parameters
Modify the following parameters at the top of `betamac.py` to suit your preferences:
```python
ADDITION_FIRST_RANGE = (2, 100)        # Range for the first number in addition
ADDITION_SECOND_RANGE = (2, 100)       # Range for the second number in addition
MULTIPLICATION_FIRST_RANGE = (2, 12)   # Range for the first number in multiplication
MULTIPLICATION_SECOND_RANGE = (2, 100) # Range for the second number in multiplication
DURATION = 30                          # Duration of the game in seconds
```

### Viewing Results
- **Question-Level Results:** Check `math_game_results.csv` for details about each question.
- **Summary Results:** Check `math_game_summary.csv` for overall performance and session parameters.

---

## Visualization
To analyze your performance, use the provided visualization script:

1. Open a Python notebook or script and load the summary data:
   ```python
   import pandas as pd
   import seaborn as sns
   import matplotlib.pyplot as plt

   summary_csv = "/path/to/math_game_summary.csv"
   summary_df = pd.read_csv(summary_csv)
   ```

2. Generate a plot of your score over time and moving average:
   ```python
   window_size = 5
   summary_df['Moving Average'] = summary_df['Total Score'].rolling(window=window_size).mean()

   sns.lineplot(data=summary_df, x=summary_df.index, y='Total Score', label='Total Score', marker='o')
   sns.lineplot(data=summary_df, x=summary_df.index, y='Moving Average', label=f'{window_size}-Game Moving Average', linestyle='--')

   plt.title("Performance Over Time (30s Sessions)")
   plt.xlabel("Game Number")
   plt.ylabel("Score")
   plt.legend()
   plt.show()
   ```

---

## File Outputs
1. **`math_game_results.csv`:**
   - Details about each question, including time spent and question type.

2. **`math_game_summary.csv`:**
   - Records total scores, game parameters, and session details.

---

## Troubleshooting
- **Results Not Saving:**
  - Ensure the script has write permissions in the specified directory.
  - Check that the `os.makedirs` function is creating necessary directories.

- **FileNotFoundError:**
  - Run the game at least once to generate the result files.
  - Verify file paths in the script.

---

## Future Improvements
- Add more question types, such as exponents or mixed operations.
- Implement leaderboards for competitive play.
- Allow real-time parameter adjustments via the GUI.

---

## License
This project is open-source and available under the MIT License.

---

## Contributions
Feel free to contribute! Submit a pull request or open an issue for suggestions.
