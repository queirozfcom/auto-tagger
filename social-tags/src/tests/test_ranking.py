# -*- coding: utf-8 -*-

from .context import ranking

import numpy as np
import unittest


# prec @ 1 should equal
# prec @ 2 should equal
# prec @ 3 should equal
# prec @ 4 should equal
# prec @ n | n >4 should give out error



class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    # @unittest.skip("skip")
    def test1_precision_1d(self):
        arr1 = np.array([0, 0, 1])
        scores1 = np.array([0.2, 0.3, 0.5])
        scores1_not_sum_1 = np.array([x * 4 for x in scores1])

        expected_prec_at_1 = 1.0
        expected_precision_at_2 = 0.5

        k = 1
        actual = ranking.precision_at_k(y_true=arr1, y_score=scores1, k=k)
        actual_not_sum_1 = ranking.precision_at_k(y_true=arr1, y_score=scores1_not_sum_1, k=k)

        self.assertEqual(expected_prec_at_1, actual)
        self.assertEqual(expected_prec_at_1, actual_not_sum_1)

        k = 2
        actual = ranking.precision_at_k(y_true=arr1, y_score=scores1, k=k)
        actual_not_sum_1 = ranking.precision_at_k(y_true=arr1, y_score=scores1_not_sum_1, k=k)

        self.assertEqual(expected_precision_at_2, actual)
        self.assertEqual(expected_precision_at_2, actual_not_sum_1)

    # @unittest.skip("skip")
    def test2_precision_1d(self):
        """
        same as before but now the indicator array has 2 positives
        :return:
        """
        arr1 = np.array([0, 1, 1])
        scores1 = np.array([0.2, 0.3, 0.5])
        scores1_not_sum_1 = np.array([x * 1542 for x in scores1])

        expected_prec_at_1 = 1.0
        expected_precision_at_2 = 1.0

        k = 1
        actual = ranking.precision_at_k(y_true=arr1, y_score=scores1, k=k)
        actual_not_sum_1 = ranking.precision_at_k(y_true=arr1, y_score=scores1_not_sum_1, k=k)

        self.assertEqual(expected_prec_at_1, actual)
        self.assertEqual(expected_prec_at_1, actual_not_sum_1)

        k = 2
        actual = ranking.precision_at_k(y_true=arr1, y_score=scores1, k=k)
        actual_not_sum_1 = ranking.precision_at_k(y_true=arr1, y_score=scores1_not_sum_1, k=k)

        self.assertEqual(expected_precision_at_2, actual)
        self.assertEqual(expected_precision_at_2, actual_not_sum_1)

    # @unittest.skip("skip")
    def test3_precision_1d(self):
        arr1 = np.array([0, 1, 1])
        scores1 = np.array([0.7, 0.1, 0.2])
        scores1_not_sum_1 = np.array([x * 44 for x in scores1])

        expected_prec_at_1 = 0.0
        expected_precision_at_2 = 0.5

        k = 1
        actual = ranking.precision_at_k(y_true=arr1, y_score=scores1, k=k)
        actual_not_sum_1 = ranking.precision_at_k(y_true=arr1, y_score=scores1_not_sum_1, k=k)

        self.assertEqual(expected_prec_at_1, actual)
        self.assertEqual(expected_prec_at_1, actual_not_sum_1)

        k = 2
        actual = ranking.precision_at_k(y_true=arr1, y_score=scores1, k=k)
        actual_not_sum_1 = ranking.precision_at_k(y_true=arr1, y_score=scores1_not_sum_1, k=k)

        self.assertEqual(expected_precision_at_2, actual)
        self.assertEqual(expected_precision_at_2, actual_not_sum_1)

    # @unittest.skip("skip")
    def test2_precision_2d_minimal(self):
        arr3 = np.array([
            [0, 1],
            [1, 1]
        ])

        scores3 = np.array([
            [0, 0.4],
            [0.9, 0.1]
        ])

        actual_piecewise = list()

        k = 1
        expected_prec_k_1 = [1.0, 1.0]

        for i, row in enumerate(arr3):
            # print("y_true is: {}".format(arr3[i, :]))
            # print("y_true.shape is: {}".format(arr3[i, :].shape))

            actual = ranking.precision_at_k(y_true=arr3[i, :], y_score=scores3[i, :], k=k)
            actual_piecewise.append(actual)

        values_actual_piecewise = np.vstack(actual_piecewise)
        values_actual = ranking.precision_at_k(y_true=arr3, y_score=scores3, k=k)

        # print(values_actual_piecewise)
        # print("values_actual: {} \n".format(values_actual))

        self.assertEqual(values_actual_piecewise.shape, values_actual.shape, "shapes must match")
        self.assertTrue(np.allclose(values_actual_piecewise, values_actual), "values must match")
        self.assertTrue(np.allclose(values_actual_piecewise, expected_prec_k_1), "values must match")
        self.assertTrue(np.allclose(values_actual, expected_prec_k_1), "values must match")

    # @unittest.skip("skip")
    def test2_precision_2d(self):
        arr3 = np.array([
            [0, 1, 1, 0],
            [0, 0, 1, 1],
            [0, 0, 1, 0],
            [1, 1, 1, 1],
            [1, 1, 1, 1]
        ])

        scores3 = np.array([
            [0, 0.4, 0.25, 0.35],
            [0.3, 0.2, 0.5, 0.0],
            [0.1, 0.1, 0.2, 0.6],
            [0.9, 0.1, 0.05, 0.05],
            [0.1, 0.9, 0.05, 0.05]
        ])

        actual_piecewise = list()

        k = 1
        expected_prec_k_1 = [1.0, 1.0, 0.0, 1.0, 1.0]

        for i, row in enumerate(arr3):
            # print("y_true is: {}".format(arr3[i, :]))
            # print("y_true.shape is: {}".format(arr3[i, :].shape))

            actual = ranking.precision_at_k(y_true=arr3[i, :], y_score=scores3[i, :], k=k)
            actual_piecewise.append(actual)

        values_actual_piecewise = np.vstack(actual_piecewise)
        values_actual = ranking.precision_at_k(y_true=arr3, y_score=scores3, k=k)

        self.assertEqual(values_actual_piecewise.shape, values_actual.shape, "shapes must match")

        self.assertTrue(np.allclose(values_actual_piecewise, values_actual, expected_prec_k_1), "values must match")

        k = 2
        expected_prec_k_2 = [0.5, 0.5, 0.5, 1.0, 1.0]

        actual_piecewise = list()

        for i, row in enumerate(arr3):
            # print("y_true is: {}".format(arr3[i, :]))
            # print("y_true.shape is: {}".format(arr3[i, :].shape))

            actual = ranking.precision_at_k(y_true=arr3[i, :], y_score=scores3[i, :], k=k)
            actual_piecewise.append(actual)

        values_actual_piecewise = np.vstack(actual_piecewise)
        values_actual = ranking.precision_at_k(y_true=arr3, y_score=scores3, k=k)

        self.assertEqual(values_actual_piecewise.shape, values_actual.shape, "shapes must match")

        self.assertTrue(np.allclose(values_actual_piecewise, values_actual, expected_prec_k_1), "values must match")

    def test_exception_if_shapes_dont_match(self):
        arr1 = np.array([0, 1, 1])
        scores1 = np.array([0.7, 0.1, 0.2])
        arr2 = np.array([0, 1, 1, 0])
        scores2 = np.array([0.5, 0.1, 0.2, 0.2])

        with self.assertRaises(AssertionError):
            ranking.precision_at_k(y_true=arr1, y_score=scores2, k=1)

        with self.assertRaises(AssertionError):
            ranking.precision_at_k(y_true=arr2, y_score=scores1, k=1)


if __name__ == '__main__':
    unittest.main()
