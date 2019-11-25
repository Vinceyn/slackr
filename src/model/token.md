# Tokens
We will be using JSON web tokens with the HMAC-SHA256 hashing algorithm.

Our payload is of the form:
```json
{
	"jti": <randomly generated session ID>,
	"uid": <user's u_id>
}
```

Upon login, a new `jti` is generated and stored in the data store; on logout, the `jti` is removed from the store.

Use auth_check_token(token) to check a token validity and return the user's u_id
