import sys
import os

current_path = os.path.abspath(os.path.dirname(__file__))
project_path = os.path.abspath(os.path.join(current_path, '..'))
sys.path.append(project_path)

from bignumber.BigNumber import BigNumber

def test_add_same_signs():
    n1 = BigNumber("222")
    n2 = BigNumber("222")
    assert n1.add(n2).toString() == "444"

    n1 = BigNumber("-222")
    n2 = BigNumber("-222")
    assert n1.add(n2).toString() == "-444"

    n1 = BigNumber("-999")
    n2 = BigNumber("-1")
    assert n1.add(n2).toString() == "-1000"

    n1 = BigNumber("-1")
    n2 = BigNumber("-999")
    assert n1.add(n2).toString() == "-1000"

    n1 = BigNumber("-1654989746897")
    n2 = BigNumber("-222876787685")
    assert n1.add(n2).toString() == "-1877866534582"


def test_add_positive_negative():
    n1 = BigNumber("222")
    n2 = BigNumber("-222")
    assert n1.add(n2).toString() == "0"

    n1 = BigNumber("111")
    n2 = BigNumber("-99")
    assert n1.add(n2).toString() == "12"

    n1 = BigNumber("99")
    n2 = BigNumber("-111")
    assert n1.add(n2).toString() == "-12"

    n1 = BigNumber("222")
    n2 = BigNumber("-111")
    assert n1.add(n2).toString() == "111"

    n1 = BigNumber("1654989746897")
    n2 = BigNumber("-222876787685")
    assert n1.add(n2).toString() == "1432112959212"


def test_add_negative_positive():
    n1 = BigNumber("-222")
    n2 = BigNumber("222")
    assert n1.add(n2).toString() == "0"

    n1 = BigNumber("-111")
    n2 = BigNumber("99")
    assert n1.add(n2).toString() == "-12"

    n1 = BigNumber("-99")
    n2 = BigNumber("111")
    assert n1.add(n2).toString() == "12"

    n1 = BigNumber("-222")
    n2 = BigNumber("111")
    assert n1.add(n2).toString() == "-111"

    n1 = BigNumber("-1654989746897")
    n2 = BigNumber("222876787685")
    assert n1.add(n2).toString() == "-1432112959212"


def test_add_decimal():
    n1 = BigNumber("-222")
    n2 = BigNumber("222.00")
    assert n1.add(n2).toString() == "0"

    n1 = BigNumber("1.00")
    n2 = BigNumber("99")
    assert n1.add(n2).toString() == "100.00"

    n1 = BigNumber("-2")
    n2 = BigNumber("-2.00")
    assert n1.add(n2).toString() == "-4.00"

    n1 = BigNumber("-222.123")
    n2 = BigNumber("111.123")
    assert n1.add(n2).toString() == "-111.000"

    n1 = BigNumber("-1654989746897.123465")
    n2 = BigNumber("222876787685.123465")
    assert n1.add(n2).toString() == "-1432112959212.000000"


def test_sub_same_sign():
    n1 = BigNumber("5")
    n2 = BigNumber("5.0")
    assert n1.subtract(n2).toString() == "0"

    n1 = BigNumber("-5")
    n2 = BigNumber("-5.0")
    assert n1.subtract(n2).toString() == "0"

    n1 = BigNumber("-5")
    n2 = BigNumber("-10.0")
    assert n1.subtract(n2).toString() == "5.0"

    n1 = BigNumber("-10.0")
    n2 = BigNumber("-5.0")
    assert n1.subtract(n2).toString() == "-5.0"

    n1 = BigNumber("10")
    n2 = BigNumber("5")
    assert n1.subtract(n2).toString() == "5"


def test_sub_different_sign():
    n1 = BigNumber("5")
    n2 = BigNumber("-5.0")
    assert n1.subtract(n2).toString() == "10.0"

    n1 = BigNumber("-5")
    n2 = BigNumber("5.0")
    assert n1.subtract(n2).toString() == "-10.0"

    n1 = BigNumber("10")
    n2 = BigNumber("-5.0")
    assert n1.subtract(n2).toString() == "15.0"

    n1 = BigNumber("-10")
    n2 = BigNumber("5.0")
    assert n1.subtract(n2).toString() == "-15.0"


def test_multiply():
    n1 = BigNumber("5")
    n2 = BigNumber("-5.0")
    assert n1.multiply(n2).toString() == "-25.0"

    n1 = BigNumber("-5")
    n2 = BigNumber("-5.0")
    assert n1.multiply(n2).toString() == "25.0"     

    n1 = BigNumber("1.2")
    n2 = BigNumber("1.2")
    assert n1.multiply(n2).toString() == "1.44" 

    n1 = BigNumber("5")
    n2 = BigNumber("0.0")
    assert n1.multiply(n2).toString() == "0"

    n1 = BigNumber("55555")
    n2 = BigNumber("546465")
    assert n1.multiply(n2).toString() == "30358863075" 

def test_divide():
    n1 = BigNumber("5")
    n2 = BigNumber("5.0")
    assert n1.divide(n2).toString() == "1"    

    n1 = BigNumber("1465416546484")
    n2 = BigNumber("2")
    assert n1.divide(n2).toString() == "732708273242"    

    n1 = BigNumber("14654165.46484")
    n2 = BigNumber("264556.5474")
    assert n1.divide(n2).toString() == "55" 


def test_mod():
    n1 = BigNumber("5")
    n2 = BigNumber("5.0")
    assert n1.mod(n2).toString() == "0"

    n1 = BigNumber("4654")
    n2 = BigNumber("45")
    assert n1.mod(n2).toString() == "19"   