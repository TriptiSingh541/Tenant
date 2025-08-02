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
**API endpoint**
1.For AuthApp - Authentication & Permission
 Endpoint-auth/check_permission/ for checking user permission access
2.Tenant -User invitations & dashbaords.
  Endpoint- api/invite/ -->> for create a user invitation.
  Endpoint-api/invite/accept/   --->>> for  accepting invitation via toekn/link
  Endpoint-api/invite/cancel/ --->>> for cancelling the invitation
  Endpoint- api/dashboard/   --->> for project /user dashboard
  Endpoint-- api/dashboard_logging/ -->>> for viewing logging info on dashboard
  
