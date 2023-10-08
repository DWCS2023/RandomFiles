"""
Filename:     RandomFileHandlingExample.py
Author:       Amin Teymorian
Date:         8 October 2023

Description:  This script implements the handling random files example
              from the CAIE 9618 Pseudocode Guide for Teachers. Initial
              records are added to a binary file at specified positions,
              shifted down by one position, and new record is added at a
              specified position. The pickle module is used to serialize 
              and deserialze Student objects.
"""

import pickle

# Assuming each pickled pupil takes no more than 200 bytes
PUPIL_SIZE = 200

class Student():
    def __init__(self, 
                 last_name="", 
                 first_name="", 
                 date_of_birth="", 
                 year_group=0, 
                 form_group='0'):
        self.last_name = last_name
        self.first_name = first_name
        self.date_of_birth = date_of_birth
        self.year_group = year_group
        self.form_group = form_group


def add_initial_records(filename):
    with open(filename, 'wb') as file:
        for position in range(10, 21):
            pupil = Student("Johnson", "Leroy", "07/10/2023", position, 'T')
            file.seek(position * PUPIL_SIZE)
            pickle.dump(pupil, file)

def shift_and_insert(filename):
    new_pupil = Student()
    new_pupil.last_name = "Johnson"
    new_pupil.first_name = "Leroy"
    new_pupil.date_of_birth = "07/10/2023"
    new_pupil.year_group = 6
    new_pupil.form_group = 'A'

    with open(filename, 'rb+') as file:
        # Shift records 20 to 10 one position down
        for position in range(20, 9, -1):
            file.seek(position * PUPIL_SIZE)
            pupil = pickle.load(file)
            file.seek((position + 1) * PUPIL_SIZE)
            pickle.dump(pupil, file)

        # Insert new record at position 10
        file.seek(10 * PUPIL_SIZE)
        pickle.dump(new_pupil, file)

# Test driver checks select pupils before and after the shift
def check_pupil(filename, position):
  with open(filename, 'rb') as file:
    file.seek(position * PUPIL_SIZE)
    pupil = pickle.load(file)
    print(f"Pupil at position {position}:",
          f"Year Group = {pupil.year_group},",
          f"Form Group = {pupil.form_group}")

add_initial_records('StudentFile.Dat')
check_pupil('StudentFile.Dat', 10)
check_pupil('StudentFile.Dat', 20)
shift_and_insert('StudentFile.Dat')
check_pupil('StudentFile.Dat', 10)
check_pupil('StudentFile.Dat', 11)
check_pupil('StudentFile.Dat', 21)