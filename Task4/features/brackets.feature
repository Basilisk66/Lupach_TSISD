Feature: Bracket sequence validation
  As a developer
  I wanna check the balance of round brackets
  To correctly process user input

  Scenario: Balanced string
    Given the string "fsd(выа(13)33)вы"
    When I check the brackets
    Then the result is balanced
    And the first mismatch index is absent

  Scenario: Extra closing bracket
    Given the string "32(234)sv)sd"
    When I check the brackets
    Then the result is not balanced
    And the first mismatch index is 9

  Scenario: Not enough closing bracket
    Given the string "(()"
    When I check the brackets
    Then the result is not balanced
    And the first mismatch index is 3

  Scenario: String without brackets is balanced
    Given the string "42abc"
    When I check the brackets
    Then the result is balanced
    And the first mismatch index is absent