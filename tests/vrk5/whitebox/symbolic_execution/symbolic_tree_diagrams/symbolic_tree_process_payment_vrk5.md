# Symbolic Tree: process_payment(amount, simulate)

N1: amount <= 0 ?
  True  -> FAIL(reason=AMOUNT)
  False -> N2

N2: simulate == 'timeout' ?
  True  -> FAIL(reason=TIMEOUT)
  False -> N3

N3: simulate == 'insufficient' ?
  True  -> FAIL(reason=FUNDS)
  False -> N4

N4: simulate == 'fraud' ?
  True  -> FAIL(reason=FRAUD)
  False -> SUCCESS
