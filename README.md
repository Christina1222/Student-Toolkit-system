# TARUMT Student Toolkit

A comprehensive Python-based student management application featuring GPA Calculator, Homework Planner, Pomodoro Timer, and Flashcards system.

## 🚀 Features

### 1. GPA Calculator
- Add/remove courses with credits and grades
- Calculate cumulative GPA
- Track GPA history and trends
- Grade distribution analysis

### 2. Homework Planner
- Create and manage homework assignments
- Set due dates and priorities
- Track completion status
- Color-coded status indicators

### 3. Pomodoro Timer
- Customizable work/break intervals
- Session tracking and statistics
- Multiple timer modes (Work, Short Break, Long Break)
- Progress monitoring

### 4. Flashcards System
- Create multiple flashcard decks
- Support for open-ended and multiple-choice questions
- Quiz functionality with randomization
- Database storage for persistence

## 📋 Requirements

### System Requirements
- **Operating System**: Windows 10/11, macOS 10.14+, or Linux
- **Python Version**: Python 3.8 or higher
- **Memory**: Minimum 512MB RAM
- **Storage**: 50MB free disk space

### Python Dependencies

#### Standard Library (Included with Python)
- `tkinter` - GUI framework
- `json` - Data serialization
- `sqlite3` - Database operations
- `datetime` - Date/time handling
- `dataclasses` - Data structure management
- `typing` - Type hints
- `random` - Randomization
- `os` - Operating system interface

#### External Dependencies (Requires Installation)
For GPA Calculator charts and statistics visualization:
- `matplotlib` - Chart generation and plotting
- `numpy` - Numerical computations for chart data

**Installation Command:**
```bash
pip install matplotlib numpy
```

**Alternative Installation:**
```bash
pip install -r requirements.txt
```

## 🔧 Installation

### Step 1: Verify Python Installation

1. Open Command Prompt (Windows) or Terminal (macOS/Linux)
2. Check Python version:
   ```bash
   python --version
   ```
   or
   ```bash
   python3 --version
   ```

