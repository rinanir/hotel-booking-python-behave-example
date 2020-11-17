Feature: Hotel Booking

  @HOTEL-1 @OPEN
  Scenario: Create a booking in Hotel Booking
    Given a user wants to make a booking with the following details
      | firstname | lastname | price | paid | from       | to         | needs     |
      | Mark      | Winters  | 120   | true | 2018-01-01 | 2018-01-03 | Breakfast |
    When the booking is submitted by the user
    Then the booking is successfully stored
    And shown to the user as stored

  @HOTEL-2 @OPEN
  Scenario: Retrieve a booking in Hotel Booking
    Given Hotel Booking has existing bookings
    When a specific booking is requested by the user
    Then the booking is shown

  @HOTEL-3 @OPEN
  Scenario: Update a booking in Hotel Booking
    Given Hotel Booking has existing bookings
    When a specific booking is updated by the user
    Then the booking is shown to be updated

  Scenario: Delete a booking in Hotel Booking
    Given Hotel Booking has existing bookings
    When a specific booking is deleted by the user
    Then the booking is removed
