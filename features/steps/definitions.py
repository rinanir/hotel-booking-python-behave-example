from behave import given, when, then, step
from hamcrest import assert_that, equal_to, has_key, greater_than_or_equal_to, has_property
import requests


def get_token():
    body = {
        'username': 'admin',
        'password': 'password123'
    }
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    response = requests.post(
        'http://localhost:8080/login', json=body, headers=headers)
    json = response.json()
    return json['token']


request_body = None
response = None
last_booking_id = None


@given(u'a user wants to make a booking with the following details')
def step_given_a_user_wants_to_make_a_booking(context):
    global request_body
    row = context.table.rows[0]
    request_body = {
        'firstname': row[0],
        'lastname': row[1],
        'totalprice': row[2],
        'depositpaid': row[3],
        'bookingdates': {
            'checkin': row[4],
            'checkout': row[5],
        },
        'additionalneeds': row[6]
    }


@when(u'the booking is submitted by the user')
def step_when_the_booking_is_submitted(context):
    global response
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {get_token()}'
    }
    response = requests.post(
        'http://localhost:8080/api/booking', json=request_body, headers=headers)


@then(u'the booking is successfully stored')
def step_the_booking_is_successfully_stored(context):
    assert_that(response.status_code, equal_to(200))


@then(u'shown to the user as stored')
def step_then_shown_to_the_user(context):
    json = response.json()
    assert_that(json, has_key('id'))
    assert_that(json['id'], greater_than_or_equal_to(1))


@given(u'Hotel Booking has existing bookings')
def step_given_hotel_has_existing_booking(context):
    global request_body
    request_body = {
        'firstname': 'rose',
        'lastname': 'boylu',
        'totalprice': 20,
        'depositpaid': 'true',
        'bookingdates': {
            'checkin': '2020-07-2',
            'checkout': '2020-07-2',
        },
        'additionalneeds': "no"
    }
    global response
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {get_token()}'
    }
    response = requests.post(
        'http://localhost:8080/api/booking', json=request_body, headers=headers)
    assert_that(response.status_code, equal_to(200))

    global last_booking_id
    json = response.json()
    assert_that(json['id'], greater_than_or_equal_to(1))
    last_booking_id = json['id']


@when(u'a specific booking is requested by the user')
def step_a_specific_booking_is_requested_by_the_user(context):
    global response
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {get_token()}'
    }

    response = requests.get(
        f'http://localhost:8080/api/booking/{last_booking_id}', headers=headers)

    assert_that(response.status_code, equal_to(200))


@then(u'the booking is shown')
def step_then_the_booking_is_sown(context):
    global response
    json = response.json()
    assert_that(json, has_key('firstname'))
    assert_that(json, has_key('lastname'))
    assert_that(json, has_key('totalprice'))
    assert_that(json, has_key('depositpaid'))
    assert_that(json, has_key('bookingdates'))
    assert_that(json, has_key('additionalneeds'))

    assert_that(json['bookingdates'], has_key('checkin'))
    assert_that(json['bookingdates'], has_key('checkout'))


@when(u'a specific booking is updated by the user')
def step_when_a_specific_booking_is_updated(context):
    global request_body
    request_body = {
        'firstname': 'Matus',
        'lastname': 'Novak',
        'totalprice': 20,
        'depositpaid': 'true',
        'bookingdates': {
            'checkin': '2020-07-2',
            'checkout': '2020-07-2',
        },
        'additionalneeds': "no"
    }
    global response
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {get_token()}'
    }
    response = requests.put(
        f'http://localhost:8080/api/booking/{last_booking_id}', json=request_body, headers=headers)
    assert_that(response.status_code, equal_to(200))


@then(u'the booking is shown to be updated')
def step_then_the_booking_is_shown_to_be_updated(context):
    json = response.json()

    assert_that(json, has_key('firstname'))
    assert_that(json, has_key('lastname'))
    assert_that(json['firstname'], greater_than_or_equal_to('Matus'))
    assert_that(json['lastname'], greater_than_or_equal_to('Novak'))


@when(u'a specific booking is deleted by the user')
def step_when_a_specific_booking_is_deleted(context):
    global response
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {get_token()}'
    }
    response = requests.delete(
        f'http://localhost:8080/api/booking/{last_booking_id}', headers=headers)
    assert_that(response.status_code, equal_to(200))


@then(u'the booking is removed')
def step_the_booking_is_removed(context):
    global response
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {get_token()}'
    }

    response = requests.get(
        f'http://localhost:8080/api/booking/{last_booking_id}', headers=headers)
    assert_that(response.status_code, equal_to(404))
