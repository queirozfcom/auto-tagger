# -*- coding: utf-8 -*-

from src.tests.context import ranking

import numpy as np
from numpy.testing import *
import unittest


class PrecisionSuite(unittest.TestCase):
    """Basic test cases."""

    # @unittest.skip("skip")
    def test1_precision_1d(self):
        arr1 = np.array([0, 0, 1])
        scores1 = np.array([0.2, 0.3, 0.5])
        scores1_not_sum_1 = np.array([x * 4 for x in scores1])

        k = 1
        expected_prec_at_k = 1.0
        expected_prec_at_k_normalized = 1.0

        actual_normalized = ranking.precision_at_k(y_true=arr1, y_score=scores1, k=k, normalize=True)
        actual = ranking.precision_at_k(y_true=arr1, y_score=scores1, k=k, normalize=False)
        actual_not_sum_1 = ranking.precision_at_k(y_true=arr1, y_score=scores1_not_sum_1, k=k, normalize=False)
        actual_normalized_not_sum_1 = ranking.precision_at_k(y_true=arr1, y_score=scores1_not_sum_1, k=k,
                                                             normalize=True)

        self.assertEqual(expected_prec_at_k_normalized, actual_normalized)
        self.assertEqual(expected_prec_at_k, actual)
        self.assertEqual(expected_prec_at_k_normalized, actual_normalized_not_sum_1)
        self.assertEqual(expected_prec_at_k, actual_not_sum_1)

        k = 2
        expected_precision_at_k_normalized = 1.0
        expected_precision_at_k = 0.5

        actual = ranking.precision_at_k(y_true=arr1, y_score=scores1, k=k, normalize=False)
        actual_normalized = ranking.precision_at_k(y_true=arr1, y_score=scores1, k=k, normalize=True)
        actual_not_sum_1 = ranking.precision_at_k(y_true=arr1, y_score=scores1_not_sum_1, k=k, normalize=False)
        actual_normalized_not_sum_1 = ranking.precision_at_k(y_true=arr1, y_score=scores1_not_sum_1, k=k,
                                                             normalize=True)

        self.assertEqual(expected_precision_at_k, actual)
        self.assertEqual(expected_precision_at_k_normalized, actual_normalized)
        self.assertEqual(expected_precision_at_k, actual_not_sum_1)
        self.assertEqual(expected_precision_at_k_normalized, actual_normalized_not_sum_1)

    # @unittest.skip("skip")
    def test2_precision_1d(self):
        """
        same as before but now the indicator array has 2 positives
        :return:
        """
        arr1 = np.array([0, 1, 1])
        scores1 = np.array([0.2, 0.3, 0.5])
        scores1_not_sum_1 = np.array([x * 1542 for x in scores1])

        k = 1
        expected_normalized_precision_at_k = 1.0
        expected_precision_at_k = 1.0

        actual_normalized = ranking.precision_at_k(y_true=arr1, y_score=scores1, k=k, normalize=True)
        actual_normalized_not_sum_1 = ranking.precision_at_k(y_true=arr1, y_score=scores1_not_sum_1, k=k,
                                                             normalize=True)
        actual = ranking.precision_at_k(y_true=arr1, y_score=scores1, k=k, normalize=False)
        actual_not_sum_1 = ranking.precision_at_k(y_true=arr1, y_score=scores1_not_sum_1, k=k, normalize=False)

        self.assertEqual(expected_normalized_precision_at_k, actual_normalized)
        self.assertEqual(expected_normalized_precision_at_k, actual_normalized_not_sum_1)
        self.assertEqual(expected_precision_at_k, actual)
        self.assertEqual(expected_precision_at_k, actual_not_sum_1)

        k = 2
        expected_normalized_precision_at_k = 1.0
        expected_precision_at_k = 1.0

        actual_normalized = ranking.precision_at_k(y_true=arr1, y_score=scores1, k=k, normalize=True)
        actual_normalized_not_sum_1 = ranking.precision_at_k(y_true=arr1, y_score=scores1_not_sum_1, k=k,
                                                             normalize=True)
        actual = ranking.precision_at_k(y_true=arr1, y_score=scores1, k=k, normalize=False)
        actual_not_sum_1 = ranking.precision_at_k(y_true=arr1, y_score=scores1_not_sum_1, k=k, normalize=False)

        self.assertEqual(expected_normalized_precision_at_k, actual_normalized)
        self.assertEqual(expected_normalized_precision_at_k, actual_normalized_not_sum_1)
        self.assertEqual(expected_precision_at_k, actual)
        self.assertEqual(expected_precision_at_k, actual_not_sum_1)

    # @unittest.skip("skip")
    def test3_precision_1d(self):
        arr1 = np.array([0, 1, 1])
        scores1 = np.array([0.7, 0.1, 0.2])
        scores1_not_sum_1 = np.array([x * 44 for x in scores1])

        k = 1
        expected_normalized_precision_at_k = 0.0
        expected_precision_at_k = 0.0

        actual_normalized = ranking.precision_at_k(y_true=arr1, y_score=scores1, k=k, normalize=True)
        actual_normalized_not_sum_1 = ranking.precision_at_k(y_true=arr1, y_score=scores1_not_sum_1, k=k,
                                                             normalize=True)
        actual = ranking.precision_at_k(y_true=arr1, y_score=scores1, k=k, normalize=False)
        actual_not_sum_1 = ranking.precision_at_k(y_true=arr1, y_score=scores1_not_sum_1, k=k, normalize=False)

        self.assertEqual(expected_normalized_precision_at_k, actual_normalized)
        self.assertEqual(expected_normalized_precision_at_k, actual_normalized_not_sum_1)
        self.assertEqual(expected_precision_at_k, actual)
        self.assertEqual(expected_precision_at_k, actual_not_sum_1)

        k = 2
        expected_normalized_precision_at_k = 0.5
        expected_precision_at_k = 0.5

        actual_normalized = ranking.precision_at_k(y_true=arr1, y_score=scores1, k=k, normalize=True)
        actual_normalized_not_sum_1 = ranking.precision_at_k(y_true=arr1, y_score=scores1_not_sum_1, k=k,
                                                             normalize=True)
        actual = ranking.precision_at_k(y_true=arr1, y_score=scores1, k=k, normalize=False)
        actual_not_sum_1 = ranking.precision_at_k(y_true=arr1, y_score=scores1_not_sum_1, k=k, normalize=False)

        self.assertEqual(expected_normalized_precision_at_k, actual_normalized)
        self.assertEqual(expected_normalized_precision_at_k, actual_normalized_not_sum_1)
        self.assertEqual(expected_precision_at_k, actual)
        self.assertEqual(expected_precision_at_k, actual_not_sum_1)

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
        expected_prec_k = np.array([[1.0], [1.0]])

        for i, row in enumerate(arr3):
            # print("y_true is: {}".format(arr3[i, :]))
            # print("y_true.shape is: {}".format(arr3[i, :].shape))

            actual = ranking.precision_at_k(y_true=arr3[i, :], y_score=scores3[i, :], k=k, normalize=True)
            actual_piecewise.append(actual)

        values_actual_piecewise = np.vstack(actual_piecewise)
        values_actual = ranking.precision_at_k(y_true=arr3, y_score=scores3, k=k, normalize=True)

        # print(values_actual_piecewise)
        # print("values_actual: {} \n".format(values_actual))

        self.assertEqual(values_actual_piecewise.shape, values_actual.shape, "shapes must match")
        self.assertTrue(np.allclose(values_actual_piecewise, values_actual), "values must match")
        self.assertTrue(np.allclose(values_actual_piecewise, expected_prec_k), "values must match")
        self.assertTrue(np.allclose(values_actual, expected_prec_k), "values must match")

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
        expected_prec_k_1 = np.array([
            [1.0],
            [1.0],
            [0.0],
            [1.0],
            [1.0]
        ])

        for i, row in enumerate(arr3):
            # print("y_true is: {}".format(arr3[i, :]))
            # print("y_true.shape is: {}".format(arr3[i, :].shape))

            actual = ranking.precision_at_k(y_true=arr3[i, :], y_score=scores3[i, :], k=k, normalize=True)
            actual_piecewise.append(actual)

        values_actual_piecewise = np.vstack(actual_piecewise)
        values_actual = ranking.precision_at_k(y_true=arr3, y_score=scores3, k=k, normalize=True)

        self.assertEqual(values_actual_piecewise.shape, values_actual.shape, "shapes must match")

        self.assertTrue(np.allclose(values_actual_piecewise, values_actual), "values must match")
        self.assertTrue(np.allclose(values_actual_piecewise, expected_prec_k_1), "values must match")
        self.assertTrue(np.allclose(values_actual, expected_prec_k_1), "values must match")

        k = 2
        expected_prec_k = np.array([
            [0.5],
            [0.5],
            [1.0],
            [1.0],
            [1.0]])

        actual_piecewise = list()

        for i, row in enumerate(arr3):
            # print("y_true is: {}".format(arr3[i, :]))
            # print("y_true.shape is: {}".format(arr3[i, :].shape))

            actual = ranking.precision_at_k(y_true=arr3[i, :], y_score=scores3[i, :], k=k, normalize=True)
            actual_piecewise.append(actual)

        values_actual_piecewise = np.vstack(actual_piecewise)
        values_actual = ranking.precision_at_k(y_true=arr3, y_score=scores3, k=k, normalize=True)

        self.assertTrue(np.allclose(values_actual_piecewise, values_actual), "values must match")
        self.assertTrue(np.allclose(values_actual_piecewise, expected_prec_k), "values must match")
        self.assertTrue(np.allclose(values_actual, expected_prec_k), "values must match")

        k = 3
        expected_prec_k = np.array([
            [1.0],
            [0.5],
            [1.0],
            [1.0],
            [1.0]
        ])

        expected_prec_k_not_normalized = np.array([
            [2 / 3],
            [1 / 3],
            [1 / 3],
            [1.0],
            [1.0]
        ])

        actual_piecewise = list()

        for i, row in enumerate(arr3):
            # print("y_true is: {}".format(arr3[i, :]))
            # print("y_true.shape is: {}".format(arr3[i, :].shape))

            actual = ranking.precision_at_k(y_true=arr3[i, :], y_score=scores3[i, :], k=k, normalize=True)
            actual_piecewise.append(actual)

        values_actual_piecewise = np.vstack(actual_piecewise)
        values_actual = ranking.precision_at_k(y_true=arr3, y_score=scores3, k=k, normalize=True)

        self.assertTrue(np.allclose(values_actual_piecewise, values_actual), "values must match")
        self.assertTrue(np.allclose(values_actual_piecewise, expected_prec_k), "values must match")

        self.assertTrue(np.allclose(values_actual, expected_prec_k), "values must match")

        values_actual_not_normalized = ranking.precision_at_k(y_true=arr3, y_score=scores3, k=k, normalize=False)

        self.assertTrue(np.allclose(expected_prec_k_not_normalized, values_actual_not_normalized))

    def test_exception_if_shapes_dont_match(self):
        arr1 = np.array([0, 1, 1])
        scores1 = np.array([0.7, 0.1, 0.2])
        arr2 = np.array([0, 1, 1, 0])
        scores2 = np.array([0.5, 0.1, 0.2, 0.2])

        with self.assertRaises(AssertionError):
            ranking.precision_at_k(y_true=arr1, y_score=scores2, k=1)

        with self.assertRaises(AssertionError):
            ranking.precision_at_k(y_true=arr2, y_score=scores1, k=1)


