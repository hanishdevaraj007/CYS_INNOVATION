import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import sys
PATH_TO_MONITOR = os.path.abspath("/home/kali/cys_proj/monitor_target") 

LOG_FILE = os.path.join(os.path.abspath("/home/kali/cys_proj"), "monitor_events.log")

def log_event(message):
    timestamp = time.ctime()
    log_entry = f"[{timestamp}] {message}"
    
    print(log_entry) 
    
    try:
        with open(LOG_FILE, 'a') as f:
            f.write(log_entry + "\n")
    except Exception as e:
        print(f"CRITICAL LOGGING ERROR: {e}", file=sys.stderr)


class RansomwareDetector(FileSystemEventHandler):
    
    def on_created(self, event):
        if not event.is_directory:
            log_event(f"ALERT: File CREATED! -> {event.src_path}")
    
    def on_moved(self, event):
        if not event.is_directory:
            log_event(f"ALERT: File MOVED/RENAMED (Potential Encryption): {event.src_path} -> {event.dest_path}")
            
    def on_modified(self, event):
        if not event.is_directory:
            log_event(f"EVENT: File MODIFIED! -> {event.src_path}")
            
    def on_deleted(self, event):
        if not event.is_directory:
            log_event(f"EVENT: File DELETED! -> {event.src_path}")

if __name__ == "__main__":
    if not os.path.exists(PATH_TO_MONITOR):
        os.makedirs(PATH_TO_MONITOR)
        
    event_handler = RansomwareDetector()
    observer = Observer()
    observer.schedule(event_handler, PATH_TO_MONITOR, recursive=True)
    observer.start()

    log_event(f"\n[*] STARTING MONITOR. Watching: {PATH_TO_MONITOR}")
    log_event(f"[*] Logging events to {LOG_FILE}. Press Ctrl+C to stop.")

    try:
        while True:
            time.sleep(1) 
    except KeyboardInterrupt:
        observer.stop()
    
    observer.join()
    log_event("[*] Monitor stopped.")
