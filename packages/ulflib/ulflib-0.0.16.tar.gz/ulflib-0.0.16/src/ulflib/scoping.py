"""Functions for scoping a ULF formula."""

from transduction import tt
from memoization import cached

from ulflib.util import atom, variablep, listp, append, occurs_in, occurs_properly_in, subst, rec_remove, flatten_singletons, new_var
from ulflib.ulflib import (det_term_p, coord_p, coord_sent_p, tensed_sent_p, nonsubsective_premodified_verb_p, sent_p, pred_p, verbal_sent_p,
                           neg_non_verbal_sent_p, neg_sent_p, non_neg_modified_sent_p, tense_or_aspect_marker_p, tensed_verb_p,
                           premodified_verbal_sent_p, sent_or_tensed_sent_p, lambda_p, lex_function_p, find_vp_head, split_by_suffix)

# ``````````````````````````````````````
# TT Scoped LF Patterns
# ``````````````````````````````````````



QUANTIFIER = ['all', 'some', 'a', 'a{n}', 'most', 'few', 'many', 'the', 'this', 'these', 'those']
DEFAULT_TYPES = ['tense', 'quan', 'coord']


@cached
def scoped_tensed_sent_p(x):
  return listp(x) and len(x) == 2 and tense_or_aspect_marker_p(x[0]) and sent_p(x[1])


@cached
def scoped_quant_sent_p(x):
  return listp(x) and ((len(x) == 3 and x[0] in QUANTIFIER and (sent_p(x[2]) or tensed_sent_p(x[2]))) or
                       (len(x) == 4 and x[0] in QUANTIFIER and (sent_p(x[2]) or tensed_sent_p(x[2])) and
                        (sent_p(x[3]) or tensed_sent_p(x[3]))))


SCOPED_PREDS = [
  scoped_tensed_sent_p,
  scoped_quant_sent_p,
]

for pred in SCOPED_PREDS:
  tt.register_pred(pred, include_neg=True)



# ``````````````````````````````````````
# Helper Functions
# ``````````````````````````````````````



def occurs_free_in(atm, expr, bound_vars=[]):
  """Check if `atm` occurs in `expr`, without being bound therein by lambda or a scoped quantifier.
  
  The optional `bound_vars` are gathered as we work our way downward to the parts of `expr` recursively.
  """
  if atm in bound_vars:
    return False
  elif atom(expr):
    return True if atm == expr else False
  else:
    bound_vars1 = bound_vars
    if lambda_p(expr) or (expr[0] in QUANTIFIER and atom(expr[1])):
      bound_vars1.append(expr[1])
    return any([occurs_free_in(atm, xpr, bound_vars1) for xpr in expr])



def subst_for_free(val, x, expr):
  """Substitute `val` for all free occurrences of atom `x` in `expr`."""
  if expr == x:
    return val
  elif atom(expr):
    return expr
  elif not occurs_in(x, expr):
    return expr
  # is x bound at the top of expr by a quantifier or :l?
  elif len(expr) >= 3 and variablep(expr[1]) and not lex_function_p(expr[0]):
    # if the bound variable is x, return expr unchanged
    if expr[1] == x:
      return expr
    # if occurs-check is positive, first rename the variable and then substitute recursively
    elif occurs_in(expr[1], val):
      new = new_var([val, expr[1:]])
      renamed_expr = expr[0] + subst_for_free(new, expr[1], expr[1:])
      return [subst_for_free(val, x, y) for y in renamed_expr]
    # the bound variable isn't x, and doesn't occur in val
    else:
      return [subst_for_free(val, x, y) for y in expr]
  # x occurs within expr, but not as a top-level bound variable
  else:
    return [subst_for_free(val, x, y) for y in expr]
  


def to_quantifier(det):
  """Convert a determiner to a particular quantifier (if possible)."""
  if not atom(det):
    return det
  if det in ['a.d', 'an.d']:
    return 'a{n}'
  word, _ = split_by_suffix(det)
  if word and word in QUANTIFIER:
    return word
  else:
    return det

 

# ``````````````````````````````````````
# Scoping Algorithm
# ``````````````````````````````````````



def scope(ulf, types=DEFAULT_TYPES):
  """TBC"""
  candidates = scoping_candidates(ulf)

  if not candidates:
    return [scope_expr(part, types=types) for part in ulf]
  
  expr = wide_scope_winner(candidates)

  if coord_p(expr) and 'coord' in types:
    return scope_coord(expr, ulf, types=types)
  elif det_term_p(expr) and 'quan' in types:
    return scope_quan(expr, ulf, types=types)
  # TODO: should this match just (past pred.v), or the full tensed sentence?
  elif tensed_sent_p(expr) and 'tense' in types:
    return scope_tense(expr, ulf, types=types)
  elif 'coord' in types:
    return scope_coord(expr, ulf, types=types)
  else:
    return [scope_expr(part, types=types) for part in ulf]
  

