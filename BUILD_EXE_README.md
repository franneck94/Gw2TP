# Building GW2TP Backend as Executable

This guide explains how to build your GW2TP backend as a standalone executable (.exe) that can be distributed to users without requiring Python installation.

## Prerequisites

1. Python 3.10 or higher installed on your system
2. All project dependencies available

## Building the Executable

### Option 1: Using the Build Script (Recommended)

1. Open Command Prompt or PowerShell in the project root directory
2. Run the build script:
   ```cmd
   build-exe.bat
   ```

This script will:
- Create a virtual environment if it doesn't exist
- Install all required dependencies including PyInstaller
- Clean previous builds
- Build the executable using PyInstaller
- Show build results

### Option 2: Manual Build

If you prefer to build manually:

1. Install PyInstaller and dependencies:
   ```cmd
   pip install -r requirements-exe.txt
   ```

2. Build the executable:
   ```cmd
   pyinstaller backend.spec
   ```

## Output

The executable will be created in the `dist` folder as `gw2tp-backend.exe`.

## Distribution

To distribute your application to users:

1. Copy the entire contents of the `dist` folder
2. Include any additional files users might need:
   - Database files (if using local database)
   - Configuration files
   - Any static assets not included in the build

## Running the Executable

Users can run the backend by:
1. Double-clicking `gw2tp-backend.exe`
2. Or running it from command line: `gw2tp-backend.exe`

The backend will start on `http://localhost:8000` by default.

## Important Notes

### Database Considerations
- If your application uses a local database (SQLite), make sure the database files are included with the distribution
- For MongoDB or other external databases, ensure users have access to the database server
- Update any database connection strings to work with the executable environment

### Firewall and Network
- Users may need to allow the executable through their firewall
- The application will listen on port 8000 by default

### Configuration
- Consider adding a configuration file that users can modify for their environment
- Environment variables might work differently in the executable vs. development environment

### Troubleshooting

If the build fails:
1. Check that all dependencies are properly installed
2. Ensure no files are in use during the build process
3. Check the PyInstaller output for specific error messages
4. You may need to add additional hidden imports to the `backend.spec` file

### Performance Notes
- The executable may take longer to start than running with Python directly
- The executable file will be larger as it includes the Python runtime and all dependencies
- Consider using UPX compression (enabled in the spec file) to reduce file size

### Testing
Before distributing:
1. Test the executable on a clean system without Python installed
2. Verify all API endpoints work correctly
3. Test with your typical data and usage patterns
