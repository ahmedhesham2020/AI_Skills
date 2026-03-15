# SOLID Principles — Complete System Design Skill Guide

> A comprehensive reference for engineers who want to design clean, scalable, and maintainable systems using SOLID principles.

---

## 📌 What Are SOLID Principles?

SOLID is an acronym for **five object-oriented design principles** introduced by Robert C. Martin (Uncle Bob). They serve as a blueprint for writing code that is:

- Easy to **understand**
- Easy to **extend**
- Easy to **maintain**
- Easy to **test**
- Resilient to **change**

These principles are not rules — they are **guidelines** that, when applied together, produce systems that scale gracefully as requirements evolve.

| Letter | Principle | Core Idea |
|--------|-----------|-----------|
| **S** | Single Responsibility | One class = one job |
| **O** | Open/Closed | Extend, don't modify |
| **L** | Liskov Substitution | Subtypes must honor contracts |
| **I** | Interface Segregation | Small, focused interfaces |
| **D** | Dependency Inversion | Depend on abstractions |

---

## S — Single Responsibility Principle (SRP)

### Definition
> *"A class should have only one reason to change."*
> — Robert C. Martin

A class or module must be responsible for **one and only one part** of the system's functionality. If a class has multiple responsibilities, changing one responsibility may break or affect the other unintentionally.

### The Problem It Solves
When a class does too many things, it becomes:
- Hard to test (you need to set up unrelated dependencies)
- Fragile (a change in one area breaks another)
- Difficult to reuse (you pull in unnecessary logic)

### ❌ Violation Example

```python
class UserManager:
    def get_user(self, user_id):
        # Fetches user from DB
        pass

    def format_user_report(self, user):
        # Formats a user into a report string
        pass

    def send_email(self, user, message):
        # Sends an email to the user
        pass

    def save_to_database(self, user):
        # Saves user to database
        pass
```

**Why it's wrong:** `UserManager` is doing 4 completely different jobs — data access, formatting, emailing, and persistence. A change to the email system forces you to touch the same class as the DB logic.

### ✅ Correct Example

```python
class UserRepository:
    def get_user(self, user_id): pass
    def save(self, user): pass

class UserReportFormatter:
    def format(self, user): pass

class EmailService:
    def send(self, to, message): pass
```

**Why it's correct:** Each class has one clear job. You can change the email provider without touching DB logic, and vice versa.

### System Design Application

In large systems, SRP maps to **service boundaries**:
- A `PaymentService` should only handle payment processing
- A `NotificationService` should only handle sending alerts
- An `AuthService` should only handle authentication

This is also the foundation of **microservices** — each service owns one domain.

### When to Apply
- When a class has more than one reason to change
- When testing a class requires setting up unrelated mocks
- When two developers need to frequently edit the same class for different reasons

---

## O — Open/Closed Principle (OCP)

### Definition
> *"Software entities should be open for extension, but closed for modification."*
> — Bertrand Meyer, popularized by Robert C. Martin

Once a class is written and tested, you should be able to **add new behavior** by extending it — not by editing its existing code. This protects working code from being broken by new requirements.

### The Problem It Solves
When you constantly edit existing classes to add features:
- You risk introducing bugs in already-working code
- Every change requires re-testing everything
- The codebase becomes unstable over time

### ❌ Violation Example

```python
class DiscountCalculator:
    def calculate(self, customer_type, price):
        if customer_type == "regular":
            return price * 0.95
        elif customer_type == "premium":
            return price * 0.85
        elif customer_type == "vip":          # Added later — modifying existing code!
            return price * 0.70
```

**Why it's wrong:** Every time a new customer type is added, you edit the same method. This risks breaking existing discount logic and requires re-testing the entire function.

### ✅ Correct Example

```python
from abc import ABC, abstractmethod

class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, price: float) -> float:
        pass

class RegularDiscount(DiscountStrategy):
    def apply(self, price):
        return price * 0.95

class PremiumDiscount(DiscountStrategy):
    def apply(self, price):
        return price * 0.85

class VIPDiscount(DiscountStrategy):       # New type added WITHOUT touching existing code
    def apply(self, price):
        return price * 0.70

class DiscountCalculator:
    def calculate(self, strategy: DiscountStrategy, price: float) -> float:
        return strategy.apply(price)
```

