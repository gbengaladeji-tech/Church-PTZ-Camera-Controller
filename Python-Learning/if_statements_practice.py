speed = 3

if speed > 5:
    print("fast")
    # we now just made an if statment which in short terms lets the machie make the desicion for us deppending on the value
    # right now if the speed exceeds 5 it will print fast, but anything below, and it will print nothing
else:
    print("slow")
    # now we added an else statment which is what the machine will do if the if statment is not true, in this case it will print slow   
    speed = 9

    if speed <= 5:
        print("slow")
    elif speed <= 10:
        print("medium")
    else:
        print("fast")
              #elif allows us to check for another condition
speed = 4

if 1 <= speed <= 18:
    print("valid speed")
else:
    print("invalid speed")
    # this command allows us to set a range
#now lets try making an if statment
speed = 5
if 1 <= speed <= 18:
    print("valid speed")
else:
    print("invalid speed")
# now it is time to combine functions and if statments, be happy.
# we will be making a function that checks the speed we give it
def check_speed(speed):
    if 1<= speed <= 18:
        print("valid speed")
    else:
        print("invalid speed")
check_speed(5)
check_speed(19)
# Now remeber minecraft with those true and false game rules? Right now we will be doing just that
def check_speed(speed):
    if 1<= speed <= 18:
        return True
    else:
        return False
result = check_speed(5)
print(result)
# now if conditions are met we get a tru statment in the terminal, but if they are not we get a false statment
