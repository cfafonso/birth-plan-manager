#-*- coding: utf-8 -*-


from classes.Header import Header
from classes.Time import Time

from constants import NUM_HEADER_LINES, FILE_TIME_INCREMENT
from constants import DOCTORS_FILE_INDEX, SCHEDULE_FILE_INDEX, REQUESTS_FILE_INDEX
from constants import DOCTORS_FILE_SCOPE, SCHEDULE_FILE_SCOPE, REQUESTS_FILE_SCOPE


class DataManager:
    """
    A class that provides mechanisms to read and write data from or to files of the birth-plan-manager tool.
    """
    
    def __init__(self, file_name = None, header = None):
        """
        Initializes a new DataManager.

        Args:
            file_name (str, optional): the name of the .txt file. Defaults to None.
            header (Header, optional): the header of .txt file. Defaults to None.

        Note:
            If file_name is provided but header is not, the create_header_from_file_name() method will be called
            to populate the header from the file.
        """

        self._file_name = file_name
        self._header = header
  
        if self.get_file_name() and not self.get_header():
            self.create_header_from_file_name()
        

    def get_file_name(self):
        """
        The file name of the current DataManager instance.

        Returns:
            str: the name of the file of the current DataManager instance.
        """
        
        return self._file_name
    
    
    def set_file_name(self, file_name):
        """
        Set the file name of the current DataManager instance.

        Args:
            file_name (str): the name of the file to set for the current DataManager instance.
        """
            
        self._file_name = file_name
    
    
    def get_header(self):
        """
        The header of the current DataManager instance.

        Returns:
            Header: the header of the current DataManager instance.
        """
        
        return self._header
    

    def set_header(self, header):
        """
        Set the header of the current DataManager instance.

        Args:
            header (Header): the header to set for the current DataManager instance.
        """

        self._header = header

    
    def create_header_from_file_name(self):
        """
        Creates the Header object of the current DataManager instance from its file_name attribute.
        """

        header = []

        lines = self.open_file().readlines()
            
        for i, line in enumerate(lines, start=1):
            if i in range(2, NUM_HEADER_LINES, 2):
                header.append(line.rstrip())

            if i == NUM_HEADER_LINES:
                header.append(line.rstrip().rstrip(":"))
            
        organization, hour, date, scope = header

        self.set_header(Header(organization, hour, date, scope))


    def retrieve_next_time(self):
        """
        Retrieves the next update time of of the birth-plan-manager tool for the current DataManager instance.

        Returns:
            str: the time of the next update time of of the birth-plan-manager tool for the current DataManager instance.
        """

        next_time = Time(self.get_header().get_time())
        next_time.update_time(FILE_TIME_INCREMENT)

        return next_time.get_time_string()


    def open_file(self):
        """
        Opens the .txt file associated with the current DataManager instance.

        Returns:
            file: an open file object (in read mode with UTF-8 encoding) associated with the current DataManager instance.
        """

        return open(self.get_file_name(), "r", encoding = "utf-8")
    
    
    def remove_header(self):
        """
        Reads the .txt file associated with the current DataManager instance, skipping the header lines.

        Returns:
            list: a list of strings, each representing a line of content from the .txt file associated with the
                  current DataManager instance, with the header lines removed.
        """
        
        lines = self.open_file().readlines()
        content = []
        
        for i, line in enumerate(lines, start=1):
            if i > NUM_HEADER_LINES:
                content.append(line)
                
        return content
    

    def retrieve_file_scope(self, file_position):
        """
        Maps the scope of a file according to its specific position index when running the birth-plan-manager tool.

        Args:
            file_position (int): the index representing a file position, expected to be one of DOCTORS_FILE_INDEX, 
                                 SCHEDULE_FILE_INDEX, or REQUESTS_FILE_INDEX.

        Returns:
            str or None: the scope associated with the given file position, or None if the file position is not
                         found in the mapping.
        """

        file_scopes = {DOCTORS_FILE_INDEX: DOCTORS_FILE_SCOPE,
                       SCHEDULE_FILE_INDEX: SCHEDULE_FILE_SCOPE,
                       REQUESTS_FILE_INDEX: REQUESTS_FILE_SCOPE}

        return file_scopes.get(file_position)


    def create_file_name(self):
        """
        Creates the file name associated with the next DataManager instance, according to the file name and header
        of the current DataManager instance.

        Returns:
            str: the file name without the .txt extension to initialize the DataManager instance at the next
                 update of the birth-plan-manager tool.
        """
        
        scope = self.get_header().get_scope().lower()
        next_time = self.retrieve_next_time()
        new_file_name = "".join((scope, next_time))

        return new_file_name


    def create_header(self):
        """
        Creates the header associated with the next DataManager instance, according to the header of the current 
        DataManager instance and the next update time of the birth-plan-manager tool.

        Returns:
            Header: the Header object to initialize the DataManager instance at the next update of the
                    birth-plan-manager tool.
        """

        organization = self.get_header().get_organization()
        time = Time(self.get_header().get_time())
        time.update_time(FILE_TIME_INCREMENT)
        date = self.get_header().get_date()
        scope = self.get_header().get_scope()
        
        return Header(organization, time.get_time_string(), date, scope)
    

    def write_file(self):
        """
        Writes the current DataManager instance to a .txt file, according to the specifications of the 
        birth-plan-manager tool.
        """

        next_time = Time(self.retrieve_next_time())

        if next_time.within_operating_time():
            
            lines = str(self).split('\n')
            in_file = open("".join((lines[1], ".txt")), "w", encoding="utf-8-sig")
            in_file.write('\n'.join(lines[2:]))
            in_file.close()
        

    def __lt__(self, other_data_manager):
        """
        Compares the current DataManager instance and another one according to their file names and headers.

        Comparison order:
        1. If both DataManager instances have headers: the DataManager instance with the earliest time comes first.
        2. If the headers of both instances have the same time and both instances have file names: the DataManager
        instance with the file name that comes first alphabetically takes precedence.
        
        Args:
            other_data_manager (DataManager): another instance of the DataManager class.
        
        Returns:
            bool:
                - True if the current DataManager instance should be ordered before other_data_manager.
                - False otherwise.
        """

        if self.get_header() and other_data_manager.get_header():
            if self.get_header() < other_data_manager.get_header():
                return True
            elif self.get_header() > other_data_manager.get_header():
                return False

        if self.get_file_name() and other_data_manager.get_file_name():
            if self.get_file_name() < other_data_manager.get_file_name():
                return True
            elif self.get_file_name() > other_data_manager.get_file_name():
                return False

        return False
    
    
    def __eq__(self, other_data_manager):
        """
        Checks the equality between the current DataManager instance and another one.

        Args:
            other_data_manager (DataManager): another instance of the DataManager instance.
        
        Returns:
            bool:
                - True if all attributes of both instances are equal.
                - False otherwise.
        """

        if self.get_file_name() and self.get_header() and other_data_manager.get_file_name() and \
            other_data_manager.get_header():
            return self.get_file_name() == other_data_manager.get_file_name() and \
                self.get_header() == other_data_manager.get_header()
        else:
            return False


    def __str__(self):
        """
        The string representation of the current DataManager instance.

        Returns:
            str: the current DataManager instance as a string.

        Example:
            >>> str(datamanager)
            "Filename:
             doctors10h00.txt
             Organization:
             SmartMaternityCare
             Time:
             10h00
             Date:
             10:12:2023
             Doctors:"
            """
        
        return f"Filename:\n{self.get_file_name()}\n{self.get_header()}"