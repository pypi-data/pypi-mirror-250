from random import randint
# World_zone is a data structure containing country information
from world_zone import world_zone


class Number_generator:
    """
    A class for generating random phone numbers with optional country codes.
    """

    def __init__(self, phone_ini=None, country=None):
        """
        Initializes a Number_generator object.

        :param phone_ini: Initial part of the generated phone number.
        :param country: Country for which the phone number will be generated.
        """
        self.phone_ini = phone_ini
        self.country = self.search(country)

    def gen_phone(self):
        """
        Generates a random phone number based on specified criteria.

        :return: Generated phone number.
        """
        # Generate random components of the phone number
        first = str(randint(100, 999))
        second = str(randint(1, 888)).zfill(3)

        # Ensure the last part of the number is not one of the restricted values
        last = (str(randint(1, 9998)).zfill(4))
        while last in ['1111', '2222', '3333', '4444', '5555', '6666', '7777', '8888']:
            last = (str(randint(1, 9998)).zfill(4))

        # Format the phone number based on country information
        if self.country is None:
            return '{}{}{}'.format(self.phone_ini or first, second, last)
        else:
            return '+{}{}{}{}'.format(self.country, self.phone_ini or first, second, last)

    def search(self, country):
        """
        Searches for the international code (int_code) associated with the given country.

        :param country: Country for which the international code is sought.
        :return: International code if found, otherwise None.
        """
        try:
            return [element for element in world_zone if element['country'] == country][0]['int_code']
        except IndexError:
            return None

    def gen_multiple_phones(self, num_phone_numbers):
        """
        Generate a list of phone numbers.

        :param num_phone_numbers: The number of phone numbers to generate.
        :return: List of generated phone numbers.
        """
        phone_numbers = [self.gen_phone() for _ in range(num_phone_numbers)]
        return phone_numbers

    def save_to_text_file(self, num_phone_numbers, filename):
        """
        Generate and save a specified number of phone numbers to a text file.

        :param num_phone_numbers: The number of phone numbers to generate and save.
        :param filename: The name of the file to which the phone numbers will be saved.
        :return: True if the operation was successful, False otherwise.
        """
        try:
            with open(filename, 'w') as file:
                for _ in range(num_phone_numbers):
                    phone_number = self.gen_phone()
                    # Add a newline between each phone number
                    file.write(phone_number + '\n')

            print(
                f"{num_phone_numbers} phone numbers successfully saved to {filename}")
            return True
        except Exception as e:
            print(f"Error saving phone numbers to {filename}: {e}")
            return False
