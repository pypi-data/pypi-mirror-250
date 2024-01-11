import sys
sys.path.append("src/")

import pytest

from ulflib import scoping


class TestScoping:
  """Basic unit tests for scoping algorithm.
  
  Notes
  -----
  TODO: these unit tests need to be validated and expanded further.
  """
  def test_1(self):
    ulf = ['John.name', [['past', 'tell.v'], 'Mary.name', 'something.pro']]
    scoped = ['past', ['John.name', ['tell.v', 'Mary.name', 'something.pro']]]
    assert scoping.scope(ulf) == scoped

  def test_2(self):
    ulf = ['John.name', [['past', 'tell.v'], 'Mary.name', ['that', ['he.pro', [['pres', 'go.v'], ['to.p', ['the.d', 'store.n']]]]]]]
    scoped = ['past', ['John.name', ['tell.v', 'Mary.name', ['that', ['pres', ['the', '?x', ['?x', 'store.n'], ['he.pro', ['go.v', ['to.p', '?x']]]]]]]]]
    assert scoping.scope(ulf) == scoped

  def test_3(self):
    ulf = ['she.pro', [['past', 'perf'], [['pasv', 'give.v'], ['an.d', 'award.n']]]]
    scoped = [['past', 'perf'], ['a{n}', '?x', ['?x', 'award.n'], ['she.pro', [['pasv', 'give.v'], '?x']]]]
    assert scoping.scope(ulf) == scoped

  def test_4(self):
    ulf = ['Mary.name', [['pres', 'prog'], ['try.v', ['to', ['ignore.v', ['an.d', 'itch.n']]]]]]
    scoped = [['pres', 'prog'], ['a{n}', '?x', ['?x', 'itch.n'], ['Mary.name', ['try.v', ['to', ['ignore.v', '?x']]]]]]
    assert scoping.scope(ulf) == scoped

  def test_5(self):
    ['n+preds', 'block.n', ['on.p', 'it.pro']]
    ulf = ['John.name', [['past', 'tell.v'], 'Mary.name',
                         ['that', ['he.pro', [['pres', 'go.v'], ['to.p', ['the.d',
                                                [':l', '?x', [['?x', 'store.n'], 'and.cc', ['?x', ['near.p', ['the.d', 'corner.n']]]]]]]]]]]]
    scoped = ['past', ['John.name', ['tell.v', 'Mary.name',
                                     ['that', ['pres', ['the', '?x1', [['?x1', 'store.n'], 'and.cc',
                                                          ['the', '?x12', ['?x12', 'corner.n'], ['?x1', ['near.p', '?x12']]]],
                                                            ['he.pro', ['go.v', ['to.p', '?x1']]]]]]]]]
    assert scoping.scope(ulf) == scoped
    

class TestOptionalKeywords():
  def test_1(self):
    ulf = ['John.name', [['past', 'tell.v'], 'Mary.name', ['that', ['he.pro', [['pres', 'go.v'], ['to.p', ['the.d', 'store.n']]]]]]]
    scoped = ['past', ['John.name', ['tell.v', 'Mary.name', ['that', ['pres', ['he.pro', ['go.v', ['to.p', ['the.d', 'store.n']]]]]]]]]
    assert scoping.scope(ulf, types=['tense']) == scoped

  def test_2(self):
    ulf = ['John.name', [['past', 'tell.v'], 'Mary.name', ['that', ['he.pro', [['pres', 'go.v'], ['to.p', ['the.d', 'store.n']]]]]]]
    scoped = ['the', '?x', ['?x', 'store.n'], ['John.name', [['past', 'tell.v'], 'Mary.name', ['that', ['he.pro', [['pres', 'go.v'], ['to.p', '?x']]]]]]]
    print(scoping.scope(ulf, types=['quan']))
    assert scoping.scope(ulf, types=['quan']) == scoped