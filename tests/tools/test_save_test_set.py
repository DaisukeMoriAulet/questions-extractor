"""
Tests for the save_test_set tool.
"""

import pytest
from unittest.mock import MagicMock, patch

from questions_extractor_agent.tools.database_tools import save_test_set


class MockToolContext:
    """
    Mock implementation of ToolContext for testing.
    """

    def __init__(self):
        self.state = {}


class MockSupabaseResponse:
    """
    Mock implementation of Supabase response for testing.
    """

    def __init__(self, data=None, error=None):
        self.data = data
        self.error = error


class MockSupabaseTable:
    """
    Mock implementation of Supabase table for testing.
    """

    def __init__(self, data=None, error=None):
        self.data = data or []
        self.error = error
        self.upserted_data = []
        self.conflict_columns = []

    def upsert(self, data, on_conflict=None):
        self.upserted_data.append(data)
        if on_conflict:
            self.conflict_columns = on_conflict
        return self

    def execute(self):
        # Add an 'id' field to the data if it doesn't exist
        for item in self.upserted_data:
            if "id" not in item:
                item["id"] = len(self.data) + 1
        
        self.data.extend(self.upserted_data)
        response = MockSupabaseResponse(data=self.upserted_data)
        self.upserted_data = []
        return response


@pytest.fixture
def mock_supabase_client():
    """
    Fixture to create a mock Supabase client.
    """
    mock_client = MagicMock()
    
    # Mock tables with data
    tables = {
        "test_forms": MockSupabaseTable(),
        "sections": MockSupabaseTable(),
        "parts": MockSupabaseTable(),
        "passage_sets": MockSupabaseTable(),
        "passages": MockSupabaseTable(),
        "questions": MockSupabaseTable(),
        "choices": MockSupabaseTable(),
        "tags": MockSupabaseTable(),
        "question_tags": MockSupabaseTable(),
    }
    
    # Mock the table method to return the appropriate table
    mock_client.table = lambda name: tables[name]
    
    return mock_client


@pytest.fixture
def sample_test_set():
    """
    Fixture to create a sample test set for testing.
    """
    return {
        "test_forms": [
            {"name": "TOEIC Sample Test"}
        ],
        "sections": [
            {"label": "Reading", "order_no": 1}
        ],
        "parts": [
            {"section_id": 1, "label": "Part 5", "question_format": "short_blank", "order_no": 1}
        ],
        "passage_sets": [
            {"part_id": 1, "order_no": 1, "question_range": "[101,106)"}
        ],
        "passages": [
            {"passage_set_id": 1, "order_no": 1, "body": "Sample passage text"}
        ],
        "questions": [
            {
                "passage_set_id": 1, 
                "part_id": 1, 
                "number": 101, 
                "stem": "What is the answer?"
            },
            {
                "passage_set_id": 1, 
                "part_id": 1, 
                "number": 102, 
                "stem": "Choose the best option."
            }
        ],
        "choices": [
            {"question_id": 1, "label": "A", "content": "Option A", "is_correct": False},
            {"question_id": 1, "label": "B", "content": "Option B", "is_correct": True},
            {"question_id": 2, "label": "A", "content": "Option A", "is_correct": True},
            {"question_id": 2, "label": "B", "content": "Option B", "is_correct": False}
        ],
        "tags": [
            {"level1": "Grammar", "level2": "Verb Tenses"}
        ],
        "question_tags": [
            {"question_id": 1, "tag_id": 1}
        ]
    }


def test_save_test_set_success(mock_supabase_client, sample_test_set):
    """
    Test save_test_set with successful data insertion.
    """
    with patch('questions_extractor_agent.tools.database_tools.get_supabase_client', 
               return_value=mock_supabase_client):
        tool_context = MockToolContext()
        result = save_test_set(sample_test_set, tool_context)
        
        # Verify the result
        assert result["status"] == "success"
        assert "Successfully upserted" in result["message"]
        assert result["rows_upserted"] > 0
        
        # Verify that all tables were updated
        test_forms_table = mock_supabase_client.table("test_forms")
        sections_table = mock_supabase_client.table("sections")
        parts_table = mock_supabase_client.table("parts")
        questions_table = mock_supabase_client.table("questions")
        choices_table = mock_supabase_client.table("choices")
        
        assert len(test_forms_table.data) == 1
        assert len(sections_table.data) == 1
        assert len(parts_table.data) == 1
        assert len(questions_table.data) == 2
        assert len(choices_table.data) == 4


