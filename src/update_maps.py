from datetime import date
import json
import requests

MAPS_FILE_ORIGINAL = "data/maps.json"
MAPS_FILE_ARCHIVE = "data/archivedqueens.json"

class MapData:
    def __init__(self, is_archive):

        
        if is_archive:
            print("Loading ARCHIVE dataset")
            self.data = self.check_archive_update()
        else:
            print("Loading ORIGINAL dataset")
            self.data = self.get_original_data()
            
      
    def get_original_data(self):
        try:
            with open(MAPS_FILE_ORIGINAL, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"The file {MAPS_FILE_ORIGINAL} was not found.")
        except json.JSONDecodeError:
            raise ValueError("Error decoding the JSON file.")     
        
        return data
        
    def check_archive_update(self):
        with open(MAPS_FILE_ARCHIVE, 'r') as archive_file:
            current_data = json.load(archive_file)
            
        year, month, day = map(int, current_data[0]['date'].split("/")) 

        latest_date = date(year, month, day)
        
        current_date = date.today()
        
        if latest_date < current_date and self.update_archive():
          
            
            
            with open(MAPS_FILE_ARCHIVE, 'r') as archive_file:
                updated_data = json.load(archive_file)
                
            print("New maps! Loaded updated data")
            return updated_data
        
        else:
            print("Nothing new! Loading current data")
            return current_data
        
            
    
    
    def update_archive(self):
        try:
            req = requests.get("https://queensstorage.blob.core.windows.net/puzzles/linkedinPuzzles.json")
            
            data = req.json()
            
            
            
        
            formatted_dict = {entry['id']: entry for entry in data}
            
            formatted_dict[177]['regions'][6][7] = 9
            formatted_dict[177]['regions'][6][8] = 9
            formatted_dict[177]['regions'][7][7] = 9
            formatted_dict[177]['regions'][7][8] = 9
            
            
            with open(MAPS_FILE_ARCHIVE, 'w') as file:
                json.dump(list(formatted_dict.values()), file, indent=4)
                file.close()
                
            print("ARCHIVE UPDATED")
        except requests.exceptions.RequestException as e:
            # Issues with the GET request
            print(f"Request failed: {e}")
            return False

        except FileNotFoundError as e:
            # File path doesn't exist
            print(f"File not found: {e}")
            return False

        except Exception as e:
            # General exception handler 
            print(f"An unexpected error occurred: {e}")
            return False
        
        return True
    
