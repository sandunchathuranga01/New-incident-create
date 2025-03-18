from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from datetime import datetime
from typing import Dict
from openAPI_IDC.models.CreateIncidentModel import Incident
from openAPI_IDC.services.CreateIncidentService import create_incident, update_incident
from utils.logger.loggers import get_logger

# Get the logger
logger_INC1A01 = get_logger('INC1A01')
logger_INC1P02 = get_logger('INC1P02')

router = APIRouter()

# Pydantic Models for Responses
class IncidentResponse(BaseModel):
    Incident_Id: str
    message: str

class ErrorResponse(BaseModel):
    detail: str

@router.post(
    "/Request_Incident_External_information",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new incident",
    description="""
    Create Incident API 
    
    Endpoint:POST /Request_Incident_External_information

    This API allows creating a new incident record.

    🔹 Key Features:
    - Validates the incoming JSON data using the `RequestIncidentExternalinformationModel` model.
    - Inserts the validated data into the database.
    - Logs the time taken to process the request.

    📌 Responses:
    - ✔️ 201 Created: Incident created successfully.
    - ❌ 500 Internal Server Error: If something goes wrong.

    📝 Example Request Body:
    json
        {
          "Incident_Id": 16,
          "Account_Num": "ACC12345",
          "Arrears": 15000.75,
          "Created_By": "User123",
          "Created_Dtm": "2024-12-01 10:00:00",
          "Incident_Status": "Open No Agent",
          "Incident_Status_Dtm": "2024-12-01 10:05:00",
          "Status_Description": "Pending review",
          "File_Name_Dump": "incident_file_1.txt",
          "Batch_Id": "01",
          "Batch_Id_Tag_Dtm": "2024-12-01 11:00:00",
          "External_Data_Update_On": "2024-12-02 08:00:00",
          "Filtered_Reason": "Duplicate data",
          "Export_On": "2024-12-03 10:00:00",
          "File_Name_Rejected": "rejected_file_1.txt",
          "Rejected_Reason": "Invalid data provided",
          "Incident_Forwarded_By": "Admin123",
          "Incident_Forwarded_On": "2024-12-03 12:00:00",
          "Contact_Details": [
            {
              "Contact_Type": "Land",
              "Contact": "0111234567",
              "Create_Dtm": "2024-12-01 09:10:00",
              "Create_By": "User123"
            }
          ],
          "Product_Details": [
            {
              "Product_Label": "ProductA",
              "Customer_Ref": "CUST001",
              "Product_Seq": 1,
              "Equipment_Ownership": "Owned",
              "Product_Id": "PROD001",
              "Product_Name": "WidgetX",
              "Product_Status": "OK",
              "Effective_Dtm": "2024-11-01 00:00:00",
              "Service_Address": "123 Street Name, City",
              "Cat": "Category1",
              "Db_Cpe_Status": "Online",
              "Received_List_Cpe_Status": "Delivered",
              "Service_Type": "Standard",
              "Region": "",
              "Province": ""
            }
          ],
          "Customer_Details": {
            "Customer_Name": "John Doe",
            "Company_Name": "Doe Inc.",
            "Company_Registry_Number": "REG12345",
            "Full_Address": "456 Business St, City, Country",
            "Zip_Code": "12345",
            "Customer_Type_Name": "Corporate",
            "Nic": "123456789V",
            "Customer_Type_Id": "CORP"
          },
          "Account_Details": {
            "Account_Status": "Active",
            "Acc_Effective_Dtm": "2024-01-01 00:00:00",
            "Acc_Activate_Date": "2024-01-02 00:00:00",
            "Credit_Class_Id": "CLASS01",
            "Credit_Class_Name": "Premium",
            "Billing_Centre": "Centre1",
            "Customer_Segment": "SegmentA",
            "Mobile_Contact_Tel": "9876543210",
            "Daytime_Contact_Tel": "1234567890",
            "Email_Address": "john.doe@example.com",
            "Last_Rated_Dtm": "2024-11-30 18:00:00"
          },
          "Last_Actions": {
            "Billed_Seq": 1001,
            "Billed_Created": "2024-12-01 12:00:00",
            "Payment_Seq": 2002,
            "Payment_Created": "2024-12-02 09:30:00"
          },
          "Marketing_Details": {
            "ACCOUNT_MANAGER": "Jane Smith",
            "CONSUMER_MARKET": "Retail",
            "Informed_To": "MarketingDept@example.com",
            "Informed_On": "2024-12-02 10:30:00"
          },
          "Action": "aaa",
          "Validity_period": 6,
          "Remark":"abcdefgh"
          ],
          "updatedAt":"2025-01-14T09:38:37.843Z",
          "Rejected_By": "Admin123",
          "Rejected_Dtm":"2025-01-14T09:38:37.833Z",
          "Arrears_Band": "AB-10_25",
          "Source_Type": "Product Terminate"
        }
    """,
    response_model=IncidentResponse,
    responses={
        201: {"description": "Incident created successfully", "model": IncidentResponse},
        500: {"description": "Internal Server Error", "model": ErrorResponse}
    }
)
async def create_incident_endpoint(incident: Incident):
    try:
        logger_INC1A01.info("Starting the incident creation process.")
        API_Start_time = datetime.now()

        incident_id = create_incident(incident)
        logger_INC1A01.info(f"Incident created successfully (id: {incident_id})")

        API_End_time = datetime.now()
        processing_time = (API_End_time - API_Start_time).total_seconds()
        logger_INC1A01.info(f"Processing Duration: {processing_time:.6f} seconds")

        return {"Incident_Id": incident_id, "message": "Incident created successfully"}

    except Exception as e:
        logger_INC1A01.error(f"Error creating incident: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create incident",
        )

