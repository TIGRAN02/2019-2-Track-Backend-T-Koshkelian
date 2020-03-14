import time

from django.test import TestCase, Client, LiveServerTestCase
from selenium import webdriver


class FillDataBaseTest(TestCase):

    def setUp(self):
        self.Client = Client()

    def test_correct(self):
        response = self.Client.get('/fill_db/')
        self.assertEqual(response.status_code, 200)


class SeleniumTests(LiveServerTestCase):
    selenium = None
    fixtures = ['fixtures.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Chrome(executable_path='./chromedriver')
        cls.selenium.implicitly_wait(30)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_create_account(self):
        self.selenium.get('http://localhost:3000/#/')
        time.sleep(0.1)
        self.selenium.find_element_by_xpath('//*[@id="root"]/div/a').click()
        username_input = self.selenium.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/input[1]')
        username_input.send_keys('Marianna')
        tag_input = self.selenium.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/input[2]')
        tag_input.send_keys('Tangerine')
        bio_input = self.selenium.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/textarea')
        bio_input.send_keys('Hey there')
        password_input = self.selenium.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div[2]/input[1]')
        password_input.send_keys('secret')
        repeat_password_input = self.selenium.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div[2]/input[2]')
        repeat_password_input.send_keys('secret')
        self.selenium.find_element_by_xpath('//*[@id="root"]/div/div[1]/div[3]/div/div/img').click()