class RecallSuite(unittest.TestCase):
    """Basic test cases."""

    # @unittest.skip("skip")
    def test1_recall_1d(self):
        arr1 = np.array([0, 0, 1, 1, 0])
        scores1 = np.array([0.15, 0.15, 0.35, 0.2, 0.15])
        scores1_not_sum_1 = np.array([x * 4 for x in scores1])

        k = 1
        expected_recall_at_k = 0.5
        expected_recall_at_k_normalized = 1.0

        self.assertEqual(expected_recall_at_k, ranking.recall_at_k(y_true=arr1, y_score=scores1, k=k))
        self.assertEqual(expected_recall_at_k, ranking.recall_at_k(y_true=arr1, y_score=scores1_not_sum_1, k=k))
        self.assertEqual(expected_recall_at_k_normalized,
                         ranking.recall_at_k(y_true=arr1, y_score=scores1, k=k, normalize=True))
        self.assertEqual(expected_recall_at_k_normalized,
                         ranking.recall_at_k(y_true=arr1, y_score=scores1_not_sum_1, k=k, normalize=True))

        k = 2
        expected_recall_at_k = 1.0
        expected_recall_at_k_normalized = 1.0

        self.assertEqual(expected_recall_at_k, ranking.recall_at_k(y_true=arr1, y_score=scores1, k=k))
        self.assertEqual(expected_recall_at_k, ranking.recall_at_k(y_true=arr1, y_score=scores1_not_sum_1, k=k))
        self.assertEqual(expected_recall_at_k_normalized,
                         ranking.recall_at_k(y_true=arr1, y_score=scores1, k=k, normalize=True))
        self.assertEqual(expected_recall_at_k_normalized,
                         ranking.recall_at_k(y_true=arr1, y_score=scores1_not_sum_1, k=k, normalize=True))

        k = 3
        expected_recall_at_k = 1.0
        expected_recall_at_k_normalized = 1.0

        self.assertEqual(expected_recall_at_k, ranking.recall_at_k(y_true=arr1, y_score=scores1, k=k))
        self.assertEqual(expected_recall_at_k, ranking.recall_at_k(y_true=arr1, y_score=scores1_not_sum_1, k=k))
        self.assertEqual(expected_recall_at_k_normalized,
                         ranking.recall_at_k(y_true=arr1, y_score=scores1, k=k, normalize=True))
        self.assertEqual(expected_recall_at_k_normalized,
                         ranking.recall_at_k(y_true=arr1, y_score=scores1_not_sum_1, k=k, normalize=True))

    def test2_recall_2d(self):
        arr1 = np.array([
            [0, 0, 1, 1, 0],
            [0, 0, 1, 0, 0],
            [1, 0, 1, 1, 0],
            [1, 0, 1, 0, 1],
            [1, 0, 0, 0, 1]
        ])
        scores1 = np.array([
            [0.15, 0.10, 0.35, 0.25, 0.15],
            [0.15, 0.10, 0.35, 0.25, 0.15],
            [0.10, 0.15, 0.35, 0.25, 0.30],
            [0.15, 0.10, 0.35, 0.25, 0.01],
            [0.15, 0.10, 0.35, 0.25, 0.50]
        ])
        scores1_not_sum_1 = np.array([x * 4 for x in scores1])

        k = 1
        expected_recall_at_k = np.array([
            [1 / 2],
            [1],
            [1 / 3],
            [1 / 3],
            [1 / 2]
        ])

        assert_allclose(expected_recall_at_k, ranking.recall_at_k(y_true=arr1, y_score=scores1, k=k))
        assert_allclose(expected_recall_at_k, ranking.recall_at_k(y_true=arr1, y_score=scores1_not_sum_1, k=k))

        k = 2
        expected_recall_at_k = np.array([
            [1],
            [1],
            [1 / 3],
            [1 / 3],
            [1 / 2]
        ])

        assert_allclose(expected_recall_at_k, ranking.recall_at_k(y_true=arr1, y_score=scores1, k=k))
        assert_allclose(expected_recall_at_k, ranking.recall_at_k(y_true=arr1, y_score=scores1_not_sum_1, k=k))

        k = 3
        expected_recall_at_k = np.array([
            [1],
            [1],
            [2 / 3],
            [2 / 3],
            [1 / 2],
        ])

        assert_allclose(expected_recall_at_k, ranking.recall_at_k(y_true=arr1, y_score=scores1, k=k))
        assert_allclose(expected_recall_at_k, ranking.recall_at_k(y_true=arr1, y_score=scores1_not_sum_1, k=k))

    def test1d_k_higher_than_labels(self):
        arr1 = np.array([
            [0, 0, 1, 1, 0],
            [1, 0, 1, 1, 0],
        ])

        scores1 = np.array([
            [0.1, 0.1, 0.4, 0.3, 0.1],
            [0.1, 0.1, 0.4, 0.3, 0.1]
        ])

        k = 10

        values_actual = ranking.recall_at_k(y_true=arr1, y_score=scores1, k=k)

        # print(values_actual)


