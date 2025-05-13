#-*- coding: utf-8 -*-


class Mother:
    """
    A class to represent a mother.
    """
    
    def __init__(self, name, age = None, wristband = None, risk = None):
        """
        Initializes a new Mother.

        Args:
            name (str): the name of a mother.
            age (str, optional): the age of a mother. Defaults to None.
            wristband (str, optional): the wristband of a mother. Defaults to None.
            risk (str, optional): the risk of a mother. Defaults to None.
        """
        
        self._name = name
        self._age = age
        self._wristband = wristband
        self._risk = risk
    

    def get_name(self):
        """
        The name of the current Mother instance.

        Returns:
            str: the name of the current Mother instance.
        """
        
        return self._name
    

    def set_name(self, name):
        """
        Sets the name of the current Mother instance.

        Args:
            name (str): the name to set for the current Mother instance.
        """

        self._name = name
    

    def get_age(self):
        """
        The age of the current Mother instance.

        Returns:
            str: the age of the current Mother instance.
        """
        
        return self._age
        
    
    def set_age(self, age):
        """
        Sets the age of the current Mother instance.
        
        Args:
            age (str): the age to set for the current Mother instance.
        """
        
        self._age = age
    
    
    def get_wristband(self):
        """
        The wristband of the current Mother instance.

        Returns:
            str: the wristband of the current Mother instance.
        """

        return self._wristband
    

    def set_wristband(self, wristband):
        """
        Sets the wristband of the current Mother instance.

        Args:
            wristband (str): the wristband to set for the current Mother instance.
        """
    
        self._wristband = wristband
                
        
    def get_risk(self):
        """
        The risk of the current Mother instance.

        Returns:
            str: the risk of the current Mother instance.
        """
                
        return self._risk
    
    
    def set_risk(self, risk):
        """
        Sets the risk of the current Mother instance.
        
        Args:
            risk (str): the risk to set for the current Mother instance.
        """
        
        self._risk = risk

        
    def map_wristband(self):
        """
        Converts the string representation of the current Mother instance's wristband attribute to its corresponding
        integer value

        Returns:
            int: the integer value corresponding to the current Mother instance's wristband attribute.
        """

        wristband = {'green':0, 'yellow': 1, 'red': 2}
        
        return wristband[self.get_wristband()]
    
    
    def map_risk(self):
        """
        Converts the string representation of the current Mother instance's risk attribute to its corresponding
        integer value.

        Returns:
            int: the integer value corresponding to the current Mother instance's risk attribute.
        """
                
        risk = {'low': 0, 'medium': 1, 'high': 2}
        
        return risk[self.get_risk()]
        

    def __lt__(self, other_mother):
        """
        Compares the current Mother instance and another one, according to the priority criteria defined in the
        specification of the birth-plan-manager tool.

        Comparison order:
        - If all attributes are defined:
        1. risk
        2. wristband
        3. age
        4. name
        - If any of the optional attributes are None, compares only by name.

        Args:
            other_mother (Mother): another instance of the Mother class.
        Returns:
            bool:
                - True if the current Mother instance should be ordered before other_mother for an assistance.
                - False otherwise.
        """

        if self.get_name() and self.get_age() and self.get_wristband() and self.get_risk() and other_mother.get_name() \
            and other_mother.get_age() and other_mother.get_wristband() and other_mother.get_risk():

            if self.map_risk() < other_mother.map_risk():
                return False        
            elif self.map_risk() > other_mother.map_risk():
                return True

            if self.map_wristband() < other_mother.map_wristband():
                return False
            elif self.map_wristband() > other_mother.map_wristband():
                return True

            if int(self.get_age()) < int(other_mother.get_age()):
                return False
            elif int(self.get_age()) > int(other_mother.get_age()):
                return True

            if self.get_name() < other_mother.get_name():
                return True

            return False
        
        else:
            if self.get_name() < other_mother.get_name():
                return True

            return False


    def __eq__(self, other_mother):
        """
        Checks the equality between the current Mother instance and another one.

        Args:
            other_mother (Mother): another instance of the Mother class.
        
        Returns:
            bool:
                - True if all the attributes of both instances are defined and equal or if only the name attribute of both
                instances is defined and equal.
                - False otherwise.
        """

        if self.get_name() and self.get_age() and self.get_wristband() and self.get_risk() and other_mother.get_name() and \
            other_mother.get_age() and other_mother.get_wristband() and other_mother.get_risk():
        
            return self.get_name() == other_mother.get_name() and self.get_age() == other_mother.get_age() and \
                self.get_wristband() == other_mother.get_wristband() and self.get_risk() == other_mother.get_risk()

        else:
            if self.get_name() and not (self.get_age() or self.get_wristband() or self.get_risk()) and \
                other_mother.get_name() and not (other_mother.get_age() or other_mother.get_wristband() or \
                                                 other_mother.get_risk()):
                return self.get_name() == other_mother.get_name()
            
            return False


    def __str__(self):
        """
        The string representation of the current Mother instance.

        Returns:
            str: the current Mother instance as a string.

        Example:
            If all attributes are defined:
                >>> str(mother)
                "Barbara Brooks, 28, green, high"

            If only the name attribute is defined (with other attributes set to None):
                >>> str(mother)
                "Barbara Brooks"
        """

        if self.get_name() and self.get_age() and self.get_wristband() and self.get_risk():
            return f"{self.get_name()}, {(self.get_age())}, {self.get_wristband()}, {self.get_risk()}"
            
        else:
            return f"{self.get_name()}"