Feature: Assessment Form loads when user visits "/"
    In order to streamline the user experience
    An Authenticated Local Admin
    Should see the assessment form when he visits "/"
 
    Scenario: Assessment Form appears
        Given I am an Authenticated Local Admin
        And I visit "/"
        Then the words, "Organization:" appear at the top left of the page, and the words "(Admin Panel)" appear at the top left of the page, hyperlinked to "/admin" and the assessment form loads.