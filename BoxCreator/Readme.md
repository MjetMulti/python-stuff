# Box Creator #
#### Version 0.1 ####

- create text based boxes
- add content to the created boxes
- use custom symbols for borders

## Example: ##
```python
# create main box with 3 smaller boxes inside
a = Display()
a.boxInBox(2,15,5,50)
a.boxInBox(5,9,15,25)
a.boxInBox(7,18,3,58)
# create a sub box for content (with no border) and put content in it
x = Box(1,4,8,3)
x.addContent(0,0,"12345678")
x.addContent(1,0,"TESTTEXT")
x.addContent(2,0,"12345678")
# add the sub box to the main box
a.content["TestBox"] = x
# save the main box in the file "boxsavefile.txt"
a.saveBox()
# open the saved box
with open("boxsavefile.txt", "r", encoding = 'utf-8') as file:
	xe = json.load(file)
	b = Display(**xe) # unpack the dictionary that is saved to recreate the box
# get the string version of the box and print it
print(b.insertContent())
```