#-*- coding: utf-8 -*-


from classes.Time import Time

from datetime import datetime


class Header:
    """
    A class to represent a header.
    """
    
    def __init__(self, organization, time, date, scope):
        """
        Initializes a new Header.

        Args:
            organization (str): the organization associated with the header.
            time (str): the time of the header.
            date (str): the date of the header in the format '%d:%m:%Y'.
            scope (str): the scope of the header.
        """

        self._organization = organization
        self._time = time
        self._date = date
        self._scope = scope
    

    def get_organization(self):
        """
        The name of the organization associated with the current Header instance.

        Returns:
            str: the name of the organization associated with the current Header instance.
        """

        return self._organization
    

    def set_organization(self, organization):
        """
        Sets the name of the organization associated with the current Header instance.

        Args:
            organization (str): the name of the organization to set for the current Header instance.
        """

        self._organization = organization
    

    def get_time(self):
        """
        The time of the current Header instance.

        Returns:
            str: the time of the current Header instance.
        """
        
        return self._time
    

    def set_time(self, time):
        """
        Sets the time of the current Header instance.

        Args:
            time (str): the time of the current Header instance.
        """
        
        self._time = time
    

    def get_date(self):
        """
        The date of the current Header instance.

        Returns:
            str: the date of the current Header instance.
        """

        return self._date
    

    def set_date(self, date):
        """
        Sets the date of the current Header instance.

        Args:
            date (str): the date of the current Header instance.
        """
        
        self._date = date
    

    def get_scope(self):
        """
        The scope of the current Header instance.

        Returns:
            str: the scope of the current Header instance.
        """
        
        return self._scope

    
    def set_scope(self, scope):
        """
        Sets the scope of the current Header instance.

        Args:
            scope (str): the scope of the current Header instance.
        """
        
        self._scope = scope
    
        
    def __lt__(self, other_header):
        """
        Compares the current Header instance and another one, according to their date and time attributes.

        Comparison order:
        - If both Header instances have the same date: the Header instance with the earlier time comes first.
        - If both Header instances have different dates: the Header instance with the earlier date comes first.

        Args:
            other_header (Header): another instance of the Header class.
        
        Returns:
            bool:
                - True if the current Header should be ordered before other_header.
                - False otherwise.
        """
        
        if self.get_date() == other_header.get_date():
            return Time(self.get_time()) < Time(other_header.get_time())

        return datetime.strptime(self.get_date(), '%d:%m:%Y').date() < \
                datetime.strptime(other_header.get_date(), '%d:%m:%Y').date()


    def __eq__(self, other_header):
        """
        Checks the equality between the current Header instance and another one.

        Args:
            other_header (Header): another instance of the Header class.
        
        Returns:
            bool:
                - True if all attributes of both instances are equal.
                - False otherwise.
        """

        return self.get_organization() == other_header.get_organization() and \
               self.get_time() == other_header.get_time() and \
               self.get_date() == other_header.get_date() and \
               self.get_scope() == other_header.get_scope()
    

    def __str__(self):
        """
        The string representation of the current Header instance.

        Returns:
            str: the current Header instance as a string.
        
        Example:
            >>> str(header)
            "Organization:
             SmartMaternityCare
             Time:
             10h00
             Date:
             10:12:2023
             Doctors:"
        """

        return f"Organization:\n{self.get_organization()}\nTime:\n{self.get_time()}\nDate:\n{self.get_date()}\n{self.get_scope()}:"