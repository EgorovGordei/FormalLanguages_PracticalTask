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
        a = Automate("abc..")
        for node in a.nodes:
            node.finish = True
        a.reverse()
        assert(False)
    except NotImplementedError:
        assert(True)

def test_custom_exception_1():
    try:
        a = Automate("abc..")
        for node in a.nodes:
            node.finish = False
        a.reverse()
        assert(False)
    except NotImplementedError:
        assert(True)

def test_custom_exception_2():
    try:
        a = Automate("abc..")
        for node in a.nodes:
            node.finish = False
        a.determinise()
        assert(False)
    except NotImplementedError:
        assert(True)

def test_basic_positive_0():
    a = Automate("1")
    a.determinise()
    assert(a.check_word(""))
    assert(not a.check_word("a"))

def test_basic_positive_1():
    a = Automate("ab.")
    a.determinise()
    assert(a.check_word("ab"))
    assert(not a.check_word(""))

def test_basic_positive_2():
    a = Automate("ab.*")
    a.determinise()
    assert(a.check_word("ababab"))
    assert(not a.check_word("babab"))

def test_basic_positive_3():
    a = Automate("ab+*")
    a.determinise()
    assert(a.check_word("abb"))
    assert(a.check_word("abbbaaa"))

def test_basic_positive_4():
    a = Automate("a1a..")
    a.determinise()
    assert(a.check_word("aa"))
    assert(not a.check_word("a"))

def test_basic_positive_5():
    a = Automate("abc.+")
    a.determinise()
    assert(a.check_word("a"))
    assert(a.check_word("bc"))

def test_basic_positive_6():
    a = Automate("abc++")
    a.determinise()
    assert(a.check_word("c"))
    assert(not a.check_word("ab"))

def test_basic_positive_7():
    a = Automate("1***b****.")
    a.determinise()
    assert(a.check_word("b"))
    assert(a.check_word("bbbb"))

def test_basic_positive_8():
    a = Automate("bc.ab.+*")
    a.determinise()
    assert(a.check_word("abbcbcab"))
    assert(not a.check_word("abbccb"))

def test_basic_positive_9():
    a = Automate("abc.c.c.c.*+")
    a.determinise()
    assert(not a.check_word("bccccabccccaaaa"))
    assert(a.check_word("bccccbcccc"))

def test_basic_negative_0():
    try:
        a = Automate("abc.")
        assert(False)
    except ValueError:
        assert(True)

def test_basic_negative_1():
    try:
        a = Automate("ab++++")
        assert(False)
    except ValueError:
        assert(True)

def test_basic_negative_2():
    try:
        a = Automate(".a")
        assert(False)
    except ValueError:
        assert(True)

def test_basic_negative_3():
    try:
        a = Automate("ab.ab.ab.ab.*")
        assert(False)
    except ValueError:
        assert(True)

def test_basic_negative_4():
    try:
        a = Automate("*")
        assert(False)
    except ValueError:
        assert(True)