class F1Suite(unittest.TestCase):
    """Basic test cases."""

    # @unittest.skip("skip")
    def test1_f1_2d(self):
        arr1 = np.array([
            [0, 0, 1, 1, 0],
            [0, 0, 1, 0, 0],
            [1, 0, 1, 1, 0],
            [1, 0, 1, 0, 1],
            [1, 0, 0, 0, 1]
        ])
        scores1 = np.array([
            [0.15, 0.10, 0.35, 0.25, 0.15],
            [0.15, 0.10, 0.35, 0.25, 0.15],
            [0.10, 0.15, 0.35, 0.25, 0.30],
            [0.15, 0.10, 0.35, 0.25, 0.01],
            [0.15, 0.10, 0.35, 0.25, 0.50]
        ])
        scores1_not_sum_1 = np.array([x * 4 for x in scores1])

        k = 1
        expected_precision_at_k = np.array([
            [1.],
            [1.],
            [1.],
            [1.],
            [1.]
        ])

        expected_recall_at_k = np.array([
            [1 / 2],
            [1 / 1],
            [1 / 3],
            [1 / 3],
            [1 / 2]
        ])

        expected_f1_score_at_k = np.array([
            [2 / 3],
            [1.0],
            [0.5],
            [0.5],
            [2 / 3]
        ])

        assert_allclose(expected_precision_at_k, ranking.precision_at_k(y_true=arr1, y_score=scores1, k=k))
        assert_allclose(expected_recall_at_k, ranking.recall_at_k(y_true=arr1, y_score=scores1, k=k))
        assert_allclose(expected_recall_at_k, ranking.recall_at_k(y_true=arr1, y_score=scores1_not_sum_1, k=k))
        assert_allclose(expected_f1_score_at_k, ranking.f1_score_at_k(y_true=arr1, y_score=scores1, k=k))
        assert_allclose(expected_f1_score_at_k, ranking.f1_score_at_k(y_true=arr1, y_score=scores1_not_sum_1, k=k))

        k = 2
        expected_precision_at_k = np.array([
            [2 / 2],
            [1 / 2],
            [1 / 2],
            [1 / 2],
            [1 / 2]
        ])

        expected_recall_at_k = np.array([
            [2 / 2],
            [1 / 1],
            [1 / 3],
            [1 / 3],
            [1 / 2]
        ])

        expected_f1_score_at_k = np.array([
            [1.0],
            [2 / 3],
            [0.4],
            [0.4],
            [0.5]
        ])

        assert_allclose(expected_precision_at_k, ranking.precision_at_k(y_true=arr1, y_score=scores1, k=k))
        assert_allclose(expected_recall_at_k, ranking.recall_at_k(y_true=arr1, y_score=scores1_not_sum_1, k=k))
        assert_allclose(expected_f1_score_at_k, ranking.f1_score_at_k(y_true=arr1, y_score=scores1_not_sum_1, k=k))

    # @unittest.skip("skip")
    def test1_f1_2d_zero_result(self):
        arr1 = np.array([
            [0, 0, 1, 1, 0],
            [0, 0, 1, 0, 0],
            [1, 0, 1, 1, 0],
            [1, 0, 1, 0, 1],
            [1, 0, 0, 0, 1]
        ])
        scores1 = np.array([
            [0.15, 0.10, 0.35, 0.25, 0.15],
            [0.15, 0.10, 0.05, 0.25, 0.15],
            [0.10, 0.15, 0.35, 0.25, 0.30],
            [0.15, 0.10, 0.35, 0.25, 0.01],
            [0.15, 0.10, 0.35, 0.25, 0.50]
        ])
        scores1_not_sum_1 = np.array([x * 4 for x in scores1])

        k = 1
        expected_precision_at_k = np.array([
            [1.0],
            [0],
            [1.0],
            [1.0],
            [1.0]
        ])

        expected_recall_at_k = np.array([
            [1 / 2],
            [0.0],
            [1 / 3],
            [1 / 3],
            [1 / 2]
        ])

        expected_f1_score_at_k = np.array([
            [2 / 3],
            [0.0],
            [0.5],
            [0.5],
            [2 / 3]
        ])

        assert_allclose(expected_precision_at_k, ranking.precision_at_k(y_true=arr1, y_score=scores1, k=k))
        assert_allclose(expected_recall_at_k, ranking.recall_at_k(y_true=arr1, y_score=scores1, k=k))
        assert_allclose(expected_recall_at_k, ranking.recall_at_k(y_true=arr1, y_score=scores1_not_sum_1, k=k))
        assert_allclose(expected_f1_score_at_k, ranking.f1_score_at_k(y_true=arr1, y_score=scores1, k=k))
        assert_allclose(expected_f1_score_at_k, ranking.f1_score_at_k(y_true=arr1, y_score=scores1_not_sum_1, k=k))


