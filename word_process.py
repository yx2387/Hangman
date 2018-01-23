# Process the word list
# Remove the words that has numbers/special characters

f = open("words.txt","r")
print f
myList = []

for line in f:
	if line.strip().isalpha():
		myList.append(line)
print len(myList)
f = open("english_words.txt",'w')
for i in myList:
	f.write(i)