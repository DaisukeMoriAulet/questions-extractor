"""
Tests for the backoff utility.
"""

import time
import unittest
from unittest.mock import MagicMock, patch

from utils.backoff import exponential_backoff


class TestExponentialBackoff(unittest.TestCase):
    """Test cases for the exponential_backoff utility."""

    @patch('time.sleep')
    def test_successful_first_attempt(self, mock_sleep):
        """Test that the function returns normally on successful first attempt."""
        mock_fn = MagicMock(return_value="success")
        
        result = exponential_backoff(mock_fn, max_retries=3)()
        
        mock_fn.assert_called_once()
        mock_sleep.assert_not_called()
        self.assertEqual(result, "success")

    @patch('time.sleep')
    def test_successful_after_retries(self, mock_sleep):
        """Test that the function retries and eventually succeeds."""
        # Function that fails twice then succeeds
        mock_fn = MagicMock(side_effect=[ValueError("Failed"), ValueError("Failed"), "success"])
        
        result = exponential_backoff(mock_fn, max_retries=3, retryable_exceptions=(ValueError,))()
        
        self.assertEqual(mock_fn.call_count, 3)
        self.assertEqual(mock_sleep.call_count, 2)  # Sleep called for each retry
        self.assertEqual(result, "success")

    @patch('time.sleep')
    def test_failure_after_retries(self, mock_sleep):
        """Test that the function raises the last exception after exhausting all retries."""
        # Function that always fails
        mock_fn = MagicMock(side_effect=ValueError("Failed"))
        
        with self.assertRaises(ValueError):
            exponential_backoff(mock_fn, max_retries=2, retryable_exceptions=(ValueError,))()
        
        self.assertEqual(mock_fn.call_count, 3)  # Initial try + 2 retries
        self.assertEqual(mock_sleep.call_count, 2)  # Sleep called for each retry

    @patch('time.sleep')
    def test_delay_calculation_without_jitter(self, mock_sleep):
        """Test correct delay calculation without jitter."""
        # Function that fails twice then succeeds
        mock_fn = MagicMock(side_effect=[ValueError("Failed"), ValueError("Failed"), "success"])
        
        exponential_backoff(
            mock_fn, 
            max_retries=3, 
            base_delay_seconds=1.0, 
            jitter=False, 
            retryable_exceptions=(ValueError,)
        )()
        
        # Check that sleep was called with the correct exponential delays
        mock_sleep.assert_any_call(1.0)  # First retry: 1.0 * 2^0
        mock_sleep.assert_any_call(2.0)  # Second retry: 1.0 * 2^1

    @patch('time.sleep')
    @patch('random.uniform', return_value=0.5)  # Fixed value for testing
    def test_delay_calculation_with_jitter(self, mock_random, mock_sleep):
        """Test correct delay calculation with jitter."""
        # Function that fails twice then succeeds
        mock_fn = MagicMock(side_effect=[ValueError("Failed"), ValueError("Failed"), "success"])
        
        exponential_backoff(
            mock_fn, 
            max_retries=3, 
            base_delay_seconds=1.0, 
            jitter=True, 
            retryable_exceptions=(ValueError,)
        )()
        
        # Check that sleep was called with jitter added to exponential delays
        # With our mocked random.uniform returning 0.5:
        # First retry: 1.0 * 2^0 + 0.5 = 1.5
        # Second retry: 1.0 * 2^1 + 0.5 = 2.5
        mock_sleep.assert_any_call(1.5)  
        mock_sleep.assert_any_call(2.5)  

    @patch('time.sleep')
    def test_non_retryable_exception(self, mock_sleep):
        """Test that non-retryable exceptions are immediately raised."""
        # Function that raises a non-retryable exception
        mock_fn = MagicMock(side_effect=KeyError("Not retryable"))
        
        with self.assertRaises(KeyError):
            exponential_backoff(
                mock_fn, 
                max_retries=3, 
                retryable_exceptions=(ValueError, TypeError)
            )()
        
        mock_fn.assert_called_once()  # Function called only once
        mock_sleep.assert_not_called()  # No retries attempted

    @patch('time.sleep')
    def test_max_retries_zero(self, mock_sleep):
        """Test behavior with max_retries=0 (should attempt once)."""
        # Function that fails
        mock_fn = MagicMock(side_effect=ValueError("Failed"))
        
        with self.assertRaises(ValueError):
            exponential_backoff(mock_fn, max_retries=0, retryable_exceptions=(ValueError,))()
        
        mock_fn.assert_called_once()  # Function called only once
        mock_sleep.assert_not_called()  # No retries attempted

    @patch('time.sleep')
    def test_max_delay_cap(self, mock_sleep):
        """Test that delay is capped at max_delay_seconds."""
        # Function that fails multiple times
        mock_fn = MagicMock(side_effect=[
            ValueError("Failed"), 
            ValueError("Failed"), 
            ValueError("Failed"), 
            ValueError("Failed"), 
            "success"
        ])
        
        exponential_backoff(
            mock_fn, 
            max_retries=4, 
            base_delay_seconds=10.0, 
            max_delay_seconds=30.0, 
            jitter=False, 
            retryable_exceptions=(ValueError,)
        )()
        
        # Check that sleep was called with delays capped at max_delay_seconds
        # 10.0 * 2^0 = 10.0
        # 10.0 * 2^1 = 20.0
        # 10.0 * 2^2 = 40.0 -> capped to 30.0
        # 10.0 * 2^3 = 80.0 -> capped to 30.0
        mock_sleep.assert_any_call(10.0)
        mock_sleep.assert_any_call(20.0)
        mock_sleep.assert_any_call(30.0)  # Capped at max_delay_seconds

    def test_decorator_usage(self):
        """Test that the utility can be used as a decorator."""
        counter = {"count": 0}
        
        @exponential_backoff(max_retries=2, retryable_exceptions=(ValueError,))
        def test_function():
            counter["count"] += 1
            if counter["count"] < 2:
                raise ValueError("Failed")
            return "success"
        
        # Use patch as a context manager for this test
        with patch('time.sleep'):
            result = test_function()
        
        self.assertEqual(result, "success")
        self.assertEqual(counter["count"], 2)  # Function called twice


if __name__ == "__main__":
    unittest.main()