3. Ensure you have Python 3.8 or higher. If not, download from [python.org](https://www.python.org/downloads/)

### Step 2: Download the Project

1. Download or clone the project files
2. Extract to your desired location (e.g., `C:\Users\YourName\TARUMT_Student_Toolkit`)

### Step 3: Install Chart Dependencies

For GPA Calculator charts and statistics visualization, install the required packages:

```bash
pip install matplotlib numpy
```

**Note:** If you encounter any installation issues:
- On Windows: You may need to install Microsoft Visual C++ Build Tools
- On macOS: You may need Xcode command line tools
- On Linux: Install python3-dev and build-essential packages

### Step 4: Verify Project Structure

Ensure your project directory contains:
```
Software Assignment/
├── main.py
├── main_gui.py
├── flashcards_app.py
├── F_app.py
├── F_models.py
├── F_ui_components.py
├── F_database.py
├── F_utils.py
├── utils.py
├── core/
│   ├── __init__.py
│   ├── gpa.py
│   ├── homework.py
│   ├── pomodoro.py
│   ├── flashcards.py
│   └── storage.py
├── data/
│   ├── flashcards.json
│   ├── gpa_history.json
│   ├── homework.json
│   ├── pomodoro.json
│   └── flashcard.db
└── README.md
```

### Step 4: Test Installation

1. Navigate to the project directory:
   ```bash
   cd "Software Assignment"
   ```

2. Run a quick test:
   ```bash
   python main.py
   ```

## 🎮 Usage

### Launching the Application

#### Option 1: GUI Mode (Recommended)
```bash
python main_gui.py
```

#### Option 2: Console Mode
```bash
python main.py
```

### Using the Features

#### GPA Calculator
1. Click "GPA Calculator" from the main menu
2. Add courses with name, credits, and grade
3. View calculated GPA and statistics
4. Access GPA history and trends

#### Homework Planner
1. Click "Homework Planner" from the main menu
2. Add new homework assignments
3. Set due dates, priorities, and details
4. Mark assignments as complete
5. Filter by status (Pending, In Progress, Completed)

#### Pomodoro Timer
1. Click "Pomodoro Timer" from the main menu
2. Configure work/break intervals
3. Start timer sessions
4. Track completed sessions and statistics

#### Flashcards
1. Click "Flashcards" from the main menu
2. Create new flashcard decks
3. Add questions and answers
4. Take quizzes and track progress

## 📁 Project Structure

```
Software Assignment/
├── main.py                    # Console-based main application
├── main_gui.py               # GUI-based main application
├── flashcards_app.py         # Flashcards GUI application
├── F_app.py                  # Flashcards core application logic
├── F_models.py               # Flashcards data models
├── F_ui_components.py        # Flashcards UI components
├── F_database.py             # Flashcards database operations
├── F_utils.py                # Flashcards utility functions
├── utils.py                  # General utility functions
├── core/                     # Core application modules
│   ├── __init__.py          # Package initialization
│   ├── gpa.py               # GPA calculation logic
│   ├── homework.py          # Homework management logic
│   ├── pomodoro.py          # Pomodoro timer logic
│   ├── flashcards.py        # Flashcards core logic
│   └── storage.py           # Data storage management
├── data/                     # Data storage directory
│   ├── flashcards.json      # Flashcards data (JSON)
│   ├── gpa_history.json     # GPA history data
│   ├── homework.json        # Homework assignments data
│   ├── pomodoro.json        # Pomodoro settings and state
│   └── flashcard.db         # Flashcards database (SQLite)
└── README.md                # This file
```

## ⚙️ Configuration

### Data Storage
- **JSON Files**: Store application data in `data/` directory
- **SQLite Database**: Used for flashcards (automatic creation)
- **Backup**: Regularly backup the `data/` directory

### Customization
- **Pomodoro Settings**: Modify default work/break intervals in `core/pomodoro.py`
- **GPA Scale**: Adjust grade points in `core/gpa.py`
- **UI Colors**: Customize interface colors in `main_gui.py`

### File Permissions
Ensure the application has read/write permissions to:
- Project directory
- `data/` subdirectory
- JSON and database files

## 🔧 Troubleshooting

### Common Issues

#### Issue: "ModuleNotFoundError: No module named 'tkinter'"
**Solution**: Install tkinter (usually included with Python)
- **Windows**: Reinstall Python with tkinter option checked
- **macOS**: Install python3-tk: `brew install python-tk`
- **Linux**: Install python3-tk: `sudo apt-get install python3-tk`

#### Issue: "Permission denied" when saving data
**Solution**: 
1. Run as administrator (Windows) or with sudo (Linux/macOS)
2. Check file permissions in the `data/` directory
3. Ensure the application has write access

#### Issue: GUI window doesn't appear
**Solution**:
1. Check if another instance is already running
2. Try running in console mode first: `python main.py`
3. Verify tkinter installation

#### Issue: Database errors
**Solution**:
1. Delete `data/flashcard.db` to reset the database
2. Ensure write permissions in the `data/` directory
3. Check for file corruption

#### Issue: Chart/Graph not displaying in GPA Calculator
**Solution**:
1. Install required packages: `pip install matplotlib numpy`
2. Check if matplotlib backend is properly configured
3. Try running: `python -c "import matplotlib; print(matplotlib.get_backend())"`
4. On some systems, you may need: `pip install matplotlib[all]`

#### Issue: "No module named 'matplotlib'" error
**Solution**:
1. Install matplotlib: `pip install matplotlib`
2. If using virtual environment, ensure it's activated
3. Try: `pip install --upgrade pip` then `pip install matplotlib`
4. On Windows, you may need Microsoft Visual C++ Build Tools

### Performance Issues

#### Slow startup
- Ensure Python 3.8+ is being used
- Close other applications to free memory
- Check for large data files in `data/` directory

#### GUI responsiveness
- Reduce the number of homework items or flashcards
- Close unused application windows
- Restart the application periodically

## 🔍 Technical Details

### Architecture
- **MVC Pattern**: Separation of data models, business logic, and UI
- **Object-Oriented Design**: Classes with inheritance and encapsulation
- **Data Persistence**: JSON and SQLite for different data types
- **Event-Driven GUI**: Tkinter-based responsive interface

### Key Technologies
- **Python 3.8+**: Core programming language
- **Tkinter**: Native GUI framework
- **SQLite3**: Embedded database for flashcards
- **JSON**: Lightweight data interchange
- **Dataclasses**: Modern Python data structures
- **Matplotlib**: Chart generation and data visualization
- **NumPy**: Numerical computations for statistical analysis

### Data Flow
1. **User Input** → GUI Components
2. **GUI Components** → Business Logic Classes
3. **Business Logic** → Data Storage Layer
4. **Data Storage** → File System (JSON/SQLite)

### Security Considerations
- All data stored locally (no network transmission)
- Input validation on all user entries
- File permission checks for data access
- Error handling for data corruption

## 📞 Support

### Getting Help
1. Check this README for common solutions
2. Verify your Python installation and version
3. Ensure all files are in the correct directory structure
4. Check file permissions in the `data/` directory

### System Requirements Verification
Run this command to check your system:
```bash
python -c "import sys, tkinter, json, sqlite3, datetime, dataclasses; print('All dependencies available!')"
```

## 📄 License

This project is developed for educational purposes as part of the TARUMT Software Assignment.

---

**Version**: 1.0  
**Last Updated**: 2025  
**Python Compatibility**: 3.8+  
**Platform**: Cross-platform (Windows, macOS, Linux)
