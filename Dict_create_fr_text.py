"""
    Module to create series of dict from text file.
    The text file must be of certain format for retrieval.
    
    list of parameters
    # - only at start of string. Comment out.
    $ - dict name. only found in dict name, not in key, value pair.
    @ - object. Only use for key value pair. at start of string.

    eg of format used for different dict used in a setting text file.

        $first
        aa:bbb,cccc,1,2,3
        1:1,bbb,cccc,1,2,3

        $second
        ee:bbb,cccc,1,2,3
        2:1,bbb,cccc,1,2,3

    Will get two dict object (first & second). each with two keys.
    $ - defined the dict name
    the key and value will be the following lines of form key:value.
    The value will be a list of items of the correct base type.

    updates:
        Jul 17 204: Add in object handling
        Jun 21 2014: Add in case to handle simple comment
                   : Debug on the key value pair to take care of case with more than one ':'
        Jun 19 2014: put the parse_the_full_dict method in init so it str away call

"""
import os, time, sys, ast, re

class DictParser(object):
    
    def __init__(self,target_fname, lookup_dict = dict()):
        self.target_fname =  target_fname
        self.input_object_lookup = lookup_dict
        self.parse_the_full_dict()
        
    def set_input_object_lookup(self, lookup_dict):
        """Add in additional object in dict so that keyword with #xxx able to lookup when parse.

            Args:
                lookup_dict (dict): dict holding all required objects.

        """
        self.input_object_lookup =  lookup_dict


    def read_all_data_fr_file(self):
        """Method to read all the lines from the file and store it as a list

        """
        with open(self.target_fname,'r') as f:
            self.filedata = self.filter_comment_lines(f.readlines())

    def filter_comment_lines(self, list_of_lines):
        """Simple method to filter out comment line. Only works at the start of line marked with '#'.

            Args:
                list_of_lines (list): raw data.

            Returns:
                filtered version of the lines. 
        """
        return [line for line in list_of_lines if not line.startswith('#')]


    def is_line_dict_name(self, line):
        """
            Method to check if the line is a start of new dict and also the dict name.
            Args:
                line (str): particular line from the text file
            Returns:
                (bool): True if contain the dict name

        """
        line = line.lstrip()
        if not line == '':
            return line.startswith('$')
        else:
            return 0

    def parse_dict_name(self, line):
        """ Method to parse the dict name from a particular line.
            Use the '$' to denote the line as header.
            Args:
                line (str): particular line from the text file
            Returns:
                (str): dict name
        """
        line = line.lstrip()
        if '$' not in line or line == '' :
            raise ValueError('"$" not present in line. Line is not able to parse')
        else:
            return line.lstrip('$').strip()

    def is_line_key(self, line):
        """Method to check if line is a key. Key line will start with 'keyname:' and will start after the dict


        """
        if not ':' in line: return False
        if line.split(':')[1] == '':
            ## 'no value pair for the key. skip this key'
            return False

        return True
    
    def parse_key(self, line):
        """Method to parse the key value pair
            Args:
                line (str): particular line from the text file

            Returns:
                key (str):
                value (list): value will always in list

            TODO: not able to work with list of list. No correct format for the list??
            Temp treat as all element are fundamental type.

        
        """
        target_search_grp = re.match('^([a-zA-Z0-9_]*):(.*)', line)
        key = target_search_grp.group(1)
        value = target_search_grp.group(2)
        key =  self.convert_str_to_correct_type(key.strip())
        value = value.split(',')
        value =  [n.strip() for n in value]
        value = self.convert_list_of_str_to_type(value)
        
        return key, value

    def parse_the_full_dict(self):
        """Method to parse the full file of dict
            Once detect dict name open the all the key value pairs

        """
        self.read_all_data_fr_file()

        self.dict_of_dict_obj = {}
        ## start parsing each line
        ## intialise temp_dict obj
        start_dict_name = ''
        for line in self.filedata:
            if self.is_line_dict_name(line):
                start_dict_name = self.parse_dict_name(line)
                ## intialize the object
                self.dict_of_dict_obj[start_dict_name] = dict()
                
            elif self.is_line_key(line):
                 
                 temp_key, temp_value = self.parse_key(line)
                 self.dict_of_dict_obj[start_dict_name][temp_key] = temp_value
                    
    
    def convert_list_of_str_to_type(self, strlist):
        """ Function to convert the list of str element to the correct type.

            Args:
                strlist (list): list of element where each element is a string

            Returns:
                (list) : List with correctly converted elements.

            Function modified from http://stackoverflow.com/questions/2859674/converting-python-list-of-strings-to-their-type
        """
        
        return [self.convert_str_to_correct_type(n) for n in strlist ]
    
    def convert_str_to_correct_type(self, target_str):
        """ Method to convert the str repr to the correct type
            Idea from http://stackoverflow.com/questions/2859674/converting-python-list-of-strings-to-their-type
            If the target_str start with '#', indicate it is an object.
            Will then search the self.input_object_lookup for corresponding object.
            If no object found, return as string.

            Args:
                target_str (str): str repr of the type

            Returns:
                (str/float/int) : return the correct representation of the type
        """
        if target_str.startswith('@'):
            ## object detect
            return self.map_object_to_lookup(target_str)
        try:
            ans =  ast.literal_eval(target_str)
            return ans
        except:
            ## not converting as it is string
            pass
        return target_str

    def map_object_to_lookup(self,obj_name):
        """Map object to lookup table. Return back str if object not found
            Args:
                obj_name (str): object name to be use in lookup.
            Returns:
                (obj): Return corresponding object.
                or (str): Return str if object not found
        """
        if self.input_object_lookup.has_key(obj_name[1:]):
            return self.input_object_lookup[obj_name[1:]] # check with the # removed.
        else:
            return obj_name


if __name__ == '__main__':
    temp_working_file = r'c:\data\temp\dictcreate.txt'
    
    p = DictParser(temp_working_file, {'a':[1,3,4]})
    p.parse_the_full_dict()
    print p.dict_of_dict_obj    






