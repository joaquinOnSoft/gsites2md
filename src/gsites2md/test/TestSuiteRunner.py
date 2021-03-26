import unittest

import gsites2md.test.TestHTML2md
import gsites2md.test.TestHTML2mdConverter

# initialize the test suite
loader = unittest.TestLoader()
suite = unittest.TestSuite()

# add tests to the test suite
suite.addTests(loader.loadTestsFromModule(gsites2md.test.TestHTML2md))
suite.addTests(loader.loadTestsFromModule(gsites2md.test.TestHTML2mdConverter))


# initialize a runner, pass it your suite and run it
runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)