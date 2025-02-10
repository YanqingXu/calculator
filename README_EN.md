# Calculator with Custom Background

[中文](README.md) | English

A modern calculator application built with Python and PySide2, featuring a customizable background image system. This elegant and user-friendly calculator combines essential mathematical operations with a personalized visual experience.

## Features

- Basic arithmetic operations (addition, subtraction, multiplication, division)
- Decimal point calculations
- Customizable background images
- Calculation history tracking
- Keyboard shortcuts support
- Modern and intuitive UI

## Tech Stack

- Python 3.x
- PySide2 5.15.2.1 (Qt framework)
- Pillow 9.5.0 (Image processing)
- PyInstaller 5.13.2 (Packaging tool)

## Project Structure

```
calculator/
├── main.py              # Main program entry
├── modules/             # Modules directory
│   ├── calculator_ui.py     # UI implementation
│   ├── calculator_core.py   # Core calculator logic
│   ├── background_manager.py# Background manager
│   ├── history_manager.py   # History manager
│   ├── keyboard_handler.py  # Keyboard event handler
│   └── base_widget.py       # Base components
├── requirements.txt     # Project dependencies
└── background_config.json # Background configuration
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/YanqingXu/calculator.git
cd calculator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

## Usage

- Basic calculations: Click number and operation buttons
- Keyboard input: Use keyboard for numbers and operations
- Background customization: Click settings to choose a custom background
- History: View previous calculations

## Building Executable

Build the application using PyInstaller:
```bash
pyinstaller build.py
```

## Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
