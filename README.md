# Battleship Game (Pygame)

This is a **Battleship** game implemented using Python and **Pygame**. Players take turns attacking the opponent's grid, attempting to sink all their ships. The game features AI opponent placement and a simple user interface for selecting and attacking ships.

---

## **Features**
- Classic Battleship game mechanics
- AI opponent with random ship placement
- Interactive grid-based UI using **Pygame**
- Visual hit/miss feedback
- Ship placement rotation using right-click

---

## **Installation & Setup**

### **1. Install Python**
Ensure you have **Python 3.x** installed. You can download it from [python.org](https://www.python.org/).

### **2. Install Required Dependencies**
Before running the game, install dependencies using:
```bash
pip install -r requirements.txt
```

Alternatively, manually install **Pygame**:
```bash
pip install pygame
```

### **3. Run the Game**
Execute the following command:
```bash
python battleship.py
```

---

## **Gameplay Instructions**

### **1. Ship Placement**
- Place your ships by clicking on the grid.
- Right-click to rotate the ship before placing it.
- The AI automatically places its ships.

### **2. Taking Turns**
- Click on the opponent’s grid to attack.
- The AI will take turns attacking your grid.
- Hits are marked in **pink**, and misses in **gray**.

### **3. Winning the Game**
- The game ends when all of an opponent’s ships are sunk.
- A **"You Win!"** or **"You Lose!"** message will appear.

---

## **File Structure**
```
/your_project_directory
│── battleship.py          # Main game file
│── requirements.txt       # Python dependencies
│── README.md              # Project documentation
```

---

## **Future Improvements**
- Add multiplayer mode (local or online)
- Improve AI difficulty
- Add animations and sound effects

---

## **License**
This project is for educational purposes and can be modified and distributed freely.

---

Enjoy playing Battleship! 🚢🎯

