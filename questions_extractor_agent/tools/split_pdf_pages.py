"""
Tool for splitting PDF pages into JPEG images.
"""

import os
from pathlib import Path
from typing import Dict, Union

import PyPDF2
from google.adk.tools import ToolContext
from pdf2image import convert_from_path


def split_pdf_pages(
    file_path: str, tool_context: ToolContext
) -> Dict[str, Union[str, Dict[str, str]]]:
    """
    Splits a PDF file into individual JPEG images, one per page.

    Args:
        file_path (str): Path to the PDF file to split.
        tool_context (ToolContext): ADK ToolContext for storing the file information.

    Returns:
        Dict[str, Union[str, Dict[str, str]]]: A dictionary containing:
            - status: "success" or "error"
            - message: A string describing the success or error
            - files: A dictionary of the generated JPEG files (filename as key, "" as value)
    """
    pdf_path = Path(file_path)

    # Check if file exists
    if not pdf_path.exists():
        return {
            "status": "error",
            "message": f"File '{file_path}' does not exist",
            "files": {},
        }

    # Check if file is a PDF
    if pdf_path.suffix.lower() != ".pdf":
        return {
            "status": "error",
            "message": f"File '{file_path}' is not a PDF",
            "files": {},
        }

    generated_files = {}
    try:
        # Open the PDF using PyPDF2
        pdf_reader = PyPDF2.PdfReader(file_path)
        num_pages = len(pdf_reader.pages)

        if num_pages == 0:
            return {
                "status": "error",
                "message": f"PDF file '{file_path}' has no pages",
                "files": {},
            }

        # Extract the filename without extension
        file_name_without_ext = pdf_path.stem
        
        # Convert PDF pages to images using pdf2image
        images = convert_from_path(file_path)
        
        # Initialize files dict in tool_context if it doesn't exist
        if "files" not in tool_context.state:
            tool_context.state["files"] = {}
        
        # Save each page as a JPEG image
        for i, image in enumerate(images):
            # Create output filename with format: {original_filename_without_ext}-{page_number}.jpg
            output_filename = f"{file_name_without_ext}-{i+1}.jpg"
            output_path = pdf_path.parent / output_filename
            
            # Save the image as JPEG
            image.save(str(output_path), "JPEG")
            
            # Store the absolute path in the generated_files dictionary
            absolute_path = str(output_path.absolute())
            generated_files[absolute_path] = ""
            
            # Store the file in the tool_context.state
            tool_context.state["files"][absolute_path] = ""
            
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error processing PDF file '{file_path}': {str(e)}",
            "files": {},
        }

    # Return the result
    return {
        "status": "success",
        "message": f"Successfully split PDF '{file_path}' into {len(generated_files)} JPEG images",
        "files": generated_files,
    }