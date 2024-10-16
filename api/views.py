import os
from django.views.decorators.csrf import csrf_exempt


from django.conf import settings
from .models import filedata_collection
from django.http import HttpResponse, JsonResponse

from .utils.utils import extract_text, extract_images, perform_ocr, serialize_data

from django.http import HttpResponse


def index(request):
    """
    A simple view function that returns a greeting message.
    """
    # Return a simple HTTP response with a greeting message
    return HttpResponse("Hello, world. You're at the polls index.")


def add_data(request):
    """
    A view function that adds a new record to the MongoDB collection.

    """
    # Create a dictionary to represent the new record to be added
    record = {"first_name": "John", "last_name": "Doe"}

    # Insert the new record into the MongoDB collection
    filedata_collection.insert_one(record)

    # Return an HTTP response confirming that the record has been added
    return HttpResponse("New record added")


@csrf_exempt
def read_file(request):
    """
    View function to handle file upload and data extraction from a .docx file.
    Note: if you are in project then you need to remove csrf_exempt decorator

    Args:
        request: The HTTP request object that contains the uploaded file and other form data.

    Returns:
        HttpResponse: A response indicating the success or failure of the file upload and data extraction.
    """
    # Check if the request method is POST and if a file has been uploaded
    if request.method == "POST" and request.FILES.get("doc_file"):
        doc_file = request.FILES["doc_file"]  # Get the uploaded file from the request

        # Save the file to the media folder
        media_folder = os.path.join(
            settings.MEDIA_ROOT, "uploaded_docs"
        )  # Define the path for saving files
        os.makedirs(
            media_folder, exist_ok=True
        )  # Create the media folder if it doesn't exist
        file_path = os.path.join(
            media_folder, doc_file.name
        )  # Define the full file path

        # Save the uploaded file in chunks to handle large files efficiently
        with open(file_path, "wb+") as destination:
            for chunk in doc_file.chunks():  # Write the file in chunks
                destination.write(chunk)

        # Extract text and images from the saved .docx file
        extracted_text = extract_text(file_path)  # Extract text from the document
        images = extract_images(file_path)  # Extract images from the document
        ocr_texts = perform_ocr(images)  # Perform OCR on the extracted images

        # Save the file path and extracted data in the database
        record = {
            "first_name": request.POST.get(
                "first_name"
            ),  # Get the first name from the form data
            "file_path": file_path,
            "extracted_text": extracted_text,
            "ocr_texts": ocr_texts,
        }
        filedata_collection.insert_one(
            record
        )  # Insert the record into the MongoDB collection

        # Return a success response with the added record information
        return HttpResponse(f"File uploaded and data extracted. Record added: {record}")

    # Return an error response if no file was uploaded
    return HttpResponse(
        "No file uploaded", status=400
    )  # Return a 400 Bad Request response


def get_all_data(request):
    """
    View function to retrieve all records from the MongoDB collection.

    """
    # Fetch data from the collection and convert the cursor to a list
    data = list(filedata_collection.find())  # Querying the database to get all records

    # Serialize the data (convert ObjectId to string)
    serialized_data = serialize_data(
        data
    )  # Serializing the data for JSON compatibility

    # Return the data as a JSON response
    return JsonResponse(
        serialized_data, safe=False
    )  # Returning the serialized data as a JSON response
