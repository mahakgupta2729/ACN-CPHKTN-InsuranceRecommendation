import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient

def extract_text_from_pdf(file):
    try:
        endpoint = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT")
        key = os.getenv("AZURE_FORM_RECOGNIZER_KEY")

        form_recognizer_client = DocumentAnalysisClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(key)
        )

        # file is a FileStorage object, which has a `.stream` attribute (a file-like object)
        poller = form_recognizer_client.begin_analyze_document(
            model_id="prebuilt-document",
            document=file.stream  # this is correct
        )

        result = poller.result()

        extracted_text = ""
        for page in result.pages:
            for line in page.lines:
                extracted_text += line.content + "\n"

        return extracted_text

    except Exception as e:
        print(f"❌ Failed to extract text: {e}")
        return ""