**Why it's correct:** Adding a new discount type means creating a new class, not editing existing ones. The `DiscountCalculator` never changes.

### System Design Application

OCP applies at the **architecture level** through:
- **Plugin systems** — applications that accept new modules without core code changes
- **Payment gateways** — new providers are added as adapters without modifying checkout logic
- **Feature flags** — new features are injected, not hardcoded into existing flows
- **Middleware pipelines** — new processing steps are added to a chain, not inserted into existing handlers

### Techniques to Achieve OCP
| Technique | How It Helps |
|-----------|-------------|
| Abstract classes / Interfaces | Define contracts, extend via new implementations |
| Strategy Pattern | Swap behaviors at runtime |
| Decorator Pattern | Add behavior by wrapping existing classes |
| Dependency Injection | Inject new implementations without touching consumers |

### When to Apply
- When adding a new "type" forces you to edit a core class
- When your `if/else` or `switch` chains grow with every new feature
- When you want to protect stable, tested code from regression

---

## L — Liskov Substitution Principle (LSP)

### Definition
> *"Objects of a superclass should be replaceable with objects of a subclass without altering the correctness of the program."*
> — Barbara Liskov, 1987

If class `B` extends class `A`, then anywhere `A` is used, `B` must work correctly **without the caller knowing the difference**. Subclasses must **honor the contract** established by their parent.

### The Problem It Solves
Without LSP, inheritance becomes a trap:
- Subclasses break the behavior callers expect
- You end up writing `instanceof` checks everywhere
- Polymorphism becomes unreliable

### ❌ Violation Example

```python
class Bird:
    def fly(self):
        print("Flying...")

class Eagle(Bird):
    def fly(self):
        print("Eagle soaring high!")   # ✅ Makes sense

class Penguin(Bird):
    def fly(self):
        raise Exception("I can't fly!")  # ❌ Breaks the contract!

def make_bird_fly(bird: Bird):
    bird.fly()   # Crashes when called with Penguin

make_bird_fly(Penguin())  # RUNTIME ERROR
```

**Why it's wrong:** `Penguin` extends `Bird` but violates the expectation that all birds can fly. Substituting `Penguin` where `Bird` is expected breaks the program.

### ✅ Correct Example

```python
from abc import ABC, abstractmethod

class Bird(ABC):
    @abstractmethod
    def move(self): pass

class FlyingBird(Bird):
    def fly(self): pass
    def move(self): self.fly()

class SwimmingBird(Bird):
    def swim(self): pass
    def move(self): self.swim()

class Eagle(FlyingBird):
    def fly(self): print("Eagle soaring!")

class Penguin(SwimmingBird):
    def swim(self): print("Penguin swimming!")

def move_bird(bird: Bird):
    bird.move()   # Works correctly for all birds

move_bird(Eagle())    # Eagle soaring!
move_bird(Penguin())  # Penguin swimming!
```

**Why it's correct:** The hierarchy now accurately models reality. Each subclass fulfills its own contract. Substitution works safely everywhere.

### LSP Contract Rules
A subclass must:
1. **Not strengthen preconditions** — It cannot require *more* than the parent
2. **Not weaken postconditions** — It cannot guarantee *less* than the parent
3. **Not throw new unexpected exceptions** — Only those declared by the parent
4. **Preserve invariants** — Core properties of the parent must still hold

### System Design Application
- **Database drivers** — `MySQLDriver`, `PostgreSQLDriver`, `MongoDriver` should all be interchangeable behind a `DatabaseDriver` interface
- **Storage backends** — `S3Storage`, `LocalStorage`, `GCSStorage` should be substitutable behind a `FileStorage` interface
- **Notification channels** — `EmailNotifier`, `SMSNotifier`, `PushNotifier` should all satisfy a `Notifier` contract

