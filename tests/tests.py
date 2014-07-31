# IMPORTING FUNCTIONS
import sys
sys.path.append("../")
from generators import generate_diffs
from generators import apply_diffs

import json
import unittest

# ------------------------------------------#
#                                           #
#    generate_diffs takes 2 tokens lists    #
#  and outputs a json list of dictionaries  #
#                                           #
# ------------------------------------------#

class Test_Diff_Gen(unittest.TestCase):

    def setUp(self):
        pass

    def test_diff_gen_seed(self):
        print "\n\nSeeds an empty token."
        text1 = [""]
        text2 = ["This is a cat.", "This is another cat."]

        expected_result = [{"before_line": 1, "cmd": "+", "after_line": 1, "text": "This is a cat."}, {"before_line": 1, "cmd": "+", "after_line": 2, "text": "This is another cat."}]
        expected_result = json.dumps(expected_result)

        self.assertEqual(generate_diffs(text1, text2), expected_result)

    def test_diff_gen_subtract(self):
        print "\n\nDeletes a token."
        text1 = ["This is a cat.", "This is another cat."]
        text2 = ["This is a cat."]

        expected_result = [{"before_line": 2, "cmd": "-", "after_line": 1, "text": None}]
        expected_result = json.dumps(expected_result)

        self.assertEqual(generate_diffs(text1, text2), expected_result)

    def test_diff_gen_addition(self):
        print "\n\nAdds a token to the end."
        text1 = ["This is a cat."]
        text2 = ["This is a cat.", "I am a cat."]

        expected_result = [{"before_line": 1, "cmd": "+", "after_line": 2, "text": "I am a cat."}]
        expected_result = json.dumps(expected_result)

        self.assertEqual(generate_diffs(text1, text2), expected_result)

    def test_diff_gen_switch_token(self):
        print "\n\nSwitching tokens."
        text1 = ["This is a cat.", "I am a cat."]
        text2 = ["This is a cat.", "I am not a cat."]

        expected_result = [{"before_line": 2, "cmd": "-", "after_line": 1, "text": None}, {"before_line": 2, "cmd": "+", "after_line": 2, "text": "I am not a cat."}]
        expected_result = json.dumps(expected_result)

        self.assertEqual(generate_diffs(text1, text2), expected_result)

    def test_diff_gen_alternate(self):
        print "\n\nSwapping several tokens."
        text1 = ["I have a cat.", "Her name is Mana.", "My other cat's name is Jiji.", "Jiji sheds a lot.", "Jiji is also fat."]
        text2 = ["Her name is Mana.", "Not the test, my cat.", "Jiji sheds a lot.", "She's my cat."]

        expected_result = [{"before_line": 1, "cmd": "-", "after_line": 0, "text": None}, {"before_line": 3, "cmd": "-", "after_line": 1, "text": None}, {"before_line": 3, "cmd": "+", "after_line": 2, "text": "Not the test, my cat."}, {"before_line": 5, "cmd": "-", "after_line": 3, "text": None}, {"before_line": 5, "cmd": "+", "after_line": 4, "text": "She's my cat."}]
        expected_result = json.dumps(expected_result)

        self.assertEqual(generate_diffs(text1, text2), expected_result)

    def test_diff_gen_delete_first(self):
        print "\n\nSubtracting the first from several tokens."
        text1 = ["Mana likes to meow.", "Meow.", "Meow.", "Meow meow meow meow meow."]
        text2 = ["Meow.", "Meow.", "Meow meow meow meow meow."]

        expected_result = [{"before_line": 1, "cmd": "-", "after_line": 0, "text": None}]
        expected_result = json.dumps(expected_result)

        self.assertEqual(generate_diffs(text1, text2), expected_result)

    def test_diff_gen_add_first(self):
        print "\n\nAdding one token in the beginning of a list of several tokens."
        text1 = ["Mana likes to meow.", "Meow.", "Meow.", "Meow meow meow meow meow."]
        text2 = ["Meow meow meow meow.", "Mana likes to meow.", "Meow.", "Meow.", "Meow meow meow meow meow."]

        expected_result = [{"before_line": 0, "cmd": "+", "after_line": 1, "text": "Meow meow meow meow."}]
        expected_result = json.dumps(expected_result)

        self.assertEqual(generate_diffs(text1, text2), expected_result)

# ------------------------------------------#
#                                           #
#    apply_diffs takes a list of tokens,    #
#  object of diffs and creates new string   #
#                                           #
# ------------------------------------------#

# ** takes a list of tokens, and output tokens,
# ** and when text is needed as a string, i.e. displayed on editor,
# ** it can be joined into a string in the controller.

    def test_apply_seed(self):
        print "\n\nTake an empty string and add text."

        tokens = [""]
        diffs = json.dumps([{"before_line": 1, "cmd": "+", "after_line": 1, "text": "This is a cat."}, {"before_line": 1, "cmd": "+", "after_line": 2, "text": "This is another cat."}])

        expected_result = ["This is a cat.", "This is another cat."]

        self.assertEqual(apply_diffs(tokens, diffs), expected_result)

    def test_apply_subtract(self):
        print "\n\nSubtract a token."

        tokens = ["Meow meow meow meow.", "Too many meows."]
        diffs = json.dumps([{"before_line": 2, "cmd": "-", "after_line": 1, "text": None}])

        expected_result = ["Meow meow meow meow."]
        
        self.assertEqual(apply_diffs(tokens, diffs), expected_result)

    def test_apply_addition(self):
        print "\n\nAdd a token."

        tokens = ["Meow meow meow meow."]
        diffs = json.dumps([{"before_line": 1, "cmd": "+", "after_line": 2, "text": "Not enough meows."}])

        expected_result = ["Meow meow meow meow.", "Not enough meows."]
        
        self.assertEqual(apply_diffs(tokens, diffs), expected_result)

    def test_apply_switch_token(self):
        print "\n\nSwitching tokens."

        tokens = ["This is a cat.", "I am a cat."]
        diffs = json.dumps([{"before_line": 2, "cmd": "-", "after_line": 1, "text": None}, {"before_line": 2, "cmd": "+", "after_line": 2, "text": "I am not a cat."}])
        
        expected_result = ["This is a cat.", "I am not a cat."]
        
        self.assertEqual(apply_diffs(tokens, diffs), expected_result)

    def test_apply_alternate(self):
        print "\n\nSwapping several tokens."

        tokens = ["I have a cat.", "Her name is Mana.", "My other cat's name is Jiji.", "Jiji sheds a lot.", "Jiji is also fat."]
        diffs = json.dumps([{"before_line": 1, "cmd": "-", "after_line": 0, "text": None}, {"before_line": 3, "cmd": "-", "after_line": 1, "text": None}, {"before_line": 3, "cmd": "+", "after_line": 2, "text": "Not the test, my cat."}, {"before_line": 5, "cmd": "-", "after_line": 3, "text": None}, {"before_line": 5, "cmd": "+", "after_line": 4, "text": "She's my cat."}])

        expected_result = ["Her name is Mana.", "Not the test, my cat.", "Jiji sheds a lot.", "She's my cat."]
        
        self.assertEqual(apply_diffs(tokens, diffs), expected_result)

    def test_apply_delete_first(self):
        print "\n\nSubtracting the first from several tokens."

        tokens = ["Mana likes to meow.", "Meow.", "Meow.", "Meow meow meow meow meow."]
        diffs = json.dumps([{"before_line": 1, "cmd": "-", "after_line": 0, "text": None}])

        expected_result = ["Meow.", "Meow.", "Meow meow meow meow meow."]
        
        self.assertEqual(apply_diffs(tokens, diffs), expected_result)

    def test_apply_add_first(self):
        print "\n\nAdding one token in the beginning of a list of several tokens."

        tokens = ["Mana likes to meow.", "Meow.", "Meow.", "Meow meow meow meow meow."]
        diffs = json.dumps([{"before_line": 0, "cmd": "+", "after_line": 1, "text": "Meow meow meow meow."}])

        expected_result = ["Meow meow meow meow.", "Mana likes to meow.", "Meow.", "Meow.", "Meow meow meow meow meow."]
        
        self.assertEqual(apply_diffs(tokens, diffs), expected_result)

if __name__ == "__main__":
    unittest.main()