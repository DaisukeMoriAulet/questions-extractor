"""
Utility for Supabase connection.
"""

import os
from typing import Optional

from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()


def get_supabase_client() -> Client:
    """
    Create and return a Supabase client using credentials from environment variables.

    Returns:
        Client: A Supabase client instance.

    Raises:
        ValueError: If SUPABASE_URL or SUPABASE_API_KEY environment variables are not set.
    """
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_API_KEY")

    if not supabase_url or not supabase_key:
        raise ValueError(
            "SUPABASE_URL and SUPABASE_API_KEY must be set in environment variables."
        )

    return create_client(supabase_url, supabase_key)