def scope_expr(ulf, types=DEFAULT_TYPES):
  """Scope an arbitrary ULF expression.
  
  The input `ulf` could be any expression, but we only scope sentences and monadic preds
  (though wff/pred *parts* of other expressions are also scoped by recursion).
  """
  if atom(ulf):
    return ulf
  elif sent_or_tensed_sent_p(ulf):
    return scope(ulf, types=types)
  elif pred_p(ulf):
    return scope_pred(ulf, types=types)
  else:
    return [scope_expr(part, types=types) for part in ulf]
  

def scoping_candidates(ulf):
  """Find accessible unscoped elements, if any, in the given expr.

  Return the expr itself if it is unscoped, followed by the scoping candidates from
  all parts that are *not* scope islands as determined by the island constraints listed in README.md.
  """
  candidates = []

  if atom(ulf):
    return []
  
  # Per island constraints 2 and 4: skip sentence modifiers other than 'not' or already scoped expressions
  if non_neg_modified_sent_p(ulf) or scoped_quant_sent_p(ulf) or scoped_tensed_sent_p(ulf):
    return []
  
  # if ulf consists of 'not' applied to a NONverbal wff, return empty
  # (normally only tense can escape from a negation)
  if neg_non_verbal_sent_p(ulf):
    return []
  
  # if ulf consists of 'not' applied to a wff that has an external unscoped tense operator
  # applied to it, extract the tense expression and return it in a singleton list
  if neg_sent_p(ulf):
    tensed_expr = find_unscoped_tense_expr(ulf[1])
    if tensed_expr:
      return [tensed_expr]
    # failure does not mean there's no unscoped tense; it may be part of the predicate of the wff
  
  # Per island constraint 3: if ulf consists of a nonsubsective predicate modifier applied to a predicate,
  # extract the tense expression of the predicate (if any) and return it as a singleton list
  if nonsubsective_premodified_verb_p(ulf):
    tensed_expr = find_unscoped_tense_expr(ulf[1])
    if tensed_expr:
       return [tensed_expr]
    else:
       return []
    
  # Per island constraint 5: if ulf is an unscoped coordination of wffs, extract only the ulf itself
  if coord_sent_p(ulf):
    return [ulf]
  
  # if ulf is an unscoped quantified term, an unscoped tense-modified expression,
  # or an unscoped coordinated expression, then initiate the candidates with [ulf]
  # TODO: should this match just (past pred.v), or the full tensed sentence?
  if det_term_p(ulf) or tensed_sent_p(ulf) or coord_p(ulf):
    candidates = [ulf]

  # recursively add further candidates
  # Per island constraint 6: if a sub-expression is a verbal wff, we do not process it
  candidates = candidates + append([scoping_candidates(expr) if not (atom(expr) or verbal_sent_p(expr)) else [] for expr in ulf])

  # Per island constraint 1: drop candidates that contain a free variable bound in ulf outside of the candidate
  candidates = [c for c in candidates if not binding_constrained_candidate(c, ulf)]

  return candidates


def binding_constrained_candidate(xp, expr):
  """Determine whether `xp` contains a free variable bound in `expr` outside of itself.
  
  If there is a variable-binding operator at the top level, and the variable it binds occurs
  free in `xp`, return True; otherwise check for each top-level subexpression of `expr` whether
  `xp` occurs in it and is binding-constrained relative to it, returning True if this occurs for
  any of those subexpressions, and False otherwise.
  """
  if atom(xp) or atom(expr):
    return False
  if xp == expr:
    return False
  if not occurs_properly_in(xp, expr):
    return False
  
  # top-level lambda, or top-level scoped quantifier
  if ((lambda_p(expr) and occurs_free_in(expr[1], xp)) or
      (expr[0] in QUANTIFIER and atom(expr[1]) and occurs_free_in(expr[1], xp))):
    return True
  
  # embedded binding operator, outside xp, binding something in xp
  return any([binding_constrained_candidate(xp, xpr) for xpr in expr])
    

def find_unscoped_tense_expr(verbal_pred):
  """Find a top-level or superficially embedded unscoped-tense expression, given a verbal predication.
  
  Usually this expression is just a tensed atomic verb, but some might have non-atomic logical translations.

  This program is necessary because tense tends to scope outside modified verbal predicates *even when the modifier
  is non-subsective* (whereas quantifiers and binary connectives tend to stay inside). For example, in "He almost died",
  it's not that an event of almost-dying-in-the-past happened, but rather, that in the past an event of almost-dying happened.
  In contrast, "He almost solved every problem" is likely to be understood as referring to a near-completion of the entire set
  of problems, rather than a near-completion of each problem individually.
  """
  if atom(verbal_pred):
    return None
  # we do not extract from coordinated expressions
  if coord_p(verbal_pred):
    return None
  # is verbal_pred itself tense-modified?
  if tensed_verb_p(verbal_pred):
    return verbal_pred
  # is verbal_pred a verbal pred applied to at least one argument?
  if verbal_sent_p(verbal_pred):
    vp = verbal_pred[1]
    head = find_vp_head(vp)
    return head if head else find_unscoped_tense_expr(verbal_pred[1])
  # is verbal_pred a modified verbal pred?
  if premodified_verbal_sent_p(verbal_pred):
    return find_unscoped_tense_expr(verbal_pred[1])
  # lambda abstract forming a verbal pred?
  if lambda_p(verbal_pred):
    lexpr = verbal_pred[2]
    # is this an abstraction from another verbal pred or an uncoordinated wff?
    if tensed_verb_p(lexpr) or (verbal_sent_p(lexpr) and not coord_p(lexpr)):
      return find_unscoped_tense_expr(lexpr)
  return None
      

