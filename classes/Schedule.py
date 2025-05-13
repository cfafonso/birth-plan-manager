#-*- coding: utf-8 -*-


from classes.Time import Time
from classes.Mother import Mother
from classes.Doctor import Doctor
from classes.Assistance import Assistance
from classes.DataManager import DataManager

from copy import deepcopy


class Schedule(DataManager):
    """
    A class to represent a collection of Assistance objects.
    """

    def __init__(self, file_name = None, header = None, schedule = []):
        """
        Initializes a new Schedule.

        Args:
            file_name (str, optional): the name of the file associated with the collection. Defaults to None.
            header (Header, optional): the Header object associated with the collection. Defaults to None.
            schedule (list, optional): the list of Assistance objects associated with the collection. Defaults to an empty list.
        
        Note:
            If file_name is provided and schedule is an empty list, the set_schedule() method will be called to populate
            the schedule from the file.
        """
        
        super().__init__(file_name, header)
        self._schedule = deepcopy(schedule)
         
        if self.get_file_name() and not self.get_schedule():
            self.set_schedule()


    def get_schedule(self):
        """
        A deep copy of the schedule attribute in the current Schedule instance.

        Returns:
            list: a deep copy of the list containing Assistance objects. Changes to the returned list will not affect
                  the original one.
        """

        return deepcopy(self._schedule)
    

    def set_schedule(self, schedule = []):
        """
        Sets the list of Assistance objects associated with the current Schedule instance.

        Args:
            schedule (list, optional): the list of Assistance objects associated with the current Schedule instance.
                                       Defaults to an empty list.
        """

        if schedule == []:

            in_file = super().remove_header()

            for line in in_file:
                time, mother, doctor = line.rstrip().split(", ")
                self.add_assistance(Time(time), Mother(mother), Doctor(doctor))

        else:
            self._schedule = schedule


    def schedule_items(self):
        """
        Supports iteration over the schedule attribute of the current Schedule instance.

        Yields:
            Assistance: each Assistance object in the schedule attribute, one at a time.
        """
        
        for assistance in self._schedule:
            yield assistance


    def create_next_schedule(self, doctors_collection, mothers_collection):
        """
        Creates the schedule attribute of the next Schedule instance according to the criteria defined in the 
        specification of the birth-plan-manager tool.
        
        Args:
            doctors_collection (DoctorsCollection): the list of Doctor objects associated with the current collection.
            mothers_collection (MothersCollection): the list of Mother objects associated with the current collection.

        Returns:
            next_schedule (list): the list of Assistance objects associated with the next collection.
        """

        doctors = deepcopy(doctors_collection)
        mothers = deepcopy(mothers_collection)
        
        mothers.sort_mothers()

        next_schedule = Schedule()
        next_time = Time(doctors.retrieve_next_time())
        
        doctors_on_leave = []
        
        for mother in mothers.mothers_items():
            doctor = self.assign_doctor(mother, doctors)

            if doctor:
                assistance_time, adjusted_availability = doctor.adjust_availability(next_time)

                if adjusted_availability.within_operating_time():
                    next_schedule.add_assistance(assistance_time, mother, doctor)
                    doctor.update_working_time(adjusted_availability)
                    doctor.daily_break_check()

                    if doctor.weekly_leave_check():
                        doctors_on_leave.append(doctor)

                else:
                    next_schedule.add_assistance(assistance_time, mother)

        doctors.add_weekly_leave()
        next_schedule.add_unassigned_requests(next_time, mothers)
        self.add_pending_assistances(next_time, next_schedule)
        next_schedule.sort_schedule()

        return next_schedule, doctors
    

    def assign_doctor(self, mother, doctors_collection):
        """
        Assigns the most appropriate doctor to a mother, according to the criteria defined in the specification
        of the birth-plan-manager tool.

        Args:
            mother (Mother): the mother that needs an assistance.
            doctors_collection (DoctorsCollection): the collection of available doctors.
        
        Returns:
            Doctor: the selected doctor for an assistance to a given mother or None if no doctor is available.
        """

        if mother.get_risk() == "high":
            return doctors_collection.select_doctor(min_category=True)
        else:
            return doctors_collection.select_doctor()
    

    def add_assistance(self, time, mother, doctor=None):
        """
        Creates an Assistance object with Time, Mother and Doctor objects, and adds it to the collection of the
        current Schedule instance.

        Requires:
            time (Time): the time of an Assistance.
            mother (Mother): the mother of an Assistance.
            doctor (Doctor, optional): the doctor of an Assistance. Defaults to None.
        """

        if doctor:
            self._schedule.append(Assistance(time, mother, doctor))
        else:
            self._schedule.append(Assistance(time, mother))
        

    def add_unassigned_requests(self, next_time, mothers_collection):
        """
        Retrieves the requests to which it was not possible to assign any doctor and adds them to the collection
        of Assistance objects associated with the next update of the birth-plan-manager tool.
        
        Args:
            next_time (Time): the time of the next update of the birth-plan-manager tool.
            mothers_collection (MothersCollection): the collection of mothers that need an assistance.
        """

        scheduled_mothers = [assistance.get_mother() for assistance in self.schedule_items()]
        
        for mother in mothers_collection.mothers_items():
            if mother not in scheduled_mothers:
                self.add_assistance(next_time, mother)
        

    def add_pending_assistances(self, next_time, next_schedule):
        """
        Retrieves the assistances that are yet to be carried out at the current Schedule instance and adds them
        to the collection of Assistance objects associated with the next update of the birth-plan-manager tool.
        
        Args:
            next_schedule (list): the list of Assistance objects associated with the Schedule instance at the 
                                  next update of the birth-plan-manager tool.
        """
                
        for assistance in self.schedule_items():
            if not assistance.get_time() < next_time:
                next_schedule.add_assistance(assistance.get_time(), assistance.get_mother(), assistance.get_doctor())
        
        
    def sort_schedule(self):
        """
        Sorts the assistances in the current Schedule instance, according to the criteria defined in the specification
        of the birth-plan-manager tool.
        """

        self._schedule.sort()


    def __lt__(self, other_schedule):
        """
        Compares the current Schedule instance and another one according to the length of their schedule attribute.

        Args:
            other_schedule (Schedule): another instance of the Schedule class.

        Returns:
            bool:
                - True if the current Schedule instance has less Assistance objects than other_schedule.
                - False otherwise (including if both instances have the same number of Assistance objects).
        """

        return len(self.get_schedule()) < len(other_schedule.get_schedule())


    def __eq__(self, other_schedule):
        """
        Checks the equality between the current Schedule instance and another one according to their schedule
        attribute.

        Args:
            other_schedule (Schedule): another instance of the Schedule instance.

        Returns:
            bool:
                - True if both instances have the same Assistance objects in their schedule attribute.
                - False otherwise.
        """

        if len(self.get_schedule()) != len(other_schedule.get_schedule()):
            return False
        
        return all(x == y for x, y in zip(sorted(self.get_schedule()), 
                                          sorted(other_schedule.get_schedule())))


    def __str__(self):
        """
        The string representation of the current Schedule instance.

        Returns:
            str: the current Schedule instance as a string.

        Example:
            >>> str(schedule)
            "Organization:
             SmartMaternityCare
             Time:
             10h00
             Date:
             10:12:2023
             Schedule:
             9h50, Mary Evans, Brian Cooper
             10h10, Emily Fletcher, Brian Cooper
             10h45, Faith Morrison, Andrew Davies"
        """
            
        return super().__str__() + '\n' + '\n'.join(str(assistance) for assistance in self.schedule_items())