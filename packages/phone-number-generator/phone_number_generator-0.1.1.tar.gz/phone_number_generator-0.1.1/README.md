# Number Generator

The `Number_generator` class is a Python utility for generating random phone numbers with optional country codes. It provides flexibility in generating individual numbers or creating batches of random phone numbers. Additionally, it supports saving generated phone numbers to a text file.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Methods](#methods)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## Installation

To use the `Number_generator` class, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/mosesoyediran/number-generator.git
   Navigate to the project directory:
   bash
   Copy code
   cd number-generator
   Use the Number_generator class in your Python scripts or projects.
   Usage
   ```

Import the Number_generator class into your Python script and create an instance to generate random phone numbers. The class can also be used to save generated phone numbers to a text file.

python
Copy code
from number_generator import Number_generator

# Create an instance of Number_generator

phone_generator = Number_generator(phone_ini="123", country="USA")

# Generate a random phone number

random_phone = phone_generator.gen_phone()
print("Generated Phone Number:", random_phone)

# Generate a list of random phone numbers

multiple_phones = phone_generator.gen_multiple_phones(5)
print("Generated Phone Numbers:", multiple_phones)

# Save generated phone numbers to a text file

phone_generator.save_to_text_file(10, "generated_phone_numbers.txt")
Methods

**init**(phone_ini=None, country=None)
Initializes a Number_generator object.

phone_ini: Initial part of the generated phone number.
country: Country for which the phone number will be generated.
gen_phone()
Generates a random phone number based on specified criteria.

search(country)
Searches for the international code (int_code) associated with the given country.

country: Country for which the international code is sought.
gen_multiple_phones(num_phone_numbers)
Generates a list of random phone numbers.

num_phone_numbers: The number of phone numbers to generate.
save_to_text_file(num_phone_numbers, filename)
Generates and saves a specified number of phone numbers to a text file.

num_phone_numbers: The number of phone numbers to generate and save.
filename: The name of the file to which the phone numbers will be saved.
Examples

For more examples on how to use the Number_generator class, refer to the Examples directory in this repository.

Contributing

Contributions are welcome! If you find a bug or have a suggestion, please open an issue.

License

This project is licensed under the MIT License.