def wide_scope_winner(unscoped_elements):
  """Pick the widest-scoping unscoped element in `ulf`.
  
  The given unscoped-elements are in left-to-right order, and
  (justified by the constituent order in unscoped LF) we pick 
  the leftmost as the default, except for giving preference to tense.

  Notes
  -----
  TODO: This function may need to be tweaked, as it's currently taken from the
  original elf-from-sentences code and the ULF tense syntax is slightly different.
  """
  if not unscoped_elements:
    return []
  tense_expr = [x for x in unscoped_elements if tense_or_aspect_marker_p(x)]
  if tense_expr:
    return tense_expr[0]
  else:
    return unscoped_elements[0]
  

def extract_tense(ulf):
  """Extract the tense marker from a ulf.
  """
  if tense_or_aspect_marker_p(ulf):
    return ulf
  elif atom(ulf):
    return None
  else:
    part1 = extract_tense(ulf[0])
    if part1:
      return part1
    else:
      return extract_tense(ulf[1:])
  

def scope_pred(pred, types=DEFAULT_TYPES):
  """Used when no unscoped elements of `pred` can be scoped as part of a larger ULF.
  
  NOTES
  -----
  TODO: we could first check if pred contains any unscoped elements, to avoid reassembling
  pred in that case, but this is not so simple to check, so is not included yet.
  """
  if atom(pred):
    return pred
  
  # Modified pred?
  if len(pred) == 2 and nonsubsective_premodified_verb_p(pred[0]) and pred_p(pred[1]):
    return [scope_expr(pred[0], types=types), scope_pred(pred[1], types=types)]

  # Lambda predicate?
  if lambda_p(pred):
    return [pred[0], pred[1], scope(pred[2], types=types)]

  # Nonmonadic pred applied to term(s)?
  # TODO: the following was copied from the original scoping method, but it appears to create
  # an infinite recursion. I'm not entirely sure what the intended purpose of the lambda is.
  # if len(pred) >= 2 and pred_p(pred):
  #   var = new_var(pred)
  #   return [':l', var, scope([var, pred], types=types)]
  # TODO: the following needs to be carefully validated
  if listp(pred) and len(pred) >= 2 and pred_p(pred):
    inner = scope(pred[1:], types=types)
    if scoped_quant_sent_p(inner):
      return [pred[0], inner]
    return [pred[0]] + inner

  return [scope_expr(p, types=types) for p in pred]


def scope_quan(expr, ulf, types=DEFAULT_TYPES):
  """Scope a ULF of form ``[<quan>, <pred>]``."""
  quan = to_quantifier(expr[0])
  x = new_var(ulf)
  pred = expr[1]
  # Prepare restrictor using new variable as subject
  if atom(pred):
    restr = [x, pred]
  elif lambda_p(pred):
    restr = subst_for_free(x, pred[1], pred[2])
  elif pred_p(pred):
    restr = [x] + pred
  else:
    restr = [x, pred]
  # Is restr actually the body of (unrestricted) ulf?
  if expr == ulf:
    return [quan, x, scope(restr, types=types)]
  # ulf is restricted
  else:
    return [quan, x, scope(restr, types=types), scope(subst(x, expr, ulf), types=types)]


def scope_tense(expr, ulf, types=DEFAULT_TYPES):
  """Scope a ULF of form ``[<tense>, <expr>]``."""
  tense = extract_tense(expr)
  if not tense: # unexpected
    return ulf
  sent = flatten_singletons(rec_remove(tense, expr))
  if expr == ulf:
    return scope([tense, sent], types=types)
  else:
    return [tense, scope(subst(sent, expr, ulf), types=types)]


def scope_coord(expr, ulf, types=DEFAULT_TYPES):
  """Scope a ULF of form ``[<expr1>, <coord>, <expr2>, ...]``."""
  # Top-level sentence coordination
  if expr == ulf:
    return [scope(expr[0], types=types), expr[1]] + [scope(xp, types=types) for xp in expr[2:]]
  else:
    return [scope(subst(expr[0], expr, ulf), types=types), expr[1]] + [scope(subst(xp, expr, ulf), types=types) for xp in expr[2:]]