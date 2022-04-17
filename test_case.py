import unittest
import trendyol

testquery = trendyol.Trendyol("kitap")
testlink = "https://www.trendyol.com/sr?q=kitap"

class TestCalc(unittest.TestCase):
    # This subfunctions MUST START with test_....  
    # Tests whether our initial link conversion is correct. My first unit test!
    def test_query(self):
        result = trendyol.Trendyol.link(testquery)
        self.assertEqual(testlink, result, "False link")
    # Tests whether the limit is correctly reached or not
    def test_parser(self):
        result1 = trendyol.Trendyol.parser(testlink, 3)
        self.assertEqual(3, len(result1), "False n. of results")
        result2 = trendyol.Trendyol.parser(testlink, 25)
        self.assertEqual(25, len(result2), "False n. of results")
        result3 = trendyol.Trendyol.parser(testlink, 100)
        self.assertEqual(100, len(result3), "False n. of results")       

# This means that if we run this module directly, then run the code within the conditional. Just I can type 
if __name__ == '__main__':
    unittest.main()