### When to Apply
- When you override a parent method but change its fundamental behavior
- When a subclass needs to throw exceptions the parent doesn't
- When using a base type in a function causes unexpected behavior depending on the subtype

---

## I — Interface Segregation Principle (ISP)

### Definition
> *"No client should be forced to depend on methods it does not use."*
> — Robert C. Martin

Interfaces should be **small and focused**. A class should not be required to implement methods that are irrelevant to its purpose just because they're part of a larger interface.

### The Problem It Solves
Fat interfaces cause:
- Classes implementing empty or dummy methods just to satisfy the interface
- High coupling — a change to one part of the interface forces recompilation of all implementors
- Confusing contracts that mix unrelated concerns

### ❌ Violation Example

```python
from abc import ABC, abstractmethod

class IWorker(ABC):
    @abstractmethod
    def work(self): pass

    @abstractmethod
    def eat(self): pass       # Robots don't eat!

    @abstractmethod
    def sleep(self): pass     # Robots don't sleep!

class HumanWorker(IWorker):
    def work(self): print("Human working")
    def eat(self): print("Human eating")
    def sleep(self): print("Human sleeping")

class RobotWorker(IWorker):
    def work(self): print("Robot working")
    def eat(self): pass       # Forced to implement a meaningless method
    def sleep(self): pass     # Same problem
```

**Why it's wrong:** `RobotWorker` is forced to implement `eat()` and `sleep()` that have no meaning for it. This is noise that can confuse maintainers and cause silent bugs.

### ✅ Correct Example

```python
from abc import ABC, abstractmethod

class IWorkable(ABC):
    @abstractmethod
    def work(self): pass

class IFeedable(ABC):
    @abstractmethod
    def eat(self): pass

class IRestable(ABC):
    @abstractmethod
    def sleep(self): pass

class HumanWorker(IWorkable, IFeedable, IRestable):
    def work(self): print("Human working")
    def eat(self): print("Human eating")
    def sleep(self): print("Human sleeping")

class RobotWorker(IWorkable):             # Only implements what's relevant
    def work(self): print("Robot working")
```

**Why it's correct:** Each interface is focused. `RobotWorker` only implements what applies to it. No dummy methods, no misleading contracts.

### How to Detect ISP Violations
- A class implements an interface but leaves some methods empty or throwing `NotImplementedError`
- You pass an object to a function that uses only 1 of its 10 methods
- A change to an interface forces many unrelated classes to be updated

### System Design Application
ISP directly influences **API design** and **service contracts**:
- Split `IUserService` into `IUserReader` and `IUserWriter` (read/write segregation)
- Split `IReportService` into `IReportGenerator`, `IReportExporter`, `IReportScheduler`
- In REST APIs: group endpoints by concern, not by entity — so consumers only subscribe to what they need

### When to Apply
- When an interface grows beyond 4–5 methods covering different concerns
- When implementors consistently leave methods blank
- When changing one method forces changes in unrelated implementations

---

## D — Dependency Inversion Principle (DIP)

### Definition
> *"High-level modules should not depend on low-level modules. Both should depend on abstractions. Abstractions should not depend on details. Details should depend on abstractions."*
> — Robert C. Martin

Your core business logic (high-level) should **not be coupled to specific implementations** (low-level). Both should communicate through interfaces. This makes it easy to swap implementations without changing business logic.

### The Problem It Solves
When high-level code directly instantiates low-level code:
- You cannot test business logic without spinning up real databases, email servers, etc.
- Changing a vendor (e.g., switching from Stripe to PayPal) forces changes deep in business code
- The system becomes tightly coupled and brittle

### ❌ Violation Example

```python
class MySQLDatabase:
    def save(self, data):
        print(f"Saving {data} to MySQL")

class OrderService:
    def __init__(self):
        self.db = MySQLDatabase()   # ❌ Directly coupled to MySQL!

    def place_order(self, order):
        self.db.save(order)
```

**Why it's wrong:** `OrderService` (high-level) directly creates and uses `MySQLDatabase` (low-level). Switching to PostgreSQL or a mock in tests requires editing `OrderService` itself.

### ✅ Correct Example

