from datetime import datetime
from ActionController.config_manager import initialize_hash_maps
from openAPI_IDC.models.CreateIncidentModel import Incident
from utils.database.connectDB import get_db_connection

initialize_hash_maps()

# Initialize MongoDB connection
try:

    # Get database connection
    db = get_db_connection()

    if db is False:
        raise Exception("Database connection failed")

    # Get the actual collection
    collection = db["incidents"]

    # Ensure index on Incident_Id
    collection.create_index("Incident_Id", unique=True)

except Exception as e:
    print(f"Error initializing database: {e}")
    collection = None  # Prevent further errors

def create_incident(incident: Incident):
    try:
        if collection is None:
            raise Exception("Database not initialized properly")

        incident_dict = incident.dict()
        incident_dict['updatedAt'] = datetime.now()
        result = collection.insert_one(incident_dict)
        return str(result.inserted_id)  # Convert ObjectId to string

    except Exception as e:
        print(f"Error inserting incident {e}")
        return "-1"

def update_incident(incident_id: int, incident: Incident):
    if collection is None:
        raise Exception("Database not initialized properly")

    existing = collection.find_one({"Incident_Id": incident_id})
    if not existing:
        return False  # Incident does not exist

    incident_dict = incident.dict()
    incident_dict['updatedAt'] = datetime.now()

    result = collection.update_one({"Incident_Id": incident_id}, {"$set": incident_dict})
    return result.modified_count > 0


