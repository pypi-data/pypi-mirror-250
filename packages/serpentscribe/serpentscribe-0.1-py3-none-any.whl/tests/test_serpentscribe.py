import uuid
import os, sys
import unittest
import json
from serpentscribe.logger import log_output

# A sample function to be decorated
def sample_function(a, b):
    return a + b

class TestSerpentScribe(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.log_file = 'function_log.json'

    # This will run before each test
    def setUp(self):
        self.unique_log_file = f"function_log_{uuid.uuid4()}.json"
        self.sample_function = log_output()(sample_function)


    def test_sample_function(self):
        try:
            # Open the unique log file before the test
            self.log_file_handle = open(self.unique_log_file, 'w')
        except IOError:
            self.fail("Couldn't open log file for writing.")

        # Redirect sys.stdout to the log file handle
        sys.stdout = self.log_file_handle

        # Run the sample function
        result = self.sample_function(3, 4)  # use self.sample_function here
        self.assertEqual(result, 7)

        # Revert sys.stdout back to its original state
        sys.stdout = sys.__stdout__

        # Close the log file handle after the test
        self.log_file_handle.close()

        # Verify the log entry
        with open(self.unique_log_file, 'r') as file:
            logs = file.readlines()
            self.assertEqual(len(logs), 1)

            log_entry = json.loads(logs[0])
            self.assertEqual(log_entry['function'], 'sample_function')
            self.assertEqual(log_entry['arguments']['args'], [3, 4])
            self.assertEqual(log_entry['arguments']['kwargs'], {})
            self.assertEqual(log_entry['result'], 7)

    # This will run after each test
    def tearDown(self):
        if os.path.exists(self.unique_log_file):
            os.remove(self.unique_log_file)

    @classmethod
    def tearDownClass(cls):
        pass  # You may want to clean up cls.log_file here

if __name__ == '__main__':
    unittest.main()
