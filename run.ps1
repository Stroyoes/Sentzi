# Define the path to your requirements.txt file and the Python executable
$requirementsFile = "requirements.txt"
$pythonExec = "sentzi-venv\Scripts\python.exe"

# activate venv
$venvPath = ".\sentzi-venv\Scripts\Activate.ps1"

# Check if the Activate.ps1 script exists
if (Test-Path $venvPath) {
    # Activate the virtual environment
    . $venvPath
    Write-Host "Virtual environment activated."
} else {
    Write-Host "Virtual environment script not found."
}

# Check if Python is installed
if (Test-Path $pythonExec) {
    # Run the Streamlit application
    Write-Host "Running Streamlit application..."
    & $pythonExec -m streamlit run app.py
} else {
Write-Host "Python is not installed. Please install Python and try again."
}