class MicroF1Suite(unittest.TestCase):
    """Basic test cases."""

    # @unittest.skip("skip")
    def test1_f1_2d(self):
        arr1 = np.array([
            [0, 1, 0],
            [1, 1, 0],
            [0, 0, 1],
            [0, 0, 1]
        ])
        scores1 = np.array([
            [0.2, 0.5, 0.3],
            [0.5, 0.2, 0.3],
            [0.6, 0.1, 0.3],
            [0.5, 0.4, 0.1]
        ])
        scores1_not_sum_1 = np.array([x * 4 for x in scores1])

        k = 1
        expected_micro_average_at_k = 2 / 7

        assert_allclose(ranking.micro_f1_at_k(arr1, scores1, k=k), expected_micro_average_at_k)

        k = 2
        expected_micro_average_at_k = 3 / 10

        assert_allclose(ranking.micro_f1_at_k(arr1, scores1, k=k), expected_micro_average_at_k)

        k = 3
        expected_micro_average_at_k = 5 / 12

        assert_allclose(ranking.micro_f1_at_k(arr1, scores1, k=k), expected_micro_average_at_k)

    def test1_f1_2d_normalized(self):
        arr1 = np.array([
            [0,  1,  0],
            [1,  1,  0],
            [0,  0,  1],
            [0,  0,  1],
            [1,  1,  1],
        ])
        scores1 = np.array([
            [0.2, 0.5, 0.3],
            [0.5, 0.2, 0.3],
            [0.6, 0.1, 0.3],
            [0.5, 0.4, 0.1],
            [0.2, 0.5, 0.1],
        ])

        # stuff in parentheses is (TP+FN+FP)
        k = 1
        expected_micro_average_at_k = 3 / (3 + 0 + 2)

        assert_allclose(ranking.micro_f1_at_k(arr1, scores1, k=k, normalize=True), expected_micro_average_at_k)

        k = 2
        expected_micro_average_at_k = 5 / (5 + 0 + 5)

        assert_allclose(ranking.micro_f1_at_k(arr1, scores1, k=k, normalize=True), expected_micro_average_at_k)

        k = 3
        expected_micro_average_at_k = 8 / (8 + 0 + 7)

        assert_allclose(ranking.micro_f1_at_k(arr1, scores1, k=k, normalize=True), expected_micro_average_at_k)


if __name__ == '__main__':
    unittest.main()
