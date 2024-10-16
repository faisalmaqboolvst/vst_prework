import os
from django.test import TestCase, Client
from django.conf import settings

from api.models import filedata_collection


class FileDataAPITest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # MongoDB connection is already configured globally, so no need to reconfigure here
        cls.client_django = Client()

    def test_add_data(self):
        """Test the add_data API by uploading a .docx file."""
        print(settings.MEDIA_ROOT)
        test_file_path = os.path.join(
            settings.MEDIA_ROOT, "uploaded_docs", os.getenv("TEST_MEDIA_FILE")
        )
        print(test_file_path)
        with open(test_file_path, "rb") as test_file:
            response = self.client_django.post(
                "/api/read_file/",  # Replace with your API endpoint
                {
                    "doc_file": test_file,
                    "first_name": "Test",
                },
            )
        # Check if the response status is 200 OK
        self.assertEqual(response.status_code, 200)

        # Check if data was added to the MongoDB collection
        inserted_record = filedata_collection.find_one({"first_name": "Test"})
        self.assertIsNotNone(inserted_record)

    def test_get_all_data(self):
        """Test the get_all_data API."""
        # Insert a sample document into the MongoDB test collection
        filedata_collection.insert_one(
            {
                "first_name": "Jane",
                "file_path": "/media/uploaded_docs/test.docx",
                "extracted_text": "Sample text from docx",
                "ocr_texts": ["Sample OCR text"],
            }
        )

        # Call the API to get all data
        response = self.client_django.get("/api/get/")  # Replace with your API endpoint

        # Check if the response status is 200 OK
        self.assertEqual(response.status_code, 200)

        # Verify the response data
        data = response.json()
        self.assertTrue(len(data) > 0)
        self.assertIn("first_name", data[0])

    # @classmethod
    # def tearDownClass(cls):
    #     # Clean up the collection after tests
    #     filedata_collection.delete_many({})  # Remove all test data
