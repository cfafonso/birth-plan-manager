#-*- coding: utf-8 -*-


from classes.DoctorsCollection import DoctorsCollection
from classes.MothersCollection import MothersCollection
from classes.Schedule import Schedule
from classes.DataManager import DataManager
from classes.Header import Header

from sys import argv

from constants import DOCTORS_FILE_INDEX, SCHEDULE_FILE_INDEX, REQUESTS_FILE_INDEX


def plan(doctors_file, schedule_file, requests_file):
    """
    Reads the three input files, assigns doctors to birth assistance requests, according to the criteria defined 
    in the specification of the birth-plan-manager tool, and writes the two output files.

    Args:
        doctors_file (str): the doctors file containing the doctors available for an assistance.
        schedule_file (str): the schedule file containing the planed assistances.
        requests_file (str): the requests file containing the mothers that need an assistance.
    """
    
    try:
        for file_position in [DOCTORS_FILE_INDEX, SCHEDULE_FILE_INDEX, REQUESTS_FILE_INDEX]:
            file_name = argv[file_position]
            collection = DataManager(file_name)
            file_scope = collection.retrieve_file_scope(file_position)
            
            actual_header = collection.get_header()

            expected_header_from_file_name = Header(actual_header.get_organization(), actual_header.get_time(), 
                                                    actual_header.get_date(), file_scope)
            
            error_message = f"File head error: scope inconsistency between name and header in file '{file_name}'."
            assert expected_header_from_file_name == actual_header, error_message
    
    except AssertionError as error_message:
        print(error_message)
    
    else:
        doctors_collection = DoctorsCollection(doctors_file)
        mothers_collection = MothersCollection(requests_file)
        schedule = Schedule(schedule_file)

        next_schedule, next_doctors = schedule.create_next_schedule(doctors_collection, mothers_collection)
        next_schedule.set_file_name(schedule.create_file_name())
        next_schedule.set_header(schedule.create_header())
        next_schedule.write_file()

        next_doctors_collection = DoctorsCollection(doctors = next_doctors.get_doctors())
        next_doctors_collection.set_file_name(doctors_collection.create_file_name())
        next_doctors_collection.set_header(doctors_collection.create_header())
        next_doctors_collection.write_file()
        
plan(argv[DOCTORS_FILE_INDEX], argv[SCHEDULE_FILE_INDEX], argv[REQUESTS_FILE_INDEX])