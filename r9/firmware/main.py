# Intentional boot-safe entry point. No physical camera traffic.
from target import Target
target = Target(38400)
target.safe()
print("PTZ R9 ready for disconnected diagnostics; camera TX disabled")
