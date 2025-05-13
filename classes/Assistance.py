#-*- coding: utf-8 -*-


from constants import REDIRECTED_REQUEST


class Assistance:
    """
    A class to represent an assistance.
    """

    def __init__(self, time, mother, doctor=None):
        """
        Initializes a new Assistance.

        Args:
            time (Time): the time of an assistance.
            mother (Mother): the mother of an assistance.
            doctor (Doctor, optional): the doctor of an assistance. Defaults to None.
        """
        
        self._time = time
        self._mother = mother
        self._doctor = doctor

    
    def get_time(self):
        """
        The time of the current Assistance instance.

        Returns:
            Time: the time for the current Assistance instance.
        """

        return self._time
    

    def set_time(self, time):
        """
        Sets the time of the current Assistance instance.

        Args:
            time (Time): the time to set for the current Assistance instance.
        """

        self._time = time
    

    def get_mother(self):
        """
        The mother of the current Assistance instance.
        
        Returns:
            Mother: the mother for the current Assistance instance.
        """

        return self._mother
    
    
    def set_mother(self, mother):
        """
        Sets the mother of the current Assistance instance.
        
        Args:
            mother (Mother): the mother to set for the current Assistance instance.
        """

        self._mother = mother

    
    def get_doctor(self):
        """
        The doctor of the current Assistance instance.

        Returns:
            Doctor: the doctor for the current Assistance instance.
        """

        return self._doctor
    

    def set_doctor(self, doctor):
        """
        Sets the doctor of the current Assistance instance.

        Args:
            doctor (Doctor): the doctor to set for the current Assistance instance.
        """

        self._doctor = doctor
       

    def __lt__(self, other_assistance):
        """
        Compares the current Assistance instance and another one, according to the criteria defined in the specification
        of the birth-plan-manager tool (first by time, then by mothers' names arranged in alphabetical order).

        Args:
            other_assistance (Assistance): another instance of the Assistance class.
        
        Returns:
            bool:
                - True if the current Assistance instance should be ordered before other_assistance.
                - False otherwise.
        """

        if self.get_time().get_time_delta() < other_assistance.get_time().get_time_delta():
            return True
        
        elif self.get_time().get_time_delta() > other_assistance.get_time().get_time_delta():
            return False
        
        if self.get_mother().get_name() < other_assistance.get_mother().get_name():
            return True
        
        elif self.get_mother().get_name() > other_assistance.get_mother().get_name():
            return False

        return False


    def __eq__(self, other_assistance):
        """
        Checks the equality between the current Assistance instance and another one.

        Args:
            other_assistance (Assistance): another instance of the Assistance class.
        
        Returns:
            bool:
                - True if all attributes of both instances are equal.
                - False otherwise.
        """
        
        if self.get_doctor() and other_assistance.get_doctor():
            return self.get_time() == other_assistance.get_time() and self.get_mother() == other_assistance.get_mother() and \
                self.get_doctor() == other_assistance.get_doctor()
        else:
            return False


    def __str__(self):
        """
        The string representation of the current Assistance instance.

        Returns:
            str: the current Assistance instance as a string.

        Example:
            If the assistance has a doctor associated to it:
            >>> str(assistance)
            "9h50, Mary Evans, Brian Cooper"

            If the assistance does not have a doctor associated to it:
            >>> str(assistance)
            "16h30, Susan Taylor, redirected to other network"
        """

        if self.get_doctor():
            return f"{self.get_time().get_time_string()}, {self.get_mother().get_name()}, {self.get_doctor().get_name()}"
        else:
            return f"{self.get_time().get_time_string()}, {self.get_mother().get_name()}, {REDIRECTED_REQUEST}"