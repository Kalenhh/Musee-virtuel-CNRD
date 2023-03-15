#coding:utf-8

text = "There are many variations of passages of Lorem Ipsum available\n, but the majority have suffered alteration in some form, by injected humour, or randomised words which don't look even slightly believable. If you are going to use a passage of Lorem Ipsum, you need to be sure there isn't anything embarrassing hidden in the middle of text. All the Lorem Ipsum generators on the Internet tend to repeat predefined chunks as necessary, making this the first true generator on the Internet. It uses a dictionary of over 200 Latin words, combined with a handful of model sentence structures, to generate Lorem Ipsum which looks reasonable. The generated Lorem Ipsum is therefore always free from repetition, injected humour, or non-characteristic words etc."


def format(string) :

	print(string)
	string.replace(" ","\n")
	print(string)
	formated_text = ""
	max_char = 30
	c = 0 

	for i in string :
		if len(string) <= max_char :
			formated_text+=string+"\n"
			break
		if c > max_char and string[c] == ' ' :
			formated_text += string[:c]+"\n"
			string = string[c:]
			c = 0 
		c+= 1

	return formated_text

print(format(text))
