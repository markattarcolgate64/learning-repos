#!/usr/bin/env python3
"""Run all coding interview prep tests."""
import unittest
import sys
import os


def main():
    root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(root)

    loader = unittest.TestLoader()
    suite = loader.discover('.', pattern='test_exercise.py')
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)


if __name__ == '__main__':
    main()
