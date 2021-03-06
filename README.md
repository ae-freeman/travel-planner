### Travel Planner

<br/>


This application is my capstone project for Harvard CS50.

This travel planner allows the user to register and create a login. The homepage displays all your trips. To add a trip, go to the add page
in the nav bar and fill in the destination and the date. Once added, the homepage will display the information, along with a picture of the destination
(retrieved from the Unsplash API).

To edit the trip, click on the edit button under each trip on the homepage.

Users can also find out the exchange rate. By inputting a starting currency, ending currency and starting amount, the application will return the value
in the end currency.

### Learning/Components
- Authentication
    - Login page x
    - Register page x
    - Create user in database x
    - Check login details against database x
    - Server-side error check to see if username already exists x
    - Client-side error check to see if username already exists
- Create a trip page
    - Input form x
    - Error checking x
    - Check date is the correct format x
    - Add form details to database x
    - Make api call for photo corresponding to API x
    - Add photo url to database x
- Home page
    - Display each trip for logged in user in a card with relevant details and image x
    - Edit button x
    - Styling of cards x
- Edit page
    - Input form x
    - Update database x
- Exchange rate
    - GET request: Input form with currency type input and output and amount in original currency x
    - Error check: see if those currency types exist x
    - Make api call x
    - POST request: Display converted currency (rounded to 2 d.p.) x
- POSSIBLE OTHER OPTIONS
    - Accomodation details on the card: in a different table?
    - File upload for bookings etc
    
## Screenshots

![HomePage](main-page.png)

![LoginPage](login-page.png)

![ExchangeMoneyPage](exchange-rate-input.png)

![ExchangeRateResult](exchange-result.png)

![AddTrip](add-trip.png)
