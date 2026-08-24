def say_hello():
    print("hello")

    # def defines a function
    # say_hello is the functions name
    # () shows this function takes no input currently
    # : is the start of the functions instructions
# when indetened that means command is inside the function
# when not indented shows the command is outside the function
say_hello()
# functions lets us packaage and store instructiuons and reuse them with just a call of the functions name
# its liek having a button that will give you a cookie everytime you press it garuenteed
# but right now () is empty so it will always give you the samne cookie, but adding info makes it way more valuble.
def show_number(number):
    print(number)
    # show_number = the function name
    #number = inpt to the function
show_number(5)
# now whatever number we put in the () will be printed out 
# now we will make a function for speed
def show_speed(speed):
    print(speed)
    # show_speed = the function name
    # speed = input to the function
show_speed(9)
# THIS IS VERY VALUABLE, When we start makign the Ptz Controller this allows us to make changes to speed, tilt etc
#Now it is time to make a function that will take multiple inputs
def show_settings(camera, speed):
    print(camera)
    print(speed)
    # show_settings = the function name
    # camera = input to the function
    # speed = input to the function
show_settings(2, 9)
# now we will show movement as a test of functions
def show_movement(camera, pan_speed, tilt_speed):
    print(camera)
    print(pan_speed)
    print(tilt_speed)
    # show_movement = the function name
    # camera = input to the function
    # pan_speed = input to the function
    # tilt_speed = input to the function
show_movement(2, 9, 5)
# right now this function only prints values, but return lets the function give a value back so the rest of the program can use it
def double(number):
    result = number * 2
    return result
answer = double(5) # machine takes number whcih is 5 then multiplys by 2 and returns the result
print(answer)

def add_numbers(a, b):
    result = a + b
    return result
answer = add_numbers(5, 3)
print(answer)
#Next thing is returning a list from a funciton :)
def make_list(a, b, c):
    result = [a, b, c]
    return result
result = make_list(2, 5, 9)
print(result)
# Now we will make a function give it three inputs, [ut those in a list and return the list
def make_settings(camera, pan_speed, tilt_speed):
    result = [camera, pan_speed, tilt_speed]
    return result
result = make_settings(2, 9, 5)
print(result)