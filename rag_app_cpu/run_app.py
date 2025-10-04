#!/usr/bin/env python3
import subprocess
import sys
import os

def main():
    """Simple script to run the Streamlit app."""
    try:
        # Change to the app directory
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        
        # Run streamlit
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"], check=True)
    except KeyboardInterrupt:
        print("\nApplication stopped by user.")
    except subprocess.CalledProcessError as e:
        print(f"Error running application: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()