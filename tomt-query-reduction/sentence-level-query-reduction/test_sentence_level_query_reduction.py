from sentence_level_query_reduction import SentenceLevelQueryReduction, get_model_by_name
import unittest

class TestPredictions(unittest.TestCase):
    def test_predict_returns_always_zero(self):
        sentence_level_reduction = SentenceLevelQueryReduction(get_model_by_name('PredictAlwaysFalse'))

        expected = ''
        actual = sentence_level_reduction.reduce_query('Hello World. My Name is XYZ.')

        self.assertEquals(expected, actual)

    def test_predict_returns_always_true(self):
        sentence_level_reduction = SentenceLevelQueryReduction(get_model_by_name('PredictAlwaysTrue'))

        expected = 'Hello World. My Name is XYZ.'
        actual = sentence_level_reduction.reduce_query('Hello World. My Name is XYZ.')

        self.assertEquals(expected, actual)

    def test_predict_returns_true_if_sentence_contains_world(self):
        sentence_level_reduction = SentenceLevelQueryReduction(get_model_by_name('PredictTrueIfSentenceContainsWorld'))

        expected = 'Hello World.'
        actual = sentence_level_reduction.reduce_query('Hello World. My Name is XYZ.')

        self.assertEquals(expected, actual)

    def test_prediction_with_real_model(self):
        sentence_level_reduction = SentenceLevelQueryReduction(get_model_by_name('bert,/models/bert-checkpoint-31250-epoch-1'))

        expected = ''
        actual = sentence_level_reduction.reduce_query('Hello World. My Name is XYZ.')

        self.assertEquals(expected, actual)

    def test_prediction_with_real_model_01(self):
        sentence_level_reduction = SentenceLevelQueryReduction(get_model_by_name('bert,/models/bert-checkpoint-31250-epoch-1'))

        expected = 'The movie is about a robot that can travel time.'
        actual = sentence_level_reduction.reduce_query('The movie is about a robot that can travel time. Thanks in advance for your help!')

        self.assertEquals(expected, actual)
