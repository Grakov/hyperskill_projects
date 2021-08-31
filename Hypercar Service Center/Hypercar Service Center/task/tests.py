from urllib.error import URLError
from urllib.request import urlopen
from hstest.check_result import CheckResult
from hstest.test_case import TestCase
from hstest.django_test import DjangoTest


class HypercarWelcomeToServiceTest(DjangoTest):

    def get_welcome_page(self) -> CheckResult:
        try:
            main_page = self.read_page(f'http://localhost:{self.port}/welcome')
            if 'Welcome to the Hypercar Service!' in main_page:
                return CheckResult.true()
            return CheckResult.false(
                'Main page should contain "Welcome to the Hypercar Service!" line'
            )
        except URLError:
            return CheckResult.false(
                'Cannot connect to the /welcome page.'
            )

    def generate(self):
        return [
            TestCase(attach=self.check_server),
            TestCase(attach=self.get_welcome_page),
        ]

    def check(self, reply, attach):
        return attach()


if __name__ == '__main__':
    HypercarWelcomeToServiceTest('hypercar.manage').run_tests()
