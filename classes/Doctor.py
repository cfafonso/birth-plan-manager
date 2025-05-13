#-*- coding: utf-8 -*-


from classes.Time import Time

from constants import MAX_WORK_TIME, DAILY_BREAK, ASSISTANCE_DURATION


class Doctor:
    """
    A class to represent a doctor.
    """
    
    def __init__(self, name, category = None, availability = None, minutes_today = None, weekly_time = None):
        """
        Initializes a new Doctor.

        Args:
            name (str): the name of a doctor.
            category (str, optional): the category of a doctor. Defaults to None.
            availability (str, optional): the availability of a doctor. Defaults to None.
            minutes_today (str, optional): the work minutes accumulated in a day. Defaults to None.
            weekly_time (str, optional): the work time accumulated in a week. Defaults to None.
        """

        self._name = name
        self._category = category
        self._availability = availability
        self._minutes_today = minutes_today
        self._weekly_time = weekly_time


    def get_name(self):
        """
        The name of the current Doctor instance.

        Returns:
            str: the name of the current Doctor instance.
        """
        
        return self._name
    

    def set_name(self, name):
        """
        Sets the name of the current Doctor instance.

        Args:
            name (str): the name to set for the current Doctor instance.
        """
        
        self._name = name
    

    def get_category(self):
        """
        The category of the current Doctor instance.

        Returns:
            str: the category of the current Doctor instance.
        """
        
        return self._category
    

    def set_category(self, category):
        """
        Sets the category of the current Doctor instance.

        Args:
            category (str): the category to set for the current Doctor instance.
        """
        
        self._category = category

        
    def get_availability(self):
        """
        The availability of the current Doctor instance.

        Returns:
            str: the availability of the current Doctor instance.
        """
        
        return self._availability
    

    def set_availability(self, availability):
        """
        Sets the availability of the current Doctor instance.
        
        Args:
            availability (str): the availability to set for the current Doctor instance.
        """
        
        self._availability = availability
    

    def get_minutes_today(self):
        """
        The accumulated work minutes in a day of the current Doctor instance.

        Returns:
            str: the work minutes of the current Doctor instance.
        """
        
        return self._minutes_today
    

    def set_minutes_today(self, minutes_today):
        """
        Sets the accumulated work minutes in a day for the current Doctor instance.
        
        Args:
            minutes_today (str): the accumulated work minutes in a day to set for the current Doctor instance.
        """
        
        self._minutes_today = minutes_today
    

    def get_weekly_time(self):
        """
        The accumulated hours and minutes since the last weekly rest of the current Doctor instance.

        Returns:
            str: the accumulated hours and minutes since the last weekly rest of the current Doctor instance.
        """
        
        return self._weekly_time
    

    def set_weekly_time(self, weekly_time):
        """
        Sets the accumulated working time since the last weekly rest for the current Doctor instance.
        
        Args:
            weekly_time (str): the accumulated working time since the last weekly rest to set for the current Doctor
                               instance.
        """
        
        self._weekly_time = weekly_time
    

    def weekly_leave_check(self):
        """
        Checks whether the current Doctor instance has reached its maximum allowed weekly working time.

        Returns:
            bool:
                - True if the current Doctor instance has reached the maximum weekly work time.
                - False otherwise.
        """

        weekly_time_object = Time(self.get_weekly_time()).get_time_delta()
        max_weekly_time_object = Time(MAX_WORK_TIME).get_time_delta()

        return weekly_time_object >= max_weekly_time_object
            

    def daily_break_check(self):
        """
        Checks whether the current Doctor instance has reached its maximum daily working time for the first time
        without taking a break and, if so, increments its availability by 1 hour.

        Note:
            The availability of the current Doctor instance is incremented by 1 hour if the condition is met.
        """

        daily_work_minutes = int(self.get_minutes_today())
        
        if 240 <= daily_work_minutes <260:
            availability = Time(self.get_availability())
            availability.update_time(DAILY_BREAK)
            self.set_availability(availability.get_time_string())    
    

    def adjust_availability(self, next_time):
        """
        Adjusts the availability of the current Doctor instance, according to the next update of the birth-plan-manager
        tool and the duration of an assistance.

        Args:
            next_time (Time): the time of the next update of the birth-plan-manager tool.
        
        Returns:
            tuple:
                - assistance_time (Time): the time of an asistance.
                - adjusted_availability (Time): the adjusted availability of the doctor carrying out the assistance.
        """

        availability = Time(self.get_availability())

        if availability.get_time_delta() < next_time.get_time_delta():
            assistance_time = Time(next_time.get_time_string())
            adjusted_availability = Time(next_time.get_time_string())
            adjusted_availability.update_time(ASSISTANCE_DURATION)
        else:
            assistance_time = Time(availability.get_time_string())
            adjusted_availability = Time(self.get_availability())
            adjusted_availability.update_time(ASSISTANCE_DURATION)
        
        return assistance_time, adjusted_availability
    

    def update_working_time(self, adjusted_availability):
        """
        Updates the availability, minutes_today and weekly_time attributes of a Doctor instance to whom an
        assistance has been assigned to.

        Args:
            adjusted_availability (Time): the newly calculated availability time for the Doctor instance, adjusted according
                                          to the assistance duration and the next update of the birth-plan-manager tool.
        
        Note:
            The current Doctor instance is updated with regards to its availability, minutes_today and weekly_time attributes.
        """

        self.set_availability(adjusted_availability.get_time_string())

        new_minutes_today = int(self.get_minutes_today()) + Time(ASSISTANCE_DURATION).convert_minutes_to_int()
        self.set_minutes_today(str(new_minutes_today))

        weekly_time = Time(self.get_weekly_time())
        weekly_time.update_time(ASSISTANCE_DURATION) 
        self.set_weekly_time(weekly_time.get_time_string())


    def __lt__(self, other_doctor):
        """
        Compares the current Doctor instance and another one, according to the priority criteria defined in the
        specification of the birth-plan-manager tool.
         
        Comparison order:
        1. availability
        2. category
        3. minutes_today
        4. weekly_time
        5. name

        Args:
            other_doctor (Doctor): another instance of the Doctor class.
        
        Returns:
            bool:
                - True if the current Doctor instance should be ordered before other_doctor for an assistance.
                - False otherwise (including if equal on all criteria).
        """

        if self.get_name() and self.get_category() and self.get_availability() and self.get_minutes_today() and \
            self.get_weekly_time() and other_doctor.get_name() and other_doctor.get_category() and \
                other_doctor.get_availability() and other_doctor.get_minutes_today() and other_doctor.get_weekly_time():

            if Time(self.get_availability()).get_time_delta() < Time(other_doctor.get_availability()).get_time_delta():
                return True
            elif Time(self.get_availability()).get_time_delta() > Time(other_doctor.get_availability()).get_time_delta():
                return False
            
            if int(self.get_category()) < int(other_doctor.get_category()):
                return False
            elif int(self.get_category()) > int(other_doctor.get_category()):
                return True

            if int(self.get_minutes_today()) < int(other_doctor.get_minutes_today()):
                return True
            elif int(self.get_minutes_today()) > int(other_doctor.get_minutes_today()):
                return False
            
            if Time(self.get_weekly_time()).get_time_delta() < Time(other_doctor.get_weekly_time()).get_time_delta():
                return True
            elif Time(self.get_weekly_time()).get_time_delta() > Time(other_doctor.get_weekly_time()).get_time_delta():
                return False
            
            if self.get_name() < other_doctor.get_name():
                return True
            
            return False

        else:
            if self.get_name() < other_doctor.get_name():
                return True

            return False
        

    def __eq__(self, other_doctor):
        """
        Checks the equality between the current Doctor instance and another one.

        Args:
            other_doctor (Doctor): another instance of the Doctor class.
        
        Returns:
            bool:
                - True if all attributes of both instances are defined and equal or if only the name attribute of both
                instances is defined and equal.
                - False otherwise.
        """
        
        if self.get_name() and self.get_category() and self.get_availability() and self.get_minutes_today() and \
            self.get_weekly_time() and other_doctor.get_name() and other_doctor.get_category() and \
                other_doctor.get_availability() and other_doctor.get_minutes_today() and other_doctor.get_weekly_time():

            return self.get_name() == other_doctor.get_name() and \
                self.get_category() == other_doctor.get_category() and \
                self.get_availability() == other_doctor.get_availability() and \
                self.get_minutes_today() == other_doctor.get_minutes_today() and \
                self.get_weekly_time() == other_doctor.get_weekly_time()
        
        else:
            if self.get_name() and not (self.get_category() or self.get_availability() or self.get_minutes_today() or \
            self.get_weekly_time()) and other_doctor.get_name() and not (other_doctor.get_category() or \
                other_doctor.get_availability() or other_doctor.get_minutes_today() or other_doctor.get_weekly_time()):
                
                return self.get_name() == other_doctor.get_name()
            
            return False


    def __str__(self):
        """
        The string representation of the current Doctor instance.

        Returns:
            str: the current Doctor instance as a string.
        
        Example:
            If all attributes are defined:
                >>> str(doctor)
                "Andrew Davies, 1, 11h05, 180, 28h00"
            
            If only the name attribute is defined (with other attributes set to None):
                >>> str(doctor)
                "Andrew Davies"
        """

        if self.get_name() and self.get_category() and self.get_availability() and self.get_minutes_today() \
            and self.get_weekly_time():
            return f"{self.get_name()}, {self.get_category()}, {self.get_availability()}, {self.get_minutes_today()}, " \
                f"{self.get_weekly_time()}"

        else:
            return f"{self.get_name()}"