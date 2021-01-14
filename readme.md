1. add user using /register
2. get credentials using POST on /auth:
{
    "username": "joe",
    "password": "pass"
}

3. to any other request add header: 
Authorization: JWT <%>token from above>