```python
from abc import ABC, abstractmethod

# Abstraction (the contract)
class IDatabase(ABC):
    @abstractmethod
    def save(self, data): pass

# Low-level implementations
class MySQLDatabase(IDatabase):
    def save(self, data):
        print(f"Saving {data} to MySQL")

class PostgreSQLDatabase(IDatabase):
    def save(self, data):
        print(f"Saving {data} to PostgreSQL")

class MockDatabase(IDatabase):        # For testing
    def save(self, data):
        print(f"Mock saving {data}")

# High-level module depends on abstraction, not implementation
class OrderService:
    def __init__(self, db: IDatabase):   # ✅ Injected via interface
        self.db = db

    def place_order(self, order):
        self.db.save(order)

# Wiring (Composition Root)
order_service = OrderService(MySQLDatabase())        # Production
order_service_test = OrderService(MockDatabase())    # Testing
```

**Why it's correct:** `OrderService` never knows about MySQL or PostgreSQL. You can swap databases, add new ones, or use mocks in tests — all without touching `OrderService`.

### Dependency Injection Patterns

| Pattern | Description |
|---------|-------------|
| **Constructor Injection** | Dependency passed via `__init__` (preferred) |
| **Setter Injection** | Dependency set via a method after construction |
| **Interface Injection** | Dependency provided through an interface method |
| **DI Container / IoC** | Framework wires dependencies automatically (Spring, .NET DI) |

### System Design Application

DIP is the foundation of **clean, testable architecture**:
- **Repository Pattern** — `OrderService` depends on `IOrderRepository`, not the actual DB
- **Ports and Adapters (Hexagonal Architecture)** — The core domain defines ports (interfaces); external systems implement adapters
- **Plugin Architecture** — Core app defines contracts; plugins implement and register themselves
- **Event Bus** — Services emit events through an `IEventBus` interface; the actual broker (Kafka, RabbitMQ) is swappable

---

## 🔗 How the SOLID Principles Work Together

The real power of SOLID comes from applying all five principles **in harmony**. Here's how they relate:

```
SRP  ──►  Keeps classes focused          ──►  Easier to apply OCP
OCP  ──►  Extend via new classes         ──►  Requires interfaces (ISP, DIP)
LSP  ──►  Safe substitution              ──►  Makes OCP and DIP reliable
ISP  ──►  Focused interfaces             ──►  Enables clean DIP injection
DIP  ──►  Decouples layers               ──►  Enables OCP and testability
```

### Combined Example — Order Processing System

```python
from abc import ABC, abstractmethod

# ISP: Small focused interfaces
class IOrderRepository(ABC):
    @abstractmethod
    def save(self, order): pass

class IPaymentProcessor(ABC):
    @abstractmethod
    def charge(self, amount, customer): pass

class INotificationSender(ABC):
    @abstractmethod
    def send(self, message, recipient): pass

# SRP: Each class has one job
class SQLOrderRepository(IOrderRepository):
    def save(self, order):
        print(f"Order {order.id} saved to SQL")

class StripePaymentProcessor(IPaymentProcessor):
    def charge(self, amount, customer):
        print(f"Charged {amount} to {customer} via Stripe")

class EmailNotificationSender(INotificationSender):
    def send(self, message, recipient):
        print(f"Email sent to {recipient}: {message}")

# OCP: New processors added without changing OrderService
class PayPalPaymentProcessor(IPaymentProcessor):
    def charge(self, amount, customer):
        print(f"Charged {amount} to {customer} via PayPal")

# DIP: High-level depends on abstractions, not concrete classes
# LSP: Any IPaymentProcessor implementation can be safely substituted
class OrderService:
    def __init__(
        self,
        repo: IOrderRepository,
        payment: IPaymentProcessor,
        notifier: INotificationSender
    ):
        self.repo = repo
        self.payment = payment
        self.notifier = notifier

    def place_order(self, order, customer):
        self.payment.charge(order.total, customer)
        self.repo.save(order)
        self.notifier.send(f"Order {order.id} confirmed!", customer.email)

# Wiring — swap anything without touching OrderService
service = OrderService(
    repo=SQLOrderRepository(),
    payment=PayPalPaymentProcessor(),   # Switched from Stripe — zero changes to OrderService
    notifier=EmailNotificationSender()
)
```

