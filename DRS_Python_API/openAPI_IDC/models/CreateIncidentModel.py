from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class ContactDetail(BaseModel):
    Contact_Type: str
    Contact: str
    Create_Dtm: datetime
    Create_By: str

class ProductDetail(BaseModel):
    Product_Label: str
    Customer_Ref: str
    Product_Seq: int
    Equipment_Ownership: str
    Product_Id: str
    Product_Name: str
    Product_Status: str
    Effective_Dtm: datetime
    Service_Address: str
    Cat: str
    Db_Cpe_Status: str
    Received_List_Cpe_Status: str
    Service_Type: str
    Region: Optional[str] = None
    Province: Optional[str] = None

class CustomerDetail(BaseModel):
    Customer_Name: str
    Company_Name: str
    Company_Registry_Number: str
    Full_Address: str
    Zip_Code: str
    Customer_Type_Name: str
    Nic: str
    Customer_Type_Id: str

class AccountDetail(BaseModel):
    Account_Status: str
    Acc_Effective_Dtm: datetime
    Acc_Activate_Date: datetime
    Credit_Class_Id: str
    Credit_Class_Name: str
    Billing_Centre: str
    Customer_Segment: str
    Mobile_Contact_Tel: str
    Daytime_Contact_Tel: str
    Email_Address: str
    Last_Rated_Dtm: datetime

class LastAction(BaseModel):
    Billed_Seq: int
    Billed_Created: datetime
    Payment_Seq: int
    Payment_Created: datetime

class MarketingDetail(BaseModel):
    ACCOUNT_MANAGER: str
    CONSUMER_MARKET: str
    Informed_To: str
    Informed_On: datetime

class Incident(BaseModel):
    Incident_Id: int
    Account_Num: str
    Arrears: float
    Created_By: str
    Created_Dtm: datetime
    Incident_Status: str
    Incident_Status_Dtm: datetime
    Status_Description: str
    File_Name_Dump: str
    Batch_Id: str
    Batch_Id_Tag_Dtm: datetime
    External_Data_Update_On: datetime
    Filtered_Reason: str
    Export_On: datetime
    File_Name_Rejected: str
    Rejected_Reason: str
    Incident_Forwarded_By: str
    Incident_Forwarded_On: datetime
    Contact_Details: List[ContactDetail]
    Product_Details: List[ProductDetail]
    Customer_Details: CustomerDetail
    Account_Details: AccountDetail
    Last_Actions: LastAction
    Marketing_Details: MarketingDetail
    Action: str
    Validity_period: int
    Remark: str
    updatedAt: datetime
    Rejected_By: str
    Rejected_Dtm: datetime
    Arrears_Band: str
    Source_Type: str
