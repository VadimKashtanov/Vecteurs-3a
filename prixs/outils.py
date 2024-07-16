def direct(x):
	return x

def ema(l,K=1):
	_ema = [l[0]]
	for e in l[1:]:
		_ema += [_ema[-1] * (1 - 1/K) + e*(1/K)]
	return _ema

def macd(x, e):
	e > 0.0
	ema12 = ema(x, e*12)
	ema26 = ema(x, e*26)
	__macd = [a-b for a,b in zip(ema12,ema26)]
	ema9 = ema(__macd, 9*e)
	return [a-b for a,b in zip(__macd, ema9)]

def chiffre(x, __chiffre):
	ret = []
	for _x in x:
		ch = (int(_x)%__chiffre)/__chiffre
		ret += [2*(0.5 - (ch if ch <= 0.5 else 1-ch))]
	return ret