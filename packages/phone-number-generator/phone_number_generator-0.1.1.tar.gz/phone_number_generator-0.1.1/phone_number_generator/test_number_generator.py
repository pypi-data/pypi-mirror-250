import unittest
from main import Number_generator


class TestNumberGenerator(unittest.TestCase):

    def setUp(self):
        # This method is called before each test
        self.phone_generator = Number_generator(phone_ini="123", country="USA")

    def test_gen_phone(self):
        # Test if gen_phone() returns a valid phone number
        phone_number = self.phone_generator.gen_phone()
        self.assertTrue(self.phone_generator.is_valid_phone(phone_number))

    def test_gen_multiple_phones(self):
        # Test if gen_multiple_phones() returns a list of valid phone numbers
        num_phone_numbers = 5
        multiple_phones = self.phone_generator.gen_multiple_phones(
            num_phone_numbers)
        self.assertEqual(len(multiple_phones), num_phone_numbers)
        for phone_number in multiple_phones:
            self.assertTrue(self.phone_generator.is_valid_phone(phone_number))

    def test_search_existing_country(self):
        # Test if search() returns the correct international code for an existing country
        country = "USA"
        int_code = self.phone_generator.search(country)
        self.assertEqual(int_code, "+1")

    def test_search_nonexistent_country(self):
        # Test if search() returns None for a nonexistent country
        country = "NonexistentCountry"
        int_code = self.phone_generator.search(country)
        self.assertIsNone(int_code)

    def test_save_to_text_file(self):
        # Test if save_to_text_file() successfully saves the specified number of phone numbers to a file
        num_phone_numbers = 3
        filename = "test_generated_phone_numbers.txt"
        success = self.phone_generator.save_to_text_file(
            num_phone_numbers, filename)
        self.assertTrue(success)

        # Check if the saved file contains the correct number of lines
        with open(filename, 'r') as file:
            lines = file.readlines()
            self.assertEqual(len(lines), num_phone_numbers)

        # Clean up: remove the test file
        import os
        os.remove(filename)
