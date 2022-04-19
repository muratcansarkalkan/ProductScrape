import unittest
import trendyol



class TestCalc(unittest.TestCase):
    # This subfunctions MUST START with test_....  
    
    # Execute before test method
    def setUp(self):
        print("Starting test...\n")
        self.testquery = trendyol.Trendyol("kitap")
        self.testlink = "https://www.trendyol.com/sr?q=kitap"
    # Execute after test method
    def tearDown(self):
        print("Testing complete.\n")
    # Tests whether our initial link conversion is correct. My first unit test!
    def test_query(self):
        print("Testing query defintion.\n")
        result = trendyol.Trendyol.link(self.testquery)
        self.assertEqual(self.testlink, result, "False link")
    # Tests whether the limit is correctly reached or not
    def test_parser(self):
        print("Testing result size.\n")
        result1 = trendyol.Trendyol.parser(self.testlink, 3)
        self.assertEqual(3, len(result1), "False n. of results")
        result2 = trendyol.Trendyol.parser(self.testlink, 25)
        self.assertEqual(25, len(result2), "False n. of results")
        result3 = trendyol.Trendyol.parser(self.testlink, 100)
        self.assertEqual(100, len(result3), "False n. of results")       

# This means that if we run this module directly, then run the code within the conditional. Just I can type 
if __name__ == '__main__':
    unittest.main()