@router.put(
    "/Request_Incident_External_information",
    summary="Update an existing incident",
    description="""
    Update Incident API

    Endpoint: `PUT /Request_Incident_External_information`

    This API allows updating an existing incident record.

    🔹 Key Features:
    - Validates the incoming JSON data using the `RequestIncidentExternalinformationModel` model.
    - Updates the existing incident in the database.
    - Logs the time taken to process the request.

    📌 Responses:
    - ✔️ 200 OK: Incident updated successfully.
    - ⚠️ 400 Bad Request: Missing `Incident_Id`.
    - ❌ 404 Not Found: Incident does not exist.
    - ❌ 500 Internal Server Error: If something goes wrong.

    📝 Example Request Body:
    json
        {
          "Incident_Id": 16,
          "Account_Num": "ACC12345",
          "Arrears": 15000.75,
          "Created_By": "User123",
          "Created_Dtm": "2024-12-01 10:00:00",
          "Incident_Status": "Open No Agent",
          "Incident_Status_Dtm": "2024-12-01 10:05:00",
          "Status_Description": "Pending review",
          "File_Name_Dump": "incident_file_1.txt",
          "Batch_Id": "01",
          "Batch_Id_Tag_Dtm": "2024-12-01 11:00:00",
          "External_Data_Update_On": "2024-12-02 08:00:00",
          "Filtered_Reason": "Duplicate data",
          "Export_On": "2024-12-03 10:00:00",
          "File_Name_Rejected": "rejected_file_1.txt",
          "Rejected_Reason": "Invalid data provided",
          "Incident_Forwarded_By": "Admin123",
          "Incident_Forwarded_On": "2024-12-03 12:00:00",
          "Contact_Details": [
            {
              "Contact_Type": "Land",
              "Contact": "0111234567",
              "Create_Dtm": "2024-12-01 09:10:00",
              "Create_By": "User123"
            }
          ],
          "Product_Details": [
            {
              "Product_Label": "ProductA",
              "Customer_Ref": "CUST001",
              "Product_Seq": 1,
              "Equipment_Ownership": "Owned",
              "Product_Id": "PROD001",
              "Product_Name": "WidgetX",
              "Product_Status": "OK",
              "Effective_Dtm": "2024-11-01 00:00:00",
              "Service_Address": "123 Street Name, City",
              "Cat": "Category1",
              "Db_Cpe_Status": "Online",
              "Received_List_Cpe_Status": "Delivered",
              "Service_Type": "Standard",
              "Region": "",
              "Province": ""
            }
          ],
          "Customer_Details": {
            "Customer_Name": "John Doe",
            "Company_Name": "Doe Inc.",
            "Company_Registry_Number": "REG12345",
            "Full_Address": "456 Business St, City, Country",
            "Zip_Code": "12345",
            "Customer_Type_Name": "Corporate",
            "Nic": "123456789V",
            "Customer_Type_Id": "CORP"
          },
          "Account_Details": {
            "Account_Status": "Active",
            "Acc_Effective_Dtm": "2024-01-01 00:00:00",
            "Acc_Activate_Date": "2024-01-02 00:00:00",
            "Credit_Class_Id": "CLASS01",
            "Credit_Class_Name": "Premium",
            "Billing_Centre": "Centre1",
            "Customer_Segment": "SegmentA",
            "Mobile_Contact_Tel": "9876543210",
            "Daytime_Contact_Tel": "1234567890",
            "Email_Address": "john.doe@example.com",
            "Last_Rated_Dtm": "2024-11-30 18:00:00"
          },
          "Last_Actions": {
            "Billed_Seq": 1001,
            "Billed_Created": "2024-12-01 12:00:00",
            "Payment_Seq": 2002,
            "Payment_Created": "2024-12-02 09:30:00"
          },
          "Marketing_Details": {
            "ACCOUNT_MANAGER": "Jane Smith",
            "CONSUMER_MARKET": "Retail",
            "Informed_To": "MarketingDept@example.com",
            "Informed_On": "2024-12-02 10:30:00"
          },
          "Action": "aaa",
          "Validity_period": 6,
          "Remark":"abcdefgh"
          ],
          "updatedAt":"2025-01-14T09:38:37.843Z",
          "Rejected_By": "Admin123",
          "Rejected_Dtm":"2025-01-14T09:38:37.833Z",
          "Arrears_Band": "AB-10_25",
          "Source_Type": "Product Terminate"
        }
    """,
    response_model=Dict[str, str],
    responses={
        200: {"description": "Incident updated successfully", "model": Dict[str, str]},
        400: {"description": "Bad Request - Missing Incident ID", "model": ErrorResponse},
        404: {"description": "Incident not found", "model": ErrorResponse},
        500: {"description": "Internal Server Error", "model": ErrorResponse}
    }
)
async def update_incident_endpoint(incident_data: dict):
    try:
        incident_id = incident_data.get("Incident_Id")

        if not incident_id:
            logger_INC1P02.error("Incident_Id is required in the request body")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incident_Id is required in the request body",
            )

        logger_INC1P02.info(f"Starting update for Incident ID: {incident_id}")
        API_Start_time = datetime.now()

        # Ensure Incident model can handle dictionary input
        incident = Incident(**incident_data)

        if not update_incident(incident_id, incident):
            logger_INC1P02.error(f"Incident ID {incident_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Incident not found",
            )

        API_End_time = datetime.now()
        processing_time = (API_End_time - API_Start_time).total_seconds()
        logger_INC1P02.info(f"Processing Duration: {processing_time:.6f} seconds")

        return {"message": "Incident updated successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        logger_INC1P02.error(f"Error updating incident: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update incident",
        )