def test_save_test_set_onconflict_questions(mock_supabase_client, sample_test_set):
    """
    Test save_test_set with onConflict for questions.
    """
    with patch('questions_extractor_agent.tools.database_tools.get_supabase_client', 
               return_value=mock_supabase_client):
        tool_context = MockToolContext()
        # First insert
        save_test_set(sample_test_set, tool_context)
        
        # Get the questions table to check the conflict columns
        questions_table = mock_supabase_client.table("questions")
        assert questions_table.conflict_columns == ["part_id", "number"]
        
        # Update a question (should use onConflict)
        updated_test_set = {
            "test_forms": [{"id": 1, "name": "TOEIC Sample Test Updated"}],
            "questions": [
                {
                    "passage_set_id": 1, 
                    "part_id": 1, 
                    "number": 101,  # Same number, should update not insert
                    "stem": "Updated question stem"
                }
            ]
        }
        
        result = save_test_set(updated_test_set, tool_context)
        
        # Verify the result
        assert result["status"] == "success"
        
        # The question should be updated not duplicated
        assert len(questions_table.data) == 3  # 2 original + 1 update
        
        # Find the updated question - the latest one should have the updated stem
        updated_question = questions_table.data[-1]
        assert updated_question["stem"] == "Updated question stem"


def test_save_test_set_onconflict_choices(mock_supabase_client, sample_test_set):
    """
    Test save_test_set with onConflict for choices.
    """
    with patch('questions_extractor_agent.tools.database_tools.get_supabase_client', 
               return_value=mock_supabase_client):
        tool_context = MockToolContext()
        # First insert
        save_test_set(sample_test_set, tool_context)
        
        # Get the choices table to check the conflict columns
        choices_table = mock_supabase_client.table("choices")
        assert choices_table.conflict_columns == ["question_id", "label"]
        
        # Update a choice (should use onConflict)
        updated_test_set = {
            "test_forms": [{"id": 1, "name": "TOEIC Sample Test"}],
            "choices": [
                {
                    "question_id": 1, 
                    "label": "A",  # Same label, should update not insert
                    "content": "Updated option A",
                    "is_correct": True
                }
            ]
        }
        
        result = save_test_set(updated_test_set, tool_context)
        
        # Verify the result
        assert result["status"] == "success"
        
        # The choice should be updated not duplicated
        assert len(choices_table.data) == 5  # 4 original + 1 update
        
        # Find the updated choice - the latest one should have the updated content
        updated_choice = choices_table.data[-1]
        assert updated_choice["content"] == "Updated option A"
        assert updated_choice["is_correct"] is True


def test_save_test_set_error_handling(mock_supabase_client):
    """
    Test save_test_set with error handling.
    """
    with patch('questions_extractor_agent.tools.database_tools.get_supabase_client', 
               return_value=mock_supabase_client):
        tool_context = MockToolContext()
        
        # Test with empty test set
        result = save_test_set({}, tool_context)
        assert result["status"] == "error"
        assert "No test_forms data provided" in result["message"]
        
        # Test with invalid test set structure
        invalid_test_set = {
            "test_forms": []  # Empty test_forms list
        }
        result = save_test_set(invalid_test_set, tool_context)
        assert result["status"] == "error"
        assert "No test_forms data provided" in result["message"]


def test_save_test_set_supabase_config_error():
    """
    Test save_test_set with Supabase configuration error.
    """
    with patch('questions_extractor_agent.tools.database_tools.get_supabase_client', 
               side_effect=ValueError("Missing Supabase credentials")):
        tool_context = MockToolContext()
        result = save_test_set({"test_forms": [{"name": "Test"}]}, tool_context)
        
        assert result["status"] == "error"
        assert "Supabase configuration error" in result["message"]
        assert result["rows_upserted"] == 0


def test_save_test_set_general_exception(mock_supabase_client):
    """
    Test save_test_set with a general exception.
    """
    with patch('questions_extractor_agent.tools.database_tools.get_supabase_client', 
               return_value=mock_supabase_client):
        with patch.object(mock_supabase_client, 'table', side_effect=Exception("Unexpected error")):
            tool_context = MockToolContext()
            result = save_test_set({"test_forms": [{"name": "Test"}]}, tool_context)
            
            assert result["status"] == "error"
            assert "Error upserting test data" in result["message"]
            assert result["rows_upserted"] == 0