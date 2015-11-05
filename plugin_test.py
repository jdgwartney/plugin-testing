
import unittest
from plugin_runner import PluginRunner
import json

"""
Example tests case that use a PluginRunner
"""


class PluginTest(unittest.TestCase):

    def get_source(self, source, output):
        """
        Searches the output of a PluginRunner that contain the source

        :param source: Source values to collect
        :param output: Results from a PluginRunner
        :return: subset array of output that matches the given source
        """
        r = []
        for o in output:
            if o['source'] == source:
                r.append(o)
        return r

    def get_metric_ids(self, output):
        """
        Generates a dictionary of metric ids and their associated counts
        :param output: Results from a PluginRunner
        :return: a dictionary of the counts of metrics in the output
        """
        r = {}
        for o in output:
            if o['metric'] not in r:
                r[o['metric']] = 1
            else:
                r[o['metric']] += 1
        return r

    def get_values(self, output, metric, source):
        """
        Returns a list of values given metric and source
        :param output: Results from a Plugin Runner
        :param metric: Metric values to collect
        :param source: Source values to collect
        :return:
        """
        r = []
        for o in output:
            if o['metric'] == metric and o['source'] == source:
                r.append(o['value'])
        return r

    def test_all_metric_count(self):
        """
        Run the plugin for a fix period and make sure the output is at least what we expect
        :return:
        """
        runner = PluginRunner()
        output = runner.run(20)
        self.assertGreaterEqual(len(output), 40)

    def source_metric_count(self, source, count):
        """
        Extract the sources from the output of PluginRunner and check to see if counts are at least what we expect
        :param source: Source to check counts against
        :param count: Minimum number of results expected from the PluginRunner output
        :return: None
        """
        runner = PluginRunner()
        output = runner.run(10)
        s = self.get_source(source, output)
        self.assertGreaterEqual(len(s), count)

    def test_red_source_metric_count(self):
        """
        Specific test for RED source
        :return: None
        """
        self.source_metric_count('RED', 20)

    def test_green_source_metric_count(self):
        """
        Specific test for GREEN source
        :return: None
        """
        self.source_metric_count('RED', 20)
        self.source_metric_count('GREEN', 20)

    def test_all_metrics_present(self):
        """
        Test to make sure all of our expected metrics are in the plugin output
        :return: None
        """
        runner = PluginRunner()
        output = runner.run(10)
        metrics = self.get_metric_ids(output)
        self.assertIn('DOCKER_BLOCK_IO_READ_BYTES', metrics)
        self.assertIn('DOCKER_TOTAL_CPU_USAGE', metrics)

    def test_metric_count(self):
        """
        Test to see if our metric count is at least what we expect
        :return:
        """
        runner = PluginRunner()
        output = runner.run(10)
        metrics = self.get_metric_ids(output)
        self.assertGreaterEqual(metrics['DOCKER_BLOCK_IO_READ_BYTES'], 20)
        self.assertGreaterEqual(metrics['DOCKER_TOTAL_CPU_USAGE'], 20)

    def values_check(self, metric, source):
        runner = PluginRunner()
        output = runner.run(10)
        values = self.get_values(output, metric, source)
        expected_values = PluginRunner.prime_sequence(len(values))

        self.assertGreaterEqual(values, 10)
        self.assertEqual(values, expected_values)

    def test_values_correct(self):
        """
        Validate that values in the plugin output is correct
        :return:
        """
        self.values_check('DOCKER_BLOCK_IO_READ_BYTES', 'RED')
        self.values_check('DOCKER_TOTAL_CPU_USAGE', 'RED')
        self.values_check('DOCKER_BLOCK_IO_READ_BYTES', 'GREEN')
        self.values_check('DOCKER_TOTAL_CPU_USAGE', 'GREEN')






