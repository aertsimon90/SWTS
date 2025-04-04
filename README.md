# Shield Web Terminal System (SWTS)

Welcome to **Shield Web Terminal System (SWTS)**, a lightweight and customizable web-based terminal originally designed for the ShieldSSP team. Now, it has been released as an open-source project for everyone to use, modify, and enjoy!

## Overview
SWTS is a simple yet powerful web terminal built with Flask, offering an intuitive interface and flexible functionality. Whether you want to log user activity, store data, or process commands in your own way, SWTS provides the foundation to make it happen. It’s designed to be easy to set up and adapt to your needs.

- **Simple Setup**: Just grab the `web_terminal.py` file and run it—that’s it!
- **User Tracking**: Enable logging with a single switch (`logs = True`) to capture client information.
- **Data Persistence**: Use the `database` variable to save and load data effortlessly.
- **Customizable Commands**: Process incoming commands however you like by tweaking the `terminal_run` function.
- **Unique Encryption**: SWTS features a custom encryption method designed by Simon Scap. While slower than standard algorithms, it offers a robust starting point by dynamically encrypting data based on the input and key, making it impossible to decrypt without the correct key.

## Features
- **Ease of Use**: Minimal setup, maximum flexibility.
- **Dynamic Encryption**: A bespoke encryption system that evolves with the data it processes, crafted for strength and originality.
- **Open Source**: Free to use, modify, and contribute to—built for the community.

## Getting Started
Using SWTS is as simple as it gets:
1. Find and download the `web_terminal.py` file.
2. Install Flask: `pip install flask`.
3. Run the script: `python web_terminal.py`.
4. Open your browser and navigate to `http://localhost:5000`.

That’s it! You’re now running your own web terminal.

## Customization
SWTS is designed to let you process commands however you want. Modify the `terminal_run` function to define your own logic. Here’s an example:

```python
def terminal_run(command, client):
    if command == "hello":
        return f"Hello from {client['remote_addr']}!"
    return f"Command received: {command}"
```

Want to log client activity? Just set `logs = True`. Need persistent data? Use the `database` variable to store and retrieve information.

## Encryption
SWTS includes a custom encryption system by Simon Scap. Unlike static methods, it adapts to the input and key, using traces of previously processed data to strengthen the encryption. While it may be slower, it provides a unique and solid foundation. Check out the `encrypt` and `decrypt` functions in `web_terminal.py` for details.

## Contributing
We welcome contributions! Whether it’s improving the UI, adding new features, or enhancing the encryption, feel free to fork the repository, make your changes, and submit a pull request.

## License
This project is open-source and available under the [MIT License](LICENSE).
