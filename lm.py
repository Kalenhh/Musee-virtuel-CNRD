#coding:utf-8

text = "Je m’appelle André BESSIERE et j’ai 17 ans. Je commence ce carnet aujourd’hui, 30 août 1939. Qu’est-ce que je vais pouvoir raconter, à part qu’il fait terriblement chaud. La première idée qui me vient à l’esprit et qui me fait écrire est le silence gêné de mes parents quand j’évoque la situation actuelle. Je ne suis pas fou, j’ai 13 ans et je suis un des meilleurs de ma classe. La presse le montre bien, la situation est très tendue et je vois les adultes se parler en douce pour ne pas que j’entende. Mais je sens bien au collège que la situation a changé depuis très peu de temps…"

def format(string) :

	print(string)
	string.replace(" ","\n")
	print(string)

	formated_text = ""
	max_char = 30
	c = 0 
	last_space = 0 # index

	for i in range(len(string)) :

		c += 1

		if string[i] == " " and c > max_char :
			string = string[:i] + "\n" + string[i+1:]
			c = 0






	return string

print(format(text))
