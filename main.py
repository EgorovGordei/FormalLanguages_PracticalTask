from Automate import Automate, AutomateNoWayException


#regular_expression = input("Regular expression: ")
#string = input("String: ")
regular_expression = "abc++*"
string = "abb"

a = Automate(regular_expression)
#a.reverse()
a.determinise()
#string = string[::-1]

a.reset()
longest_suffix = ""
try:
    for c in string:
        a.goto(c)
        longest_suffix += c
except AutomateNoWayException as e:
    pass

print(len(longest_suffix))

