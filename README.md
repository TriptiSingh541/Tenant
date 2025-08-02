**Tananat – API Access Control with Circuit Breaker (Django)**
Tananat is a robust backend system built with Django that offers:
- API access control via user roles & hierarchical access
- Circuit breaker logic to protect against repeated failures from external services
- Redis integration for caching & fault tolerance
-Secure user authentication and role-based authorization

---

## Features

- Custom Django middleware for Circuit Breaker
- Class-based API views for scalable endpoints
- Redis-based state management
- JSON-structured logging for traceability
- Password hashing and Google OAuth support

**Setup Instructions**
1. **Clone the repo:**
   git clone https://github.com/TriptiSingh541/tananat.git
   cd tananat
2.Install dependencies
   pip install -r requirements.txt
3.Apply migrations
  python manage.py migrate   
4.Run the server
  python manage.py runserver 
  
