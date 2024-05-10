from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
from os import scandir
import shutil
from time import time, sleep
import sys    

    
if sys.platform.startswith("win"):
    username = os.getlogin()

    source_dir = os.path.join("C:\\Users", username, "Downloads")
    
    dest_dir = os.path.join("C:\\Users", username, "Desktop")
    
    dest_dir_images = os.path.join(dest_dir, "Images")
    
    dest_dir_pdfs = os.path.join(dest_dir, "PDFs")
    
    dest_dir_videos = os.path.join(dest_dir, "Videos")

    
if sys.platform.startswith("linux"):
    username = os.getenv("USER")

    source_dir = os.path.join("/home", username, "Downloads")
    
    dest_dir = os.path.join("/home", username, "Desktop")
    
    dest_dir_images = os.path.join(dest_dir, "Images")
    
    dest_dir_pdfs = os.path.join(dest_dir, "PDFs")
    
    dest_dir_videos = os.path.join(dest_dir, "Videos")


if sys.platform.startswith("darwin"):
    username = os.getenv("USER")
    source_dir = os.path.join("/Users", username, "Downloads")
    dest_dir = os.path.join("/Users", username, "Desktop")
    
    dest_dir_images = os.path.join(dest_dir, "Images")
    
    dest_dir_pdfs = os.path.join(dest_dir, "PDFs")
    
    dest_dir_videos = os.path.join(dest_dir, "Videos")


def move(source, dest, name):
    print(f"\nMoving {name} from {source} to {dest}\n")
    filename, extension = os.path.splitext(name)
    file_path = os.path.join(source, name)
    
    if not os.path.exists(dest):
        os.makedirs(dest)
    
    if os.path.exists(file_path):
        unique_name = f"{filename}_{int(time())}{extension}"
        shutil.move(file_path, os.path.join(dest, unique_name))
    else:
        print(f"File {file_path} does not exist")
    

class MoverHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print(f"\nFile {event.src_path} was modified")
        with scandir(source_dir) as entries:
            for entry in entries:
                name = entry.name

                if name.endswith(".png") or name.endswith(".jpg") or name.endswith(".jpeg"):
                    move(source_dir, dest_dir_images, name)
                    
                elif name.endswith(".pdf"):
                    move(source_dir, dest_dir_pdfs, name)
                    
                elif name.endswith(".mp4") or name.endswith(".avi") or name.endswith(".mov"):
                    move(source_dir, dest_dir_videos, name)
                    
                    
if __name__ == "__main__":
    path = source_dir
    event_handler = MoverHandler()
    
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    
    try:    
        print("Waiting for changes at " + path)
            
        while True:
            sleep(1)
            
    except KeyboardInterrupt:
        print("Stopping observer")
        observer.stop()
        
    observer.join()
    