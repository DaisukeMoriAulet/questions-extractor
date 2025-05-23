"""
Tool for saving test sets to the Supabase database.
"""

from typing import Dict, Any, List, Optional, Union

from google.adk.tools import ToolContext

from utils.supabase import get_supabase_client


def save_test_set(test_set: Dict[str, Any], tool_context: ToolContext) -> Dict[str, Any]:
    """
    Upsert the structured test set to Supabase.

    This function saves the provided test set data to Supabase, handling the relationships
    between tables and enforcing onConflict constraints for questions and choices.

    Args:
        test_set (Dict[str, Any]): A dictionary containing the structured test data
                                   conforming to the 7+2 table structure.
        tool_context (ToolContext): ADK ToolContext.

    Returns:
        Dict[str, Any]: A dictionary containing:
            - status: "success" or "error"
            - message: A string describing the success or error
            - rows_upserted: Number of rows upserted (integer)
            
    Example:
        ```python
        # Example test set
        test_set = {
            "test_forms": [{"name": "TOEIC Sample Test"}],
            "sections": [{"label": "Reading", "order_no": 1}],
            "parts": [{"section_id": 1, "label": "Part 5", "question_format": "short_blank", "order_no": 1}],
            "passage_sets": [{"part_id": 1, "order_no": 1, "question_range": "[101,106)"}],
            "passages": [{"passage_set_id": 1, "order_no": 1, "body": "Sample passage text"}],
            "questions": [
                {"passage_set_id": 1, "part_id": 1, "number": 101, "stem": "Question 1"},
                {"passage_set_id": 1, "part_id": 1, "number": 102, "stem": "Question 2"}
            ],
            "choices": [
                {"question_id": 1, "label": "A", "content": "Option A", "is_correct": False},
                {"question_id": 1, "label": "B", "content": "Option B", "is_correct": True}
            ],
            "tags": [{"level1": "Grammar", "level2": "Verb Tenses"}],
            "question_tags": [{"question_id": 1, "tag_id": 1}]
        }
        
        # Call the function
        result = save_test_set(test_set, tool_context)
        
        # Expected result
        # {
        #    "status": "success",
        #    "message": "Successfully upserted 11 rows of test data",
        #    "rows_upserted": 11
        # }
        ```
    """
    try:
        # Get Supabase client
        supabase = get_supabase_client()
        rows_upserted = 0
        
        # 1. Upsert test_forms
        test_forms = test_set.get("test_forms", [])
        if test_forms:
            test_form_data = test_forms[0]  # Assuming one test form per test set
            test_form_response = supabase.table("test_forms").upsert(test_form_data).execute()
            
            if test_form_response.data:
                rows_upserted += len(test_form_response.data)
                test_form_id = test_form_response.data[0]["id"]
            else:
                return {
                    "status": "error",
                    "message": "Failed to upsert test_form data",
                    "rows_upserted": rows_upserted
                }
        else:
            return {
                "status": "error",
                "message": "No test_forms data provided",
                "rows_upserted": 0
            }
        
        # 2. Upsert sections
        sections = test_set.get("sections", [])
        section_id_map = {}  # To store the IDs of the inserted sections
        
        for section in sections:
            if "test_id" not in section:
                section["test_id"] = test_form_id
            
            section_response = supabase.table("sections").upsert(section).execute()
            
            if section_response.data:
                rows_upserted += len(section_response.data)
                for s in section_response.data:
                    section_id_map[s["label"]] = s["id"]
            else:
                return {
                    "status": "error",
                    "message": f"Failed to upsert section: {section}",
                    "rows_upserted": rows_upserted
                }
        
        # 3. Upsert parts
        parts = test_set.get("parts", [])
        part_id_map = {}  # To store the IDs of the inserted parts
        
        for part in parts:
            if "section_id" not in part and "section_label" in part:
                part["section_id"] = section_id_map.get(part["section_label"])
                del part["section_label"]  # Remove the temporary field
            
            part_response = supabase.table("parts").upsert(part).execute()
            
            if part_response.data:
                rows_upserted += len(part_response.data)
                for p in part_response.data:
                    part_id_map[p["label"]] = p["id"]
            else:
                return {
                    "status": "error",
                    "message": f"Failed to upsert part: {part}",
                    "rows_upserted": rows_upserted
                }
        
        # 4. Upsert passage_sets
        passage_sets = test_set.get("passage_sets", [])
        passage_set_id_map = {}  # To store the IDs of the inserted passage_sets
        
        for passage_set in passage_sets:
            if "part_id" not in passage_set and "part_label" in passage_set:
                passage_set["part_id"] = part_id_map.get(passage_set["part_label"])
                del passage_set["part_label"]  # Remove the temporary field
            
            passage_set_response = supabase.table("passage_sets").upsert(passage_set).execute()
            
            if passage_set_response.data:
                rows_upserted += len(passage_set_response.data)
                for ps in passage_set_response.data:
                    passage_set_id_map[f"{ps['part_id']}_{ps['order_no']}"] = ps["id"]
            else:
                return {
                    "status": "error",
                    "message": f"Failed to upsert passage_set: {passage_set}",
                    "rows_upserted": rows_upserted
                }
        
        # 5. Upsert passages
        passages = test_set.get("passages", [])
        passage_id_map = {}  # To store the IDs of the inserted passages
        
        for passage in passages:
            if "passage_set_id" not in passage and "passage_set_key" in passage:
                passage["passage_set_id"] = passage_set_id_map.get(passage["passage_set_key"])
                del passage["passage_set_key"]  # Remove the temporary field
            
            passage_response = supabase.table("passages").upsert(passage).execute()
            
            if passage_response.data:
                rows_upserted += len(passage_response.data)
                for p in passage_response.data:
                    passage_id_map[f"{p['passage_set_id']}_{p['order_no']}"] = p["id"]
            else:
                return {
                    "status": "error",
                    "message": f"Failed to upsert passage: {passage}",
                    "rows_upserted": rows_upserted
                }
        
        # 6. Upsert questions with onConflict=["part_id", "number"]
        questions = test_set.get("questions", [])
        question_id_map = {}  # To store the IDs of the inserted questions
        
        for question in questions:
            if "passage_set_id" not in question and "passage_set_key" in question:
                question["passage_set_id"] = passage_set_id_map.get(question["passage_set_key"])
                del question["passage_set_key"]  # Remove the temporary field
            
            if "part_id" not in question and "part_label" in question:
                question["part_id"] = part_id_map.get(question["part_label"])
                del question["part_label"]  # Remove the temporary field
            
            question_response = (
                supabase.table("questions")
                .upsert(question, on_conflict=["part_id", "number"])
                .execute()
            )
            
            if question_response.data:
                rows_upserted += len(question_response.data)
                for q in question_response.data:
                    question_id_map[f"{q['part_id']}_{q['number']}"] = q["id"]
            else:
                return {
                    "status": "error",
                    "message": f"Failed to upsert question: {question}",
                    "rows_upserted": rows_upserted
                }
        
        # 7. Upsert choices with onConflict=["question_id", "label"]
        choices = test_set.get("choices", [])
        
        for choice in choices:
            if "question_id" not in choice and "question_key" in choice:
                question_key = choice["question_key"]
                choice["question_id"] = question_id_map.get(question_key)
                del choice["question_key"]  # Remove the temporary field
            
            choice_response = (
                supabase.table("choices")
                .upsert(choice, on_conflict=["question_id", "label"])
                .execute()
            )
            
            if choice_response.data:
                rows_upserted += len(choice_response.data)
            else:
                return {
                    "status": "error",
                    "message": f"Failed to upsert choice: {choice}",
                    "rows_upserted": rows_upserted
                }
        
        # 8. Upsert tags
        tags = test_set.get("tags", [])
        tag_id_map = {}  # To store the IDs of the inserted tags
        
        for tag in tags:
            tag_response = supabase.table("tags").upsert(tag).execute()
            
            if tag_response.data:
                rows_upserted += len(tag_response.data)
                for t in tag_response.data:
                    tag_id_map[f"{t['level1']}_{t.get('level2', '')}_{t.get('level3', '')}"] = t["id"]
            else:
                return {
                    "status": "error",
                    "message": f"Failed to upsert tag: {tag}",
                    "rows_upserted": rows_upserted
                }
        
        # 9. Upsert question_tags
        question_tags = test_set.get("question_tags", [])
        
        for question_tag in question_tags:
            if "question_id" not in question_tag and "question_key" in question_tag:
                question_tag["question_id"] = question_id_map.get(question_tag["question_key"])
                del question_tag["question_key"]  # Remove the temporary field
            
            if "tag_id" not in question_tag and "tag_key" in question_tag:
                question_tag["tag_id"] = tag_id_map.get(question_tag["tag_key"])
                del question_tag["tag_key"]  # Remove the temporary field
            
            question_tag_response = supabase.table("question_tags").upsert(question_tag).execute()
            
            if question_tag_response.data:
                rows_upserted += len(question_tag_response.data)
            else:
                return {
                    "status": "error",
                    "message": f"Failed to upsert question_tag: {question_tag}",
                    "rows_upserted": rows_upserted
                }
        
        return {
            "status": "success",
            "message": f"Successfully upserted {rows_upserted} rows of test data",
            "rows_upserted": rows_upserted
        }
    
    except ValueError as e:
        return {
            "status": "error",
            "message": f"Supabase configuration error: {str(e)}",
            "rows_upserted": 0
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error upserting test data: {str(e)}",
            "rows_upserted": 0
        }