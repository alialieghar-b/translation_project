"""Question: Create a class ChainOfResponsibility that uses the Chain of Responsibility
pattern to pass a request along a chain of handlers.
Implement handlers HandlerA and HandlerB.
"""

# LEARNING CHALLENGE
#
# Before looking at any solution below, please try to solve this yourself first!
#
# Tips for success:
# - Read the question carefully
# - Think about what classes and methods you need
# - Start with a simple implementation
# - Test your code step by step
# - Don't worry if it's not perfect - learning is a process!
#
# Remember: The best way to learn programming is by doing, not by reading solutions!
#
# Take your time, experiment, and enjoy the learning process!

# Try to implement your solution here:
# (Write your code below this line)































# HINT SECTION (Only look if you're really stuck!)
#
# Think about:
# - What is the Chain of Responsibility pattern and when is it useful?
# - How do you link handlers together in a chain?
# - How does each handler decide whether to process or pass the request?
# - What happens when no handler can process the request?
#
# Remember: Start simple and build up complexity gradually!


# ===============================================================================
#                           STEP-BY-STEP SOLUTION
# ===============================================================================
#
# CLASSROOM-STYLE WALKTHROUGH
#
# Let's solve this problem step by step, just like in a programming class!
# Each step builds upon the previous one, so you can follow along and understand
# the complete thought process.
#
# ===============================================================================


# Step 1: Define the base Handler class
# ===============================================================================

# Explanation:
# Let's start by creating the base Handler class. This class defines the interface
# for handling requests and maintains a reference to the next handler in the chain.

class Handler:
    def __init__(self, successor=None):
        self._successor = successor

    def handle(self, request):
        if self._successor:
            self._successor.handle(request)

# What we accomplished in this step:
# - Created base Handler class with successor reference
# - Added basic handle method that passes requests to the next handler


# Step 2: Create concrete handler classes
# ===============================================================================

# Explanation:
# Now let's create concrete handler classes that inherit from Handler and
# implement specific handling logic for different types of requests.

class Handler:
    def __init__(self, successor=None):
        self._successor = successor

    def handle(self, request):
        if self._successor:
            self._successor.handle(request)

class HandlerA(Handler):
    def handle(self, request):
        if request == "A":
            print("HandlerA handled request")
        else:
            super().handle(request)

class HandlerB(Handler):
    def handle(self, request):
        if request == "B":
            print("HandlerB handled request")
        else:
            super().handle(request)

# What we accomplished in this step:
# - Created HandlerA and HandlerB that inherit from Handler
# - Each handler checks if it can handle the request, otherwise passes it along


# Step 3: Test our basic Chain of Responsibility pattern
# ===============================================================================

# Explanation:
# Let's test our Chain of Responsibility pattern by creating a chain of handlers
# and sending different requests through it.

class Handler:
    def __init__(self, successor=None):
        self._successor = successor

    def handle(self, request):
        if self._successor:
            self._successor.handle(request)

class HandlerA(Handler):
    def handle(self, request):
        if request == "A":
            print("HandlerA handled request")
        else:
            super().handle(request)

class HandlerB(Handler):
    def handle(self, request):
        if request == "B":
            print("HandlerB handled request")
        else:
            super().handle(request)

# Test our basic Chain of Responsibility pattern:
print("=== Testing Basic Chain of Responsibility Pattern ===")

handler_chain = HandlerA(HandlerB())

print("Sending request 'A':")
handler_chain.handle("A")

print("\nSending request 'B':")
handler_chain.handle("B")

print("\nSending request 'C' (unhandled):")
handler_chain.handle("C")
print("(No output - request was not handled)")

# What we accomplished in this step:
# - Created a chain with HandlerA -> HandlerB
# - Tested different requests to see how they flow through the chain
# - Demonstrated what happens when no handler can process a request


# Step 4: Enhanced Chain of Responsibility with support system
# ===============================================================================

# Explanation:
# Let's create a more sophisticated example with a support ticket system
# that routes requests based on priority and complexity.

class SupportRequest:
    def __init__(self, request_type, priority, description):
        self.request_type = request_type
        self.priority = priority  # 1=low, 2=medium, 3=high, 4=critical
        self.description = description
        self.handled_by = None

    def __str__(self):
        return f"{self.request_type} (Priority {self.priority}): {self.description}"

class SupportHandler:
    def __init__(self, name, successor=None):
        self.name = name
        self._successor = successor

    def handle(self, request):
        if self.can_handle(request):
            self.process_request(request)
            request.handled_by = self.name
        elif self._successor:
            print(f"{self.name} cannot handle request, passing to next handler")
            self._successor.handle(request)
        else:
            print(f"No handler available for request: {request}")

    def can_handle(self, request):
        raise NotImplementedError("Subclasses must implement can_handle")

    def process_request(self, request):
        print(f"{self.name} is processing: {request}")

class Level1Support(SupportHandler):
    def can_handle(self, request):
        return request.priority <= 1 and request.request_type in ["password_reset", "account_question"]

class Level2Support(SupportHandler):
    def can_handle(self, request):
        return request.priority <= 2 and request.request_type in ["software_issue", "billing_question"]

class Level3Support(SupportHandler):
    def can_handle(self, request):
        return request.priority <= 3 and request.request_type in ["technical_issue", "integration_problem"]

class ManagerSupport(SupportHandler):
    def can_handle(self, request):
        return request.priority == 4  # Critical issues only

class EscalationHandler(SupportHandler):
    def can_handle(self, request):
        return True  # Handles everything as last resort

    def process_request(self, request):
        print(f"{self.name} escalating unhandled request: {request}")

# Test enhanced Chain of Responsibility:
print("\n=== Enhanced Chain of Responsibility with Support System ===")

# Build the support chain
support_chain = Level1Support("Level 1 Support",
    Level2Support("Level 2 Support",
        Level3Support("Level 3 Support",
            ManagerSupport("Manager Support",
                EscalationHandler("Escalation Team")))))

# Test different types of requests
requests = [
    SupportRequest("password_reset", 1, "User forgot password"),
    SupportRequest("software_issue", 2, "Application crashes on startup"),
    SupportRequest("technical_issue", 3, "Database connection problems"),
    SupportRequest("system_outage", 4, "Complete system failure"),
    SupportRequest("unknown_issue", 2, "Strange behavior in system"),
]

print("Processing support requests:")
for request in requests:
    print(f"\n--- Processing: {request} ---")
    support_chain.handle(request)
    if request.handled_by:
        print(f"✓ Handled by: {request.handled_by}")
    else:
        print("✗ Request was not handled")

# What we accomplished in this step:
# - Created realistic support ticket system with multiple handler levels
# - Added request objects with properties for decision making
# - Implemented escalation chain with fallback handler
# - Demonstrated how chain handles different types and priorities


# ===============================================================================
# CONGRATULATIONS!
#
# You've successfully completed the step-by-step solution!
#
# Key concepts learned:
# - Understanding the Chain of Responsibility pattern and its benefits
# - Creating chains of handlers that can process or pass requests
# - Implementing early termination when a handler processes the request
# - Building escalation chains for support systems
# - Understanding when to use Chain of Responsibility vs other patterns
#
# Try it yourself:
# 1. Start with Step 1 and code along
# 2. Test each step before moving to the next
# 3. Understand WHY each step is necessary
# 4. Experiment with modifications (try creating a validation chain!)
#
# Remember: The best way to learn is by doing!
# ===============================================================================
