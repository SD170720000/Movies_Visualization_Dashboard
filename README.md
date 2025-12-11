# Movies Dashboard

This project provides a dashboard for visualizing movie data using Flask.

## Setup & Execution

1. **Clone the repository**
   ```bash
   git clone https://github.com/SD170720000/Movies_Visualization_Dashboard.git
   cd Movies_Visualization_Dashboard
   ```

2. **Run the application**
   Use the provided `run.sh` script. You can specify a port (default is `5000`):
   ```bash
   run.sh [PORT]
   ```
   Example:
   ```bash
   run.sh 5001
   ```

   The script will:
   - Create a Python virtual environment
   - Activate the environment
   - Upgrade pip
   - Install dependencies from `requirements.txt`
   - Start the Flask app on the specified port

## Viewing the Dashboard

- Once started, open your browser and go to:
  ```
  http://127.0.0.1:<PORT>
  ```
  Replace `<PORT>` with the port you used (default is `5000`).

## Quitting / Stopping the App

- To stop the dashboard, press `Ctrl+C` in the terminal where the app is running.
- To deactivate the virtual environment:
  ```bash
  deactivate
  ```

## Notes

- Ensure you have Python 3 installed.
- If you encounter permission issues, you may need to make the script executable:
  ```bash
  chmod +x run.sh
  ```

## Troubleshooting

- If you see errors during setup, check that all dependencies in `requirements.txt` are compatible with your Python version.
- For port conflicts, choose a different port when running the script.

---
