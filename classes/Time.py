#-*- coding: utf-8 -*-


from datetime import timedelta

from constants import CLOSING_TIME, OPENING_TIME


class Time:
    """
    A class to represent a time.
    """
    
    def __init__(self, time_string = None, time_delta = None, hours = None, minutes = None):
        """
        Initializes a new Time.

        Args:
            time_string (str, optional): time as a string with the format "HhM". Defaults to None.
            time_delta (datetime.timedelta, optional): time as a timedelta object. Defaults to None.
            hours (int, optional): hours component of the time. Defaults to None.
            minutes (int, optional): minutes component of the time. Defaults to None.

        Note:
        The constructor follows a priority order when initializing the instance:
        1. If time_string is provided: this is used as the primary representation (with time_delta, hours and minutes
        derived from it).
        2. Else if the time_delta is provided: this is used as the primary representation (with time_string, hours and 
        minutes derived from it).
        3. Else if hours and minutes are provided: this is used as the primary representation (with time_string and 
        time_delta derived from it).
        """
        
        self._time_string = time_string
        self._time_delta = time_delta
        self._hours = hours
        self._minutes = minutes

        if self.get_time_string():
            self.convert_string_to_time_delta()
            self.convert_string_to_time()
            
        elif self.get_time_delta():
            self.convert_time_delta_to_time()
            self.convert_time_to_string()
        
        elif self.get_hours() and self.get_minutes():
            self.convert_time_to_string()
            self.convert_string_to_time_delta()
 
    
    def get_time_string(self):
        """
        The string representation with the format "HhM" of the current Time instance.

        Returns:
            str: the string representation with the format "HhM" of the current Time instance.
        """
        
        return self._time_string
        

    def set_time_string(self, time_string):
        """
        Sets the string representation of the current Time instance.
        
        Args:
            time_string (str): the string representation with the format "HhM" to set for the current Time instance.
        """
        
        self._time_string = time_string
    

    def get_time_delta(self):
        """
        The datetime.timedelta object of the current Time instance.

        Returns:
            datetime.timedelta: the timedelta object of the current Time instance.
        """
        
        return self._time_delta
    

    def set_time_delta(self, time_delta):
        """
        Sets the datetime.timedelta object of the current Time instance.

        Args:
            time_delta (datetime.timedelta): the datetime.timedelta object to set for the current Time instance.
        """
        
        self._time_delta = time_delta
    

    def get_hours(self):
        """
        The hours of the current Time instance.

        Returns:
            int: the hours of the current Time instance.
        """
        
        return self._hours
    

    def set_hours(self, hours):
        """
        Sets the hours of the current Time instance.
        
        Args:
            hours (int): the hours to set for the current Time instance.
        """
        
        self._hours = hours
    

    def get_minutes(self):
        """
        The minutes of the current Time instance.

        Returns:
            int: the minutes of the current Time instance.
        """
        
        return self._minutes
    

    def set_minutes(self, minutes):
        """
        Sets the minutes of the current Time instance.

        Args:
            minutes (int): the minutes to set for the current Time instance.
        """
        
        self._minutes = minutes
    

    def convert_string_to_time_delta(self):
        """
        Uses the time_string attribute of the current Time instance to set its time_delta attribute.
        """
        
        hours, minutes = self.get_time_string().split("h")
        self.set_time_delta(timedelta(hours=int(hours), minutes=int(minutes)))

        
    def convert_time_delta_to_time(self):
        """
        Uses the time_delta attribute of the current Time instance to set its hours and minutes attributes.
        """
        
        self.set_hours(int(self.get_time_delta().total_seconds() // 3600))
        self.set_minutes(int(self.get_time_delta().total_seconds() // 60 % 60))
        
    
    def convert_string_to_time(self):
        """
        Uses the time_string attribute of the current Time instance to set its time_delta, hours and minutes 
        attributes.
        """
        
        minutes = self.convert_minutes_to_int() 
        hours = self.convert_hours_to_int() 

        self.set_time_delta(timedelta(hours=hours, minutes=minutes))

        self.set_hours(int(self.get_time_delta().total_seconds() // 3600))
        self.set_minutes(int(self.get_time_delta().total_seconds() // 60 % 60))


    def convert_hours_to_int(self):
        """
        Uses the time_string attribute of the current Time instance to retrieve the corresponding hours.

        Returns:
            int: the hours of the current Time instance.
        """

        return int(self.get_time_string().split("h")[0])


    def convert_minutes_to_int(self):
        """
        Uses the time_string attribute of the current Time instance to retrieve the corresponding minutes.

        Returns:
            int: the minutes of the current Time instance.
        """

        return int(self.get_time_string().split("h")[1])
    

    def convert_time_to_string(self):
        """
        Uses the hours and minutes attributes of the current Time instance to set its time_string attribute.
        """
        
        h = str(self.get_hours())
        m = str(self.get_minutes())
        
        if self.get_minutes() < 10:
            m = "0" + m
                
        self.set_time_string(h + "h" + m)
    
        
    def update_time(self, increment):
        """
        Updates the attributes of the current Time instance after incrementing its string representation
        with a given value.
        
        Args:
            increment (str): the string representing the time to add, in the format "HhM"
        """

        minutes = Time(increment).convert_minutes_to_int() 
        hours = Time(increment).convert_hours_to_int()   
        
        self.convert_string_to_time_delta()
        previous_time_delta = self.get_time_delta()
                
        updated_time_delta = previous_time_delta + timedelta(hours=hours, minutes=minutes)
        
        self.set_time_delta(updated_time_delta)
        self.convert_time_delta_to_time()
        self.convert_time_to_string()


    def min_operating_time_check(self):
        """
        Checks whether the current Time instance occurs after the hospital's opening time.

        Returns:
            bool:
                - True if the current Time instance occurs after the hospital's opening time.
                - False otherwise.
        """

        opening_time = Time(OPENING_TIME).get_time_delta()

        return self.get_time_delta() > opening_time


    def max_operating_time_check(self):
        """
        Checks whether the current Time instance occurs before the hospital's closing time.

        Returns:
            bool:
                - True if the current Time instance occurs before the hospital's closing time.
                - False otherwise.
        """

        closing_time = Time(CLOSING_TIME).get_time_delta() 

        return self.get_time_delta() < closing_time 


    def within_operating_time(self):
        """
        Checks whether the current Time instance occurs within the hospital's operating time.

        Returns:
            bool:
                - True if the current Time instance occurs within the hospital's operating time.
                - False otherwise.
        """

        return (self.min_operating_time_check() and self.max_operating_time_check())


    def __lt__(self, other_time):
        """
        Compares the current Time instance and another one, according to their time_delta attributes.

        Args:
            other_time (Time): another instance of the Time class.
        
        Returns:
            bool:
                - True if the current Time instance occurs before other_time.
                - False otherwise.
        """

        if self.get_time_delta() and other_time.get_time_delta():
            return self.get_time_delta() < other_time.get_time_delta()
        else:
            return False


    def __eq__(self, other_time):
        """
        Checks the equality between the current Time instance and another one, according to their time_delta
        attribute.

        Args:
            other_time (Time): another instance of the Time class.
        
        Returns:
            bool:
                - True if the time_delta attribute of both instances is equal.
                - False otherwise.
        """

        if self.get_time_delta() and other_time.get_time_delta():
            return self.get_time_delta() == other_time.get_time_delta()
        else:
            return False
        

    def __str__(self):
        """
        The string representation of the current Time instance.

        Returns:
            str: the current Time instance as a string.
        
        Example:
            >>> str(time)
            "10h00"
        """

        return f"{self.get_time_string()}"