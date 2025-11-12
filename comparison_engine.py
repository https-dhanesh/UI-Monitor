class ComparisonEngine:
    def compare_snapshots(self, old_snap, new_snap):
        changes = []
        
        old_elements = old_snap["elements"]
        new_elements = new_snap["elements"]
        all_keys = set(old_elements.keys()) | set(new_elements.keys())
        
        for key in all_keys:
            old_data = old_elements.get(key)
            new_data = new_elements.get(key)
            
            if old_data and not new_data:
                changes.append({
                    "element": key,
                    "type": "REMOVED",
                    "details": "Element no longer exists"
                })
            elif not old_data and new_data:
                changes.append({
                    "element": key,
                    "type": "ADDED", 
                    "details": "New element found"
                })
            elif old_data and new_data:
                element_changes = self._compare_element_data(key, old_data, new_data)
                changes.extend(element_changes)
        
        return changes
    
    def _compare_element_data(self, element_name, old_data, new_data):
        changes = []

        if old_data.get("text") != new_data.get("text"):
            changes.append({
                "element": element_name,
                "type": "TEXT_CHANGE",
                "old_value": old_data.get("text"),
                "new_value": new_data.get("text")
            })

        if old_data.get("is_displayed") != new_data.get("is_displayed"):
            changes.append({
                "element": element_name,
                "type": "VISIBILITY_CHANGE",
                "old_value": "visible" if old_data.get("is_displayed") else "hidden",
                "new_value": "visible" if new_data.get("is_displayed") else "hidden"
            })
        
        return changes