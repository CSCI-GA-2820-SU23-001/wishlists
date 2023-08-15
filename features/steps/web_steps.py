######################################################################
# Copyright 2016, 2023 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
######################################################################

# pylint: disable=function-redefined, missing-function-docstring
# flake8: noqa
"""
Web Steps

Steps file for web interactions with Selenium

For information on Waiting until elements are present in the HTML see:
    https://selenium-python.readthedocs.io/waits.html
"""
import logging
from behave import when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions

@when('I visit the "Home Page"')
def step_impl(context):
    """ Make a call to the base URL """
    context.driver.get(context.base_url)

@then('I should see "{message}" in the title')
def step_impl(context, message):
    """ Check the document title for a message """
    assert(message in context.driver.title)

@then('I should not see "{text_string}"')
def step_impl(context, text_string):
    element = context.driver.find_element(By.TAG_NAME, 'body')
    assert(text_string not in element.text)

@when('I set the "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    element_id = element_name.lower().replace(' ', '_')
    element = context.driver.find_element(By.ID, element_id)
    element.clear()
    element.send_keys(text_string)

@when('I select "{text_string}" from the "{element_name}"')
def step_impl(context, element_name, text_string):
    element_id = element_name.lower().replace(' ', '_')
    element = context.driver.find_element(By.ID, element_id)
    select = Select(element)
    select.select_by_value(text_string)

@then('"{text_string}" should be selected in the "{element_name}" field')
def step_impl(context, element_name, text_string):
    element_id = element_name.lower().replace(' ', '_')
    element = context.driver.find_element(By.ID, element_id)
    select = Select(element)
    assert(select.first_selected_option.text == text_string)

@then('the "{element_name}" field should be empty')
def step_impl(context, element_name):
    element_id = element_name.lower().replace(' ', '_')
    element = context.driver.find_element(By.ID, element_id)
    assert(element.get_attribute('value') == '')

@when('I press the "{button}" button')
def step_impl(context, button):
    button_id = button.lower() + '_btn'
    context.driver.find_element(By.ID, button_id).click()    

@when('I press the "{button}" button of form' )
def step_impl(context, button):
    button_id = button.lower() + '_btn'
    context.driver.find_element(By.ID, button_id).click()
    context.last_clicked_button = button_id

@then('I should see "{text_string}" in the "{element_name}" field')
def step_impl(context, text_string, element_name):
    element_id = element_name.lower().replace(' ', '_')
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.text_to_be_present_in_element_value(
            (By.ID, element_id),
            text_string
        )
    )
    assert(found)

@then('I should see the message "{message}"')
def step_impl(context, message):
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, 'flash_message'),
            message
        )
    )
    assert(found)

@when('I copy the "{element_name}" field')
def step_impl(context, element_name):
    element_id = element_name.lower().replace(' ', '_')
    element = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.presence_of_element_located((By.ID, element_id))
    )
    context.clipboard = element.get_attribute('value')
    logging.info('Clipboard contains: %s', context.clipboard)

@when('I paste the "{element_name}" field')
def step_impl(context, element_name):
    element_id = element_name.lower().replace(' ', '_')
    element = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.presence_of_element_located((By.ID, element_id))
    )
    element.clear()
    element.send_keys(context.clipboard)

@then('I should see "{name}" in the "{form}" results')
def step_impl(context, name, form):
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, (form+'_search_results')),
            name
        )
    )
    assert(found)

@then('I should not see "{name}" in the "{form}" results')
def step_impl(context, name, form):
    element_id = form + '_search_results'
    print("Searching for element with ID:", element_id)
    element = context.driver.find_element(By.ID,element_id)
    assert(name not in element.text)

@when('I change the "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    """ Changes the value of a specified input field """
    element_id = element_name.lower().replace(' ', '_')
    element = context.driver.find_element(By.ID, element_id)
    element.clear()
    element.send_keys(text_string)

@when('I visit the "{form_name}" form')
def step_impl(context, form_name):
    element_id = form_name.lower().replace(' ', '_') + "_form_data"
    WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.presence_of_element_located((By.ID, element_id))
    )