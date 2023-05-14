def Título(txt, c="=", m=0):
	if m == 0:
		tam = len(txt) + 4
		print(f"\n{c*tam}")
		print(f"{c} {txt} {c}")
		print(f"{c*tam}\n")
	elif m == 1:
		print(f"\n{c} {txt} {c}\n")