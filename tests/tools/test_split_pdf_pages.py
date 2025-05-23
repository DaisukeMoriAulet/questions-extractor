"""
Tests for the split_pdf_pages tool.
"""

import os
import tempfile
from pathlib import Path
from typing import Any, Dict

import PyPDF2
import pytest
from PIL import Image
from PyPDF2 import PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from questions_extractor_agent.tools.split_pdf_pages import split_pdf_pages


class MockToolContext:
    """
    Mock implementation of ToolContext for testing.
    """

    def __init__(self):
        self.state: Dict[str, Any] = {}


def create_test_pdf(file_path, num_pages=1):
    """
    Creates a test PDF file with the specified number of pages.

    Args:
        file_path (str): Path where the PDF should be created
        num_pages (int): Number of pages to create in the PDF
    """
    pdf_writer = PdfWriter()

    for i in range(num_pages):
        # Create a temporary PDF page
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
            temp_path = temp_file.name

        # Generate a simple PDF page with some text
        c = canvas.Canvas(temp_path, pagesize=letter)
        c.drawString(100, 700, f"Test PDF - Page {i+1}")
        c.save()

        # Add the page to the PDF writer
        pdf_reader = PyPDF2.PdfReader(temp_path)
        pdf_writer.add_page(pdf_reader.pages[0])

        # Clean up the temporary file
        os.remove(temp_path)

    # Write the final PDF
    with open(file_path, "wb") as output_file:
        pdf_writer.write(output_file)


def test_split_pdf_pages_with_multi_page_pdf():
    """
    Test split_pdf_pages with a multi-page PDF.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a multi-page test PDF file
        pdf_path = Path(temp_dir) / "test_multi_page.pdf"
        create_test_pdf(pdf_path, num_pages=3)

        # Create a mock ToolContext
        tool_context = MockToolContext()

        # Call the split_pdf_pages function
        result = split_pdf_pages(str(pdf_path), tool_context)

        # Verify the result
        assert result["status"] == "success"
        assert "Successfully split PDF" in result["message"]
        assert len(result["files"]) == 3

        # Check that the files were created
        for file_path in result["files"].keys():
            assert Path(file_path).exists()
            # Verify it's a JPEG image
            with Image.open(file_path) as img:
                assert img.format == "JPEG"

        # Verify tool_context.state was updated correctly
        assert "files" in tool_context.state
        assert len(tool_context.state["files"]) == 3
        for file_path in result["files"].keys():
            assert file_path in tool_context.state["files"]
            assert tool_context.state["files"][file_path] == ""


def test_split_pdf_pages_with_single_page_pdf():
    """
    Test split_pdf_pages with a single-page PDF.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a single-page test PDF file
        pdf_path = Path(temp_dir) / "test_single_page.pdf"
        create_test_pdf(pdf_path, num_pages=1)

        # Create a mock ToolContext
        tool_context = MockToolContext()

        # Call the split_pdf_pages function
        result = split_pdf_pages(str(pdf_path), tool_context)

        # Verify the result
        assert result["status"] == "success"
        assert "Successfully split PDF" in result["message"]
        assert len(result["files"]) == 1

        # Check that the file was created
        file_path = list(result["files"].keys())[0]
        assert Path(file_path).exists()
        # Verify it's a JPEG image
        with Image.open(file_path) as img:
            assert img.format == "JPEG"

        # Verify tool_context.state was updated correctly
        assert "files" in tool_context.state
        assert len(tool_context.state["files"]) == 1
        assert file_path in tool_context.state["files"]
        assert tool_context.state["files"][file_path] == ""


def test_split_pdf_pages_nonexistent_file():
    """
    Test split_pdf_pages with a non-existent file.
    """
    # Create a path that definitely doesn't exist
    nonexistent_file = "/path/that/definitely/does/not/exist.pdf"

    # Create a mock ToolContext
    tool_context = MockToolContext()

    # Call the split_pdf_pages function
    result = split_pdf_pages(nonexistent_file, tool_context)

    # Verify the result
    assert result["status"] == "error"
    assert "does not exist" in result["message"]
    assert len(result["files"]) == 0

    # Verify tool_context.state was not updated
    assert (
        not tool_context.state
        or "files" not in tool_context.state
        or len(tool_context.state["files"]) == 0
    )


def test_split_pdf_pages_invalid_file():
    """
    Test split_pdf_pages with an invalid file (not a PDF).
    """
    with tempfile.NamedTemporaryFile(suffix=".txt") as temp_file:
        # Write some content to make it not a valid PDF
        temp_file.write(b"This is not a PDF file")
        temp_file.flush()

        # Create a mock ToolContext
        tool_context = MockToolContext()

        # Call the split_pdf_pages function
        result = split_pdf_pages(temp_file.name, tool_context)

        # Verify the result
        assert result["status"] == "error"
        assert "not a PDF" in result["message"]
        assert len(result["files"]) == 0

        # Verify tool_context.state was not updated
        assert (
            not tool_context.state
            or "files" not in tool_context.state
            or len(tool_context.state["files"]) == 0
        )
