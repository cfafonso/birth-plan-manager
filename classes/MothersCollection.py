#-*- coding: utf-8 -*-


from classes.Mother import Mother
from classes.DataManager import DataManager

from copy import deepcopy


class MothersCollection(DataManager):
    """
    A class to represent a collection of Mother objects.
    """
    
    def __init__(self, file_name = None, header = None, mothers = []):
        """
        Initializes a new MothersCollection.

        Args:
            file_name (str, optional): the name of the file associated with the collection. Defaults to None.
            header (Header, optional): the Header object associated with the collection. Defaults to None.
            doctors (list, optional): the list of Mother objects associated with the collection. Defaults to an empty list.
        
        Note:
            If file_name is provided and mothers is an empty list, the set_mothers() method will be called to populate
            the mothers from the file.
        """
        
        super().__init__(file_name, header)
        self._mothers = deepcopy(mothers)
                
        if self.get_file_name() and not self.get_mothers():
            self.set_mothers()
        
            
    def get_mothers(self):
        """
        A deep copy of the mothers attribute in the current MothersCollection instance.

        Returns:
            list: a deep copy of the list containing Mother objects. Changes to the returned list will not affect
                  the original one.
        """
        
        return deepcopy(self._mothers)
    
    
    def set_mothers(self, mothers = []):
        """
        Sets the list of Mother objects associated with the current MothersCollection instance.

        Args:
            mothers (list, optional): the list of Mother objects associated with the current MothersCollection instance.
                                      Defaults to an empty list.
        """

        if mothers == []:
            
            in_file = super().remove_header()
                        
            for line in in_file:
                name, age, wristband, risk = line.rstrip().split(", ")
                self._mothers.append(Mother(name, age, wristband, risk))

        else:
            self._mothers = mothers
            

    def mothers_items(self):
        """
        Supports iteration over the mothers attribute of the current MothersCollection instance.

        Yields:
            Mother: each Mother object in the mothers attribute, one at a time.
        """

        for mother in self._mothers:
            yield mother


    def sort_mothers(self):
        """
        Sorts the mothers in the current MothersCollection instance, from highest to lowest priority for assistance, 
        according to the criteria defined in the specification of the birth-plan-manager tool.
        """

        self._mothers.sort()
     
        
    def __lt__(self, other_mothers_collection):
        """
        Compares the current MothersCollection instance and another one according to the length of their
        mothers attribute.

        Args:
            other_mothers_collection (MothersCollection): another instance of the MothersCollection class.

        Returns:
            bool:
                - True if the current MothersCollection instance has less Mother objects than other_mothers_collection.
                - False otherwise.
        """

        return len(self.get_mothers()) < len(other_mothers_collection.get_mothers())


    def __eq__(self, other_mothers_collection):
        """
        Checks the equality between the current MothersCollection instance and another one according to the their
        mothers attribute.

        Args:
            other_mothers_collection (MothersCollection): another instance of the MothersCollection class.
        
        Returns:
            bool:
                - True if both instances have the same Mother objects in their mothers attribute.
                - False otherwise.
        """

        if len(self.get_mothers()) != len(other_mothers_collection.get_mothers()):
            return False
        
        return all(x == y for x, y in zip(sorted(self.get_mothers()), 
                                          sorted(other_mothers_collection.get_mothers())))

    
    def __str__(self):
        """
        The string representation of the current MothersCollection instance.
        
        Returns:
            str: the current MothersCollection instance as a string.
        
        Example:
            >>> str(motherscollection)
            "Filename:
             requests10h30.txt
             Organization:
             SmartH
             Time:
             10h30
             Date:
             10:12:2023
             Mothers:
             Barbara Brooks, 28, green, high
             Catherine Anderson, 30, red, low
             Alice Carter, 35, green, high"
        """

        return super().__str__() + '\n' + '\n'.join(str(mother) for mother in self.mothers_items())