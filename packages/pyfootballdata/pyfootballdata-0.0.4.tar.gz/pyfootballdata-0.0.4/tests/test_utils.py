import unittest

from src.pyfootballdata.structs.filters import collect_unique_items
from src.pyfootballdata.structs.standings import convert_results_to_points, Form


class TestUtils(unittest.TestCase):
    def test_collect_unique_items(self):
        self.assertEqual(
            collect_unique_items(single=5, multiple=[2, 1, 2, 3]),
            [1, 2, 3, 5],
            "Should return [1, 2, 3, 5]",
        )

        self.assertEqual(
            collect_unique_items(multiple=[2, 1, 2, 3]),
            [1, 2, 3],
            "Should return [1, 2, 3]",
        )

        self.assertEqual(
            collect_unique_items(single=5),
            [5],
            "Should return [5]",
        )

        self.assertEqual(
            collect_unique_items(multiple=[]),
            None,
            "Should return None",
        )

    def test_convert_results_to_points(self):
        self.assertEqual(
            convert_results_to_points("W"),
            3,
            "Should return 3 points for a win",
        )
        self.assertEqual(
            convert_results_to_points("D"),
            1,
            "Should return 1 point for a draw",
        )
        self.assertEqual(
            convert_results_to_points("L"),
            0,
            "Should return 0 points for a loss",
        )

    def test_form_transformations(self):
        bunch_of_results = "W,D,L,D,W"
        form = Form(bunch_of_results)
        self.assertEqual(
            form,
            bunch_of_results,
            "Should return {}".format(bunch_of_results),
        )
        self.assertEqual(
            form.to_list(),
            ["W", "D", "L", "D", "W"],
            "Should return ['W', 'D', 'L', 'D', 'W']",
        )
        self.assertEqual(
            form.to_points_list(),
            [3, 1, 0, 1, 3],
            "Should return [3, 1, 0, 1, 3]",
        )
        with self.assertRaises(ValueError):
            Form("X,W,W,W,W").to_points_list()

    def test_form_equality(self):
        bunch_of_results = "W,D,L,D,W"
        form1 = Form(bunch_of_results)
        form2 = Form(bunch_of_results)
        self.assertEqual(form1, form2, "Forms should be equal")
        self.assertEqual(form1, bunch_of_results, "Form 1 has to be equal to initial string given")
        self.assertEqual(form2, bunch_of_results, "Form 1 has to be equal to initial string given")

        with self.assertRaises(TypeError):
            invalid_comparison = form1 == 5


