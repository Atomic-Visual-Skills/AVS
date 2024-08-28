import argparse

import sys
sys.path.append('../')

import models


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--input', type=str)
    parser.add_argument('--output', type=str)
    parser.add_argument('--model', type=str,
                        choices=['gpt-4o', 'custom'])
    parser.add_argument('--cot', type='store_true')
    args = parser.parse_args()