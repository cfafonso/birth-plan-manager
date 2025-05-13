#-*- coding: utf-8 -*-


from classes.Doctor import Doctor
from classes.DataManager import DataManager

from copy import deepcopy
from constants import WKL_LEAVE, MIN_CATEG


class DoctorsCollection(DataManager):
    """
    A class to represent a collection of Doctor objects.
    """

    def __init__(self, file_name = None, header = None, doctors = []):
        """
        Initializes a new DoctorsCollection.
        
        Args:
            file_name (str, optional): the name of the file associated with the collection. Defaults to None.
            header (Header, optional): the Header object associated with the collection. Defaults to None.
            doctors (list, optional): the list of Doctor objects associated with the collection. Defaults to an empty list.
        
        Note:
            If file_name is provided and doctors is an empty list, the set_doctors() method will be called to populate the
            doctors from the file.
        """
        
        super().__init__(file_name, header)
        self._doctors = deepcopy(doctors)
        
        if self.get_file_name() and not self.get_doctors():
            self.set_doctors()

    
    def get_doctors(self):
        """
        A deep copy of the doctors attribute in the current DoctorsCollection instance.

        Returns:
            list: a deep copy of the list containing Doctor objects. Changes to the returned list will not affect the
                  original one.
        """

        return deepcopy(self._doctors)
    

    def set_doctors(self, doctors = []):
        """
        Sets the list of Doctor objects associated with the current DoctorsCollection instance.

        Args:
            doctors (list, optional): the list of Doctor objects associated with the current DoctorsCollection instance.
                                      Defaults to an empty list.
        """

        if doctors == []:

            in_file = super().remove_header()
                        
            for line in in_file:
                name, category, availability, accumulated_work_minutes, weekly_work_time = line.rstrip().split(", ")                
                self._doctors.append(Doctor(name, category, availability, accumulated_work_minutes, weekly_work_time))

        else:
            self._doctors = doctors


    def doctors_items(self):
        """
        Supports iteration over the doctors attribute of the current DoctorsCollection instance.

        Yields:
            Doctor: each Doctor object in the doctors attribute, one at a time.
        """

        for doctor in self._doctors:
            yield doctor


    def sort_doctors(self):
        """
        Sorts the doctors in the current DoctorsCollection instance, who are not on weekly leave, from highest to
        lowest availability, according to the criteria defined in the specification of the birth-plan-manager tool.
        
        Returns:
            list: a new list of sorted Doctor objects who are available for an assistance.
        """

        doctors_to_sort = []

        for doctor in self.doctors_items():
            if not doctor.weekly_leave_check():
                doctors_to_sort.append(doctor)

        return sorted(doctors_to_sort)

    
    def select_doctor(self, min_category=False):
        """
        Selects the doctor for an assistance according to the specifications of the birth-plan-manager tool.

        This method finds the most appropriate doctor who:
        1. Has a category of at least 2 for high-risk mothers.
        2. Is not on weekly leave.

        Returns:
            Doctor: the selected doctor for an assistance.
            None: if no doctor is available that satisfies the criteria.
        """

        for doctor in self.sort_doctors():
            
            if min_category:
                category_check = int(doctor.get_category()) >= MIN_CATEG
                if category_check:
                    return doctor
                
            else:
                return doctor

        return None
    

    def add_weekly_leave(self):
        """
        Checks whether each Doctor object in the doctors list of the current DoctorsCollection instance has reached the
        maximum allowed value for their weekly_time attribute and, if so, updates their availability to 'weekly leave'.
        """

        for doctor in self.doctors_items():
            if doctor.weekly_leave_check():
                doctor.set_availability(WKL_LEAVE)


    def __lt__(self, other_doctors_collection):
        """
        Compares the current DoctorsCollection instance and another one according to the length of their
        doctors attribute.

        Args:
            other_doctors_collection (DoctorsCollection): another instance of the DoctorsCollection class.

        Returns:
            bool:
                - True if the current DoctorsCollection instance has less Doctor objects than other_doctors_collection.
                - False otherwise.
        """

        return len(self.get_doctors()) < len(other_doctors_collection.get_doctors())


    def __eq__(self, other_doctors_collection):
        """
        Checks the equality between the current DoctorsCollection instance and another one according to the their
        doctors attribute.

        Args:
            other_doctors_collection (DoctorsCollection): another instance of the DoctorsCollection class.
        
        Returns:
            bool:
                - True if both instances have the same Doctor objects in their doctors attribute.
                - False otherwise.
        """

        if len(self.get_doctors()) != len(other_doctors_collection.get_doctors()):
            return False
        
        return all(x == y for x, y in zip(sorted(self.get_doctors()), 
                                          sorted(other_doctors_collection.get_doctors())))


    def __str__(self):
        """
        The string representation of the current DoctorsCollection instance.

        Returns:
            str: the current DoctorsCollection instance as a string.

        Example:
            >>> str(doctorscollection)
            "Filename:
             doctors10h00.txt,
             Organization:
             SmartMaternityCare
             Time:
             10h00
             Date:
             10:12:2023
             Doctors:
             Andrew Davies, 1, 11h05, 180, 28h00
             Brian Cooper, 3, 10h30, 80, 7h20
             Charles Baker, 2, 10h35, 220, 32h00
             David Adams, 3, 10h40, 270, 15h00"
        """

        return super().__str__() + '\n' + '\n'.join(str(doctor) for doctor in self.get_doctors())