import os
import subprocess
import webbrowser

print("Building index...")
subprocess.run(["python", "indexer/build_index.py"])

print("\nStarting Flask web server...")
webbrowser.open("http://127.0.0.1:5000/")

subprocess.run(["python", "web/app.py"])