---

## 🏛️ SOLID in Real System Architecture

### Layered Architecture with SOLID

```
┌──────────────────────────────────────────┐
│           Presentation Layer             │  (Controllers, UI)
│         Depends on Use Cases             │
├──────────────────────────────────────────┤
│           Application Layer              │  (Use Cases / Services)
│   SRP: One use case per class            │
│   DIP: Depends on domain interfaces      │
├──────────────────────────────────────────┤
│             Domain Layer                 │  (Entities, Business Rules)
│   OCP: Open to new rules via strategies  │
│   LSP: Subtypes honor domain contracts   │
├──────────────────────────────────────────┤
│          Infrastructure Layer            │  (DB, Email, APIs)
│   ISP: Focused repository interfaces     │
│   DIP: Implements domain interfaces      │
└──────────────────────────────────────────┘
```

### SOLID Mapped to Architecture Patterns

| SOLID Principle | Architecture Pattern |
|----------------|---------------------|
| SRP | Microservices, Bounded Contexts |
| OCP | Plugin Architecture, Strategy Pattern |
| LSP | Ports & Adapters (Hexagonal Architecture) |
| ISP | API Gateway, Event-Driven (subscribe to what you need) |
| DIP | Clean Architecture, Dependency Injection Containers |

---

## ✅ SOLID Design Checklist

Before merging or reviewing code, use this checklist:

### SRP
- [ ] Does this class/service have only one reason to change?
- [ ] Can I describe what this class does in one sentence without using "and"?
- [ ] Are there multiple teams editing this same class for different reasons?

### OCP
- [ ] Can I add a new feature type without modifying existing classes?
- [ ] Are there growing `if/else` or `switch` blocks tied to types?
- [ ] Is existing, tested code protected from new requirement changes?

### LSP
- [ ] Can every subclass replace its parent without breaking callers?
- [ ] Are any methods in subclasses throwing unexpected exceptions?
- [ ] Are there `isinstance()` or `type()` checks in the codebase?

### ISP
- [ ] Are there interfaces with methods that some implementors leave empty?
- [ ] Is each interface focused on a single concern?
- [ ] Do consumers only use the methods they actually need?

### DIP
- [ ] Do high-level modules reference low-level class names directly?
- [ ] Can I test business logic without a real database or network?
- [ ] Are dependencies injected from outside rather than created internally?

---

## 🚫 Common SOLID Mistakes

| Mistake | Description | Fix |
|---------|-------------|-----|
| **Over-engineering** | Applying SOLID to trivial scripts or simple CRUD | Apply proportionally to complexity |
| **Too many tiny classes** | SRP taken to extreme — 1 class per line | Balance cohesion with granularity |
| **Abstraction too early** | Creating interfaces before knowing what varies | Wait for the second implementation before abstracting |
| **LSP ignored in inheritance** | Overriding methods in ways that violate parent contracts | Prefer composition over inheritance |
| **ISP over-segmentation** | Splitting every interface to 1 method | Group methods that always change together |
| **DIP without IoC container** | Manual wiring becomes complex | Use a DI framework at scale |

---

## 📚 Recommended Learning Path

1. **Start with SRP** — It's the easiest to understand and apply immediately
2. **Learn OCP through the Strategy Pattern** — They go hand in hand
3. **Study LSP through Liskov's original paper** — It's more nuanced than it appears
4. **Apply ISP during API and interface design reviews**
5. **Master DIP via Clean Architecture** by Robert C. Martin (book)

### Key Resources
- 📖 *Clean Code* — Robert C. Martin
- 📖 *Clean Architecture* — Robert C. Martin
- 📖 *Design Patterns* — Gang of Four (GoF)
- 📖 *Designing Data-Intensive Applications* — Martin Kleppmann (for systems)

---

*This skill guide was designed to give any engineer — junior or senior — a complete mental model for applying SOLID principles at both the code and system design level.*
