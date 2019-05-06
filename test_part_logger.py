import unittest
from part_logger import Part_Logger, Part

class Test_Part_Logger(unittest.TestCase):
    
    def setUp(self):
        self.logger = Part_Logger()
        self.part_1 = ['make_1', 'model_1', '2010']
        self.part_2 = ['make_1', 'model_2', '2010']
        self.part_3 = ['make_2', 'model_1', '2010']
        self.part_4 = ['make_1', 'model_3', '2003']
        self.part_5 = ['make_3', 'model_0', '2003']

    def tearDown(self):
        self.logger = None
        self.part_1, self.part_2, self.part_3, self.part_4, self.part_5 = None, None, None, None, None


class Test_Input_Types(Test_Part_Logger):
    
    def test_add_part(self):
        self.assertRaises(TypeError, self.logger.add_part, 99, 'model_1', '2010')
        self.assertRaises(TypeError, self.logger.add_part, 'make_1', True, '2010')
        self.assertRaises(TypeError, self.logger.add_part, 'make_1', 'model_1', 2010)

    def test_search_by_field(self):
        self.assertRaises(TypeError, self.logger.search_by_field, 99, 'model_1')
        self.assertRaises(TypeError, self.logger.search_by_field, 'model', 99)

    def test_search_by_id(self):
        self.assertRaises(TypeError, self.logger.search_by_id, '25')
        self.assertRaises(TypeError, self.logger.search_by_id, False)

    def test_remove_part(self):
        self.assertRaises(TypeError, self.logger.remove_part, '25')
        self.assertRaises(TypeError, self.logger.remove_part, True)
    

class Test_Input_Values(Test_Part_Logger):
    
    def test_add_part(self):
        self.assertRaises(ValueError, self.logger.add_part, '', 'model_1', '2010')
        self.assertRaises(ValueError, self.logger.add_part, 'make_1', '', '2010')
        self.assertRaises(ValueError, self.logger.add_part, 'make_1', 'model_1', '')
        self.assertRaises(ValueError, self.logger.add_part, 'make_1', 'model_1', 'year_1')
        self.assertRaises(ValueError, self.logger.add_part, 'make_1', 'model_1', '-2010')

    def test_search_by_field(self):
        self.assertRaises(ValueError, self.logger.search_by_field, 'date', '2010')
        self.assertRaises(ValueError, self.logger.search_by_field, 'model', '')
        self.assertRaises(ValueError, self.logger.search_by_field, 'year', 'March 2010')

    def test_search_by_id(self):
        self.assertRaises(ValueError, self.logger.search_by_id, -25)

    def test_remove_part(self):
        self.assertRaises(ValueError, self.logger.remove_part, -25)


class Test_Return_Types(Test_Part_Logger):

    def test_add_part(self):
        self.assertEqual(type(self.logger.add_part(*self.part_1)), int)

    def test_search_part_by_field(self):
        # test search while no data
        self.assertEqual(type(self.logger.search_by_field('model', 'model_1')), list)
        self.logger.add_part(*self.part_1)
        self.assertEqual(type(self.logger.search_by_field('model', 'model_1')), list)

    def test_search_part_by_id(self):
        # test search while no data
        self.assertEqual(type(self.logger.search_by_id(1)), type(None))
        self.logger.add_part(*self.part_1)
        self.assertEqual(type(self.logger.search_by_id(1)), Part)

    def test_remove_part(self):
        # test remove while no data
        self.assertEqual(type(self.logger.remove_part(1)), type(None))
        self.logger.add_part(*self.part_1)
        self.assertEqual(type(self.logger.remove_part(1)), Part)


class Test_Return_Values(Test_Part_Logger):

    def test_add_and_remove_parts(self):
        # testing the requirement of new ID being largest ID in the system + 1
        self.assertEqual(1, self.logger.add_part(*self.part_1))
        self.assertEqual(2, self.logger.add_part(*self.part_2))
        self.assertEqual(3, self.logger.add_part(*self.part_3))
        removed_part = self.logger.remove_part(1)
        self.assertTrue(removed_part.part_id == 1 
            and removed_part.make == 'make_1' 
            and removed_part.model == 'model_1' 
            and removed_part.year == '2010')
        removed_part = self.logger.remove_part(3)
        self.assertTrue(removed_part.part_id == 3 
            and removed_part.make == 'make_2' 
            and removed_part.model == 'model_1' 
            and removed_part.year == '2010')
        self.assertEqual(3, self.logger.add_part(*self.part_4))
        
    def test_search_part_by_field(self):
        self.assertEqual(self.logger.search_by_field('make', 'make_1'), [])
        self.assertEqual(self.logger.search_by_field('model', 'model_1'), [])
        self.assertEqual(self.logger.search_by_field('year', '2010'), [])
        # adding prior to searching
        self.logger.add_part(*self.part_1)
        self.logger.add_part(*self.part_2)
        self.logger.add_part(*self.part_3)
        self.logger.add_part(*self.part_4)
        self.logger.add_part(*self.part_5)

        self.assertEqual(len(self.logger.search_by_field('make', 'make_1')), 3)
        self.assertEqual(len(self.logger.search_by_field('model', 'model_1')), 2)
        self.assertEqual(len(self.logger.search_by_field('year', '2010')), 3)


    def test_search_part_by_id(self):
        self.assertEqual(self.logger.search_by_id(2), None)
        # adding prior to searching
        self.logger.add_part(*self.part_1)
        self.logger.add_part(*self.part_2)
        self.logger.add_part(*self.part_3)
        self.logger.add_part(*self.part_4)
        self.logger.add_part(*self.part_5)

        searched_part = self.logger.search_by_id(3)

        self.assertTrue(searched_part.part_id == 3 
            and searched_part.make == 'make_2' 
            and searched_part.model == 'model_1' 
            and searched_part.year == '2010')


if __name__ == '__main__':
    unittest.main()