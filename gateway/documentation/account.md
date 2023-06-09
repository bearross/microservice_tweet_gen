
# Documentation - Account Service
## Signup
**Function:** User will sign up for their account.  
**URL:** http://localhost:8000/graphql  
**Method:** POST  
**Request Body**
```json
mutation signUpMutation {
    signup(firstName: "Jane", lastName: "Doe", email: "janesss@doe.com", username: "janess@doe.com", password: "password", confirmPassword: "password") {
        token,
        accountId,
        errors {
            key,
            messages
        }
    }
}
```

**Response Example**
```json
{
    "signup": {
        "token": null,
        "accountId": null,
        "errors": [
            {
                "key": "username",
                "messages": [
                    "Username already exists"
                ]
            },
            {
                "key": "email",
                "messages": [
                    "Email already exists"
                ]
            }
        ]
    }
}
```

## Signin
**Function:** User will sign in to their account.  
**URL:** http://localhost:8000/graphql  
**Method:** POST  
**Request Body**
```json
mutation signInMutation {
    signin(username: "janess@doe.com", password: "password"){
        token,
        accountId,
        errors{
            key,
            messages
        }
    }
}
```

**Response Example**
```json
{
    "signin": {
        "token": "f6d915dc-1c4f-4fc9-8f49-2f87ddb7ec1b",
        "accountId": "0966bf69-705f-469c-80ba-546e82ca0f04",
        "errors": null
    }
}
```

## Account Detail
**Function:** User will sign in to their account.  
**URL:** http://localhost:8000/graphql  
**Method:** POST  
**Headers:**
| Name             | Type        | Description |  
| ---------------- | ----------- | ----------- |  
| Authorization    | String      | Auth token provided by sign up/sign in e.g. ```Token 097d93b1-640b-4470-bee9-c698484d8535```|  

**Request Body**
```json
query {
    sessionAccount{
        info {
            accountId,
            firstName,
            lastName,
            email,
            accessLevel,
            status,
            lastLogin,
            joinedOn
        }
    }
}
```

**Response Example**
```json
{
    "sessionAccount": {
        "info": {
            "accountId": "0966bf69-705f-469c-80ba-546e82ca0f04",
            "firstName": "Jane",
            "lastName": "Doe",
            "email": "janesss@doe.com",
            "accessLevel": "0",
            "status": "Registered",
            "lastLogin": "May 05, 2021 - 05:59:29 AM",
            "joinedOn": "May 05, 2021 - 05:59:29 AM"
        }
    }
}
```


## Account Update
**Function:** User will be able to update their account information.  
**URL:** http://localhost:8000/graphql  
**Method:** POST  
**Headers:**
| Name             | Type        | Description |  
| ---------------- | ----------- | ----------- |  
| Authorization    | String      | Auth token provided by sign up/sign in e.g. ```Token 097d93b1-640b-4470-bee9-c698484d8535```|  

**Request Body**
```json
mutation accountUpdateMutation {
    accountUpdate(firstName: "Jane", lastName: "Doe", email: "janesss@doe.com", username: "janess@doe.com", password: "password") {
        account,
        errors {
            key,
            messages
        }
    }
}
```

**Response Example**
```json
{
    "accountUpdate": {
        "account": [
            "Account update successful"
        ],
        "errors": null
    }
}
```


## Password Update
**Function:** User will be able to update their account information.  
**URL:** http://localhost:8000/graphql  
**Method:** POST  
**Headers:**
| Name             | Type        | Description |  
| ---------------- | ----------- | ----------- |  
| Authorization    | String      | Auth token provided by sign up/sign in e.g. ```Token 097d93b1-640b-4470-bee9-c698484d8535```|  

**Request Body**
```json
mutation accountUpdateMutation {
    updatePassword(currentPassword: "passwords", password: "password", confirmPassword: "password") {
        account,
        errors {
            key,
            messages
        }
    }
}
```

**Response Example**
```json
{
    "updatePassword": {
        "account": null,
        "errors": [
            {
                "key": "current_password",
                "messages": [
                    "Invalid current password"
                ]
            }
        ]
    }
}
```


## Forgot Password (Password reset request)
**Function:** User can reset their password by requesting a reset.  
**URL:** http://localhost:8000/graphql  
**Method:** POST  
**Request Body**
```json
mutation forGotMutation {
    forgotPassword(username: "janess@doe.com") {
        resetRequest,
        errors {
            key,
            messages
        }
    }
}
```

**Response Example**
```json
{
    "forgotPassword": {
        "resetRequest": [
            "Request successful! Check email."
        ],
        "errors": null
    }
}
```

## Reset Password
**Function:** User will sign in to their account.  
**URL:** http://localhost:8000/graphql  
**Method:** POST  
**Request Body**
```json
mutation forGotMutation {
    resetPassword(token: "50d58449-f5b1-440b-9843-1e1792b2b8d6", password: "fdsa", confirmPassword: "asdf") {
        passwordReset,
        errors {
            key,
            messages
        }
    }
}
```

**Response Example**
```json
{
    "resetPassword": {
        "passwordReset": null,
        "errors": [
            {
                "key": "token",
                "messages": [
                    "Token invalid"
                ]
            }
        ]
    }
}
```

