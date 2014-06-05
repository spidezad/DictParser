"""
    Unittest for Dict_create_fr_text module

"""
import os, sys, time
import unittest
from Dict_create_fr_text import DictParser

class DictCreateTestCase(unittest.TestCase):
    """ Base class for all DictCreate test

    """
    
    def create_open_file_object(self):
        """ Create a file object
            
        """
        temp_working_file = r'c:\data\temp\dictcreate.txt'
        self.testfile = open(temp_working_file,'w+')
        
    def erase_content_of_file(self):
        self.testfile.write('')

    def create_dict_name(self,name):
        self.testfile.write('$'+name)
        self.write_newline()

    def create_key_value_pair(self,key, value):
        """both key value pair in str"""
        self.testfile.write(str(key) + ':' + value)
        self.write_newline()

    def create_one_dict_object_in_text(self):
        self.create_dict_name('first')
        self.create_key_value_pair('aa','bbb,cccc,1,2,3')
        self.create_key_value_pair(1,'1,bbb,cccc,1,2,3')

    def create_2nd_dict_object_in_text(self):
        self.create_dict_name('second')
        self.create_key_value_pair('ee','bbb,cccc,1,2,3')
        self.create_key_value_pair(2,'1,bbb,cccc,1,2,3')

    def create_dict_with_multiple_object_type():
        pass

    def text_seq_creation(self):
        """write the text file in steps given"""

    def write_newline(self):
        self.testfile.write('\n')

    def close_file(self):
        """Close the working file -- may not need"""
        self.testfile.close()

class DictCreateTest(DictCreateTestCase):

    def setUp(self):
        self.create_open_file_object()
        self.dictreader = DictParser(r'c:\data\temp\dictcreate.txt')
        #self.erase_content_of_file()

    def test_get_dict_one_key_all_int(self):
        self.create_dict_name("first")
        self.create_key_value_pair('1', '1,2,3')
        self.close_file()

    def test_is_line_dict_name(self):
        """test the function that detect whether line is a dict name line"""
        self.assertTrue(self.dictreader.is_line_dict_name('$ abc'))
        self.assertTrue(self.dictreader.is_line_dict_name(' $abc'))
        self.assertFalse(self.dictreader.is_line_dict_name('abc'))
        self.assertFalse(self.dictreader.is_line_dict_name(''))

    def test_parse_dict_name(self):
        self.assertEqual( self.dictreader.parse_dict_name('$aaa'), 'aaa')
        self.assertEqual( self.dictreader.parse_dict_name('$ aaa'), 'aaa')
        self.assertEqual( self.dictreader.parse_dict_name('$ abc'), 'abc')
        with self.assertRaises(ValueError):
            self.dictreader.parse_dict_name('')
            self.dictreader.parse_dict_name('aaa')
            #self.dictreader.parse_dict_name('$aaa  aaaa')

    def test_is_line_key(self):
        self.assertFalse(self.dictreader.is_line_key('$ abc'))
        self.assertTrue(self.dictreader.is_line_key('abc:lll'))
        self.assertTrue(self.dictreader.is_line_key('1:999'))
        self.assertFalse(self.dictreader.is_line_key('1:'))

    def test_parse_key(self):
        self.assertItemsEqual( self.dictreader.parse_key('aaa:bbb'), ('aaa',['bbb']))
        self.assertItemsEqual( self.dictreader.parse_key('1:bbb'), (1,['bbb']))
        self.assertItemsEqual( self.dictreader.parse_key('1:bbb,ccc,ddd'), (1,['bbb','ccc','ddd']))
        self.assertItemsEqual( self.dictreader.parse_key('1: bbb,ccc,ddd'), (1,['bbb','ccc','ddd']))

    def test_parse_the_full_dict_one_dict_only(self):
        self.create_one_dict_object_in_text()
        self.close_file()
        self.dictreader = DictParser(r'c:\data\temp\dictcreate.txt')
        self.dictreader.parse_the_full_dict()
        temp_result =  {'aa':['bbb','cccc',1,2,3],1:[1,'bbb','cccc',1,2,3]}
        self.assertDictEqual( self.dictreader.dict_of_dict_obj['first'], temp_result)

    def test_parse_the_full_dict_two_dict_only(self):
        self.create_one_dict_object_in_text()
        self.write_newline()
        self.create_2nd_dict_object_in_text()
        self.close_file()
        self.dictreader = DictParser(r'c:\data\temp\dictcreate.txt')
        self.dictreader.parse_the_full_dict()
        temp_result = {'first': {'aa':['bbb','cccc',1,2,3],1:[1,'bbb','cccc',1,2,3]},
                       'second': {'ee':['bbb','cccc',1,2,3],2:[1,'bbb','cccc',1,2,3]}}
        self.assertDictEqual( self.dictreader.dict_of_dict_obj, temp_result)


    def tearDown(self):
        try:
            self.close_file()
        except:
            print 'File already closed'

if __name__ == '__main__':

    import coverage

    cov = coverage.coverage()
    cov.start()
    unittest.main()
    cov.stop()
    cov.report()

