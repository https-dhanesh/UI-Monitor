import json
import os
from datetime import datetime

class SnapshotManager:
    def __init__(self, snapshots_dir="snapshots"):
        self.snapshots_dir = snapshots_dir
        os.makedirs(snapshots_dir, exist_ok=True)
    
    def save_snapshot(self, url, elements_data, page_info):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"snapshot_{timestamp}.json"
        filepath = os.path.join(self.snapshots_dir, filename)
        
        snapshot_data = {
            "metadata": {
                "url": url,
                "timestamp": timestamp,
                "title": page_info["title"],
                "page_source_length": page_info["page_source_length"]
            },
            "elements": elements_data
        }
        
        with open(filepath, 'w') as f:
            json.dump(snapshot_data, f, indent=2)
        
        print(f"Snapshot saved: {filename}")
        return filename
    
    def load_snapshot(self, filename):
        filepath = os.path.join(self.snapshots_dir, filename)
        
        with open(filepath, 'r') as f:
            return json.load(f)
    
    def list_snapshots(self):
        files = [f for f in os.listdir(self.snapshots_dir) if f.endswith('.json')]
        return sorted(files, reverse=True)