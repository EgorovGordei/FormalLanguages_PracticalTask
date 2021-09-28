from Automate import Automate, AutomateNoWayException


def test_fromtask_0():
    regular_expression = "ab+c.aba.*.bac.+.+*"
    string = "babc"
    
    a = Automate(regular_expression)
    a.reverse()
    a.determinise()
    string = string[::-1]

    a.reset()
    longest_suffix = ""
    try:
        for c in string:
            a.goto(c)
            longest_suffix += c
    except AutomateNoWayException as e:
        pass

    assert(len(longest_suffix) == 2)

def test_fromtask_0():
    regular_expression = "acb..bab.c.*.ab.ba.+.+*a."
    string = "cbaa"
    
    a = Automate(regular_expression)
    a.reverse()
    a.determinise()
    string = string[::-1]

    a.reset()
    longest_suffix = ""
    try:
        for c in string:
            a.goto(c)
            longest_suffix += c
    except AutomateNoWayException as e:
        pass

    assert(len(longest_suffix) == 4)

def test_custom_all_0():
    regular_expression = "abc*.+ab.+"
    a = Automate(regular_expression)
    a.reverse()
    a.determinise()
    assert(hash(a) == 15289)

def test_custom_all_1():
    regular_expression = "a*bc+."
    a = Automate(regular_expression)
    a.reverse()
    a.determinise()
    assert(str(a) == """Automate:
Start node:1, current active node: 0
Nodes:
[index:0 finish:True edges:[2]] [index:1 finish:False edges:[0, 1]] [index:2 finish:True edges:[3]] [index:3 finish:True edges:[4]] 
Edges:
[index:0 from:1 to:3 letter:b][index:1 from:1 to:0 letter:c][index:2 from:0 to:2 letter:a][index:3 from:2 to:2 letter:a][index:4 from:3 to:2 letter:a]""")

def test_custom_word_0():
    regular_expression = "ab+ab*+."
    a = Automate(regular_expression)
    a.reverse()
    a.determinise()
    assert(a.check_word("a") == True)
    assert(a.check_word("bbb") == True)
    assert(a.check_word("aab") == False)
    assert(a.check_word("") == False)

def test_custom_word_1():
    regular_expression = "ab.*ba.*."
    a = Automate(regular_expression)
    a.reverse()
    a.determinise()
    assert(a.check_word("abab") == True)
    assert(a.check_word("abba") == True)
    assert(a.check_word("abbaab") == False)
    assert(a.check_word("") == True)

def test_custom_exception_0():
    try:
        a = Automate("abc")
        for node in a.nodes:
            node.finish = True
        a.reverse()
        assert(False)
    except NotImplementedError:
        assert(True)

def test_custom_exception_1():
    try:
        a = Automate("abc")
        for node in a.nodes:
            node.finish = False
        a.reverse()
        assert(False)
    except NotImplementedError:
        assert(True)

def test_custom_exception_2():
    try:
        a = Automate("abc")
        for node in a.nodes:
            node.finish = False
        a.determinise()
        assert(False)
    except NotImplementedError:
        assert(True)

