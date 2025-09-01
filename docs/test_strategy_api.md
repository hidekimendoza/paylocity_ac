# API Testing 

## 1. API info
* POST, GET, PUT: /api/Employees
* DEL, GET: /api/Employees/{id}"

# Schema (Employee)
Required:
* **firstName**: str [0-50]
* **lastName**: str [0-50]
* **username**: str [0-50]

Other properties:
* **partitionKey**: str, ro, nullable
* **sortKey**: str, uuid, ro
* **username**: str [0-50]
* **id**: str, uuid
* **firstName**: str [0-50]
* **lastName**: str [0-50]
* **dependants**: int32 [0-32]
* **expiration**: date-time str, nullable
* **salary**: float
* **gross**: float, ro
* **benefitCost**: float, ro
* **net**: float, ro

## Testing tools
The API testing will be executed utilizing pytest and requests.

## 2. Features to Be Tested 
### 2.1 CRUD Operations
Create
* Successful creation of new resources with valid data payloads.
* Verification of HTTP 200 Created status code and correct response body structure.
* Validation of newly created resource's presence and accuracy in subsequent GET requests.

Read
* Retrieval of individual resources by ID.
* Retrieval of lists of resources with various pagination and filtering parameters.?
* Verification of HTTP 200 OK status code and accurate data in the response body.
Testing edge cases for reading (e.g., non-existent IDs, empty lists).

Update (PUT/PATCH)
* Successful modification of existing resources with valid partial and full data payloads.
* Verification of HTTP 200 OK status code and updated resource data in subsequent GET requests.

Delete
* Successful deletion of existing resources.
* Verification of No Content or 200 OK status code.
* Confirmation that the deleted resource is no longer retrievable (e.g., subsequent GET returns 404 Not Found).
* Data Consistency: Ensuring data consistency across related API endpoints (e.g., creating an order updates product stock).


### 2.2 Parameter and Schema Validation 

Request Parameter Validation:

* Sending requests with valid and invalid query parameters, path parameters, and request headers.
* Testing for missing required parameters.
* Verification of appropriate error responses (e.g., 400 Bad Request) for invalid inputs.
* Request Body Schema Validation:
* Sending requests with valid, malformed, and incomplete JSON/XML payloads.
* Verification that the API rejects invalid payloads with relevant error messages and 400 Bad Request status.

Response Body Schema Validation:
* Automated validation of all API responses against expected JSON/XML schemas, ensuring correct data types, field names, and presence of required fields. .

### 2.3. Authentication and Authorization

Authentication:
* Testing protected endpoints with valid and invalid authentication credentials (e.g., API keys, tokens).
* Verification of 401 Unauthorized for unauthenticated access.
Authorization:
* Testing access control for different user roles (e.g., admin, regular user) to ensure users can only access resources they are permitted to.
* Verification of 403 Forbidden for unauthorized access attempts.

### 2.4. Error Handling

* Invalid Endpoints: Sending requests to non-existent API endpoints to verify 404 Not Found responses.
* Server Errors: Testing scenarios that might trigger server-side errors (e.g., malformed database queries through API input) to ensure graceful 5xx responses and informative internal logging.
* Rate Limiting: Testing API behavior when request limits are exceeded (if applicable) and verifying 429 Too Many Requests status.

### 2.5. Basic Performance Checks

* Latency Measurement: Recording response times for critical API endpoints under normal load.
* Throughput Simulation: Using Postman's collection runner to send a burst of requests to key endpoints to get an initial indication of API resilience and performance.

### 2.6. Data Sanitization (Security)
* Attempting to inject common malicious patterns (e.g., SQL injection strings, cross-site scripting (XSS) payloads) into input fields of POST/PUT requests.
* Verifying that the API either rejects these inputs or sanitizes them effectively, preventing security vulnerabilities.

## 3. Features Not to Be Tested
* Load and Stress Testing:
* Security and Penetration Testing: