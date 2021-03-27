import unittest

import gsites2md.test.TestHTML2md as TestHTML2md
import gsites2md.test.TestHTML2mdConverter as TestHTML2mdConverter
import gsites2md.test.TestHTMLParser2md as TestHTMLParser2md

# initialize the test suite
loader = unittest.TestLoader()
suite = unittest.TestSuite()

# add tests to the test suite
suite.addTests(loader.loadTestsFromModule(TestHTML2md))
suite.addTests(loader.loadTestsFromModule(TestHTML2mdConverter))
suite.addTests(loader.loadTestsFromModule(TestHTMLParser2md))

# initialize a runner, pass it your suite and run it
runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)