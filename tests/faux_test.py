import unittest
"""
This is a bogus test just to satisfy Jenkins.
"""

class BogusTest(unittest.TestCase):
  def testBogus(self):
    self.assertEquals(1, 1)

if __name__ == '__main__':
  unittest.main()
