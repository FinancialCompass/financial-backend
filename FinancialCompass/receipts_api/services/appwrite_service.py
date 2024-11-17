from appwrite.client import Client
from appwrite.services.databases import Databases
from django.conf import settings

class AppwriteService:
    def __init__(self):
        self.client = Client()
        self.client.set_endpoint(settings.APPWRITE_ENDPOINT)
        self.client.set_project(settings.APPWRITE_PROJECT_ID)
        self.client.set_key(settings.APPWRITE_API_KEY)
        
        self.database = Databases(self.client)
        
    def create_transaction(self, user_id, receipt_data, ipfs_hash):
        try:
            # Create document in Appwrite transactions collection
            transaction = self.database.create_document(
                database_id=settings.APPWRITE_DATABASE_ID,
                collection_id=settings.APPWRITE_COLLECTION_ID,
                document_id='unique()',
                data={
                    'user_id': user_id,
                    'ipfs_hash': ipfs_hash,
                    'store_name': receipt_data.get('store_name'),
                    'total_amount': receipt_data.get('total'),
                    'date': receipt_data.get('date'),
                    'items': receipt_data.get('items', [])
                }
            )
            return transaction
        except Exception as e:
            raise Exception(f"Appwrite Error: {str(e)}") 