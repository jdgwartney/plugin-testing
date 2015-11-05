import time


class PluginRunner(object):

    def __init__(self):
        pass

    @staticmethod
    def prime_sequence(max):
        primes = []
        i = 1
        while len(primes) < max:
            if i % 2 != 0:
                primes.append(i)
            i += 1
        return primes

    def send_output(self, metric, source, value):
        now = int(time.time())
        r = {'metric': metric, 'source': source, 'value': value, 'timestamp': now}
        return r

    def run(self, period=10):
        primes = PluginRunner.prime_sequence(period)
        results = []
        # This is a dummy implementation up we are just using the period for the number of interations
        # a real implementation will run for a fix period
        for i in range(1, period + 1):
            results.append(self.send_output('DOCKER_BLOCK_IO_READ_BYTES', 'RED', primes[i - 1]))
            results.append(self.send_output('DOCKER_TOTAL_CPU_USAGE', 'RED', primes[i - 1]))
            results.append(self.send_output('DOCKER_BLOCK_IO_READ_BYTES', 'GREEN', primes[i - 1]))
            results.append(self.send_output('DOCKER_TOTAL_CPU_USAGE', 'GREEN', primes[i - 1]))
        return results


if __name__ == '__main__':
    p = PluginRunner()
    p.run()
