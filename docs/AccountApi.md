# kodexa.client.AccountApi

All URIs are relative to *https://lehua.kodexa.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**activate_user**](AccountApi.md#activate_user) | **PUT** /api/account/activation/{activationToken} | 
[**authenticate_user**](AccountApi.md#authenticate_user) | **POST** /api/account/signin | 
[**complete_password_reset**](AccountApi.md#complete_password_reset) | **POST** /api/account/completePasswordReset | 
[**get_activation**](AccountApi.md#get_activation) | **GET** /api/account/activation/{activationToken} | 
[**get_me**](AccountApi.md#get_me) | **GET** /api/account/me | 
[**get_memberships**](AccountApi.md#get_memberships) | **GET** /api/account/memberships | 
[**get_my_pat**](AccountApi.md#get_my_pat) | **GET** /api/account/me/token | 
[**password_change**](AccountApi.md#password_change) | **POST** /api/account/passwordChange | 
[**password_reset**](AccountApi.md#password_reset) | **POST** /api/account/passwordReset | 
[**redirect_with_redirect_attributes**](AccountApi.md#redirect_with_redirect_attributes) | **POST** /api/account/me/documentationToken | 
[**refresh_jwt_token**](AccountApi.md#refresh_jwt_token) | **POST** /api/account/refreshToken | 
[**regenerate_my_pat**](AccountApi.md#regenerate_my_pat) | **PUT** /api/account/me/token | 
[**register_user**](AccountApi.md#register_user) | **POST** /api/account/register | 
[**update_me**](AccountApi.md#update_me) | **PUT** /api/account/me | 
[**validate_token**](AccountApi.md#validate_token) | **GET** /api/account/accessToken | 


# **activate_user**
> UserActivation activate_user(activation_token, user_activation)



Activate user

### Example

```python
import time
import kodexa.client
from kodexa.client.api import account_api
from kodexa.client.model.user_activation import UserActivation
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = account_api.AccountApi(api_client)
    activation_token = "activationToken_example" # str | 
    user_activation = UserActivation(
        first_name="first_name_example",
        last_name="last_name_example",
        password="password_example",
    ) # UserActivation | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.activate_user(activation_token, user_activation)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling AccountApi->activate_user: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **activation_token** | **str**|  |
 **user_activation** | [**UserActivation**](UserActivation.md)|  |

### Return type

[**UserActivation**](UserActivation.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: */*


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **authenticate_user**
> {str: (bool, date, datetime, dict, float, int, list, str, none_type)} authenticate_user(login_request)



Sign-in (JWT)

### Example

```python
import time
import kodexa.client
from kodexa.client.api import account_api
from kodexa.client.model.login_request import LoginRequest
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = account_api.AccountApi(api_client)
    login_request = LoginRequest(
        email="email_example",
        password="password_example",
    ) # LoginRequest | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.authenticate_user(login_request)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling AccountApi->authenticate_user: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **login_request** | [**LoginRequest**](LoginRequest.md)|  |

### Return type

**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: */*


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **complete_password_reset**
> {str: ({str: (bool, date, datetime, dict, float, int, list, str, none_type)},)} complete_password_reset(complete_password_reset)



Complete password reset

### Example

```python
import time
import kodexa.client
from kodexa.client.api import account_api
from kodexa.client.model.complete_password_reset import CompletePasswordReset
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = account_api.AccountApi(api_client)
    complete_password_reset = CompletePasswordReset(
        reset_token="reset_token_example",
        password="password_example",
    ) # CompletePasswordReset | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.complete_password_reset(complete_password_reset)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling AccountApi->complete_password_reset: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **complete_password_reset** | [**CompletePasswordReset**](CompletePasswordReset.md)|  |

### Return type

**{str: ({str: (bool, date, datetime, dict, float, int, list, str, none_type)},)}**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: */*


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_activation**
> UserActivation get_activation(activation_token)



Create an activation for token

### Example

```python
import time
import kodexa.client
from kodexa.client.api import account_api
from kodexa.client.model.user_activation import UserActivation
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = account_api.AccountApi(api_client)
    activation_token = "activationToken_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_activation(activation_token)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling AccountApi->get_activation: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **activation_token** | **str**|  |

### Return type

[**UserActivation**](UserActivation.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_me**
> User get_me()



Get my user profile information

### Example

```python
import time
import kodexa.client
from kodexa.client.api import account_api
from kodexa.client.model.user import User
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = account_api.AccountApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        api_response = api_instance.get_me()
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling AccountApi->get_me: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

[**User**](User.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_memberships**
> [Membership] get_memberships()



Get my memberships

### Example

```python
import time
import kodexa.client
from kodexa.client.api import account_api
from kodexa.client.model.membership import Membership
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = account_api.AccountApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        api_response = api_instance.get_memberships()
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling AccountApi->get_memberships: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

[**[Membership]**](Membership.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_my_pat**
> str get_my_pat()



Get personal access token

### Example

```python
import time
import kodexa.client
from kodexa.client.api import account_api
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = account_api.AccountApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        api_response = api_instance.get_my_pat()
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling AccountApi->get_my_pat: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **password_change**
> User password_change(password_change)



Change my password

### Example

```python
import time
import kodexa.client
from kodexa.client.api import account_api
from kodexa.client.model.user import User
from kodexa.client.model.password_change import PasswordChange
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = account_api.AccountApi(api_client)
    password_change = PasswordChange(
        old_password="old_password_example",
        new_password="new_password_example",
    ) # PasswordChange | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.password_change(password_change)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling AccountApi->password_change: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **password_change** | [**PasswordChange**](PasswordChange.md)|  |

### Return type

[**User**](User.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: */*


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **password_reset**
> {str: ({str: (bool, date, datetime, dict, float, int, list, str, none_type)},)} password_reset(password_reset)



Start password reset

### Example

```python
import time
import kodexa.client
from kodexa.client.api import account_api
from kodexa.client.model.password_reset import PasswordReset
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = account_api.AccountApi(api_client)
    password_reset = PasswordReset(
        email="email_example",
    ) # PasswordReset | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.password_reset(password_reset)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling AccountApi->password_reset: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **password_reset** | [**PasswordReset**](PasswordReset.md)|  |

### Return type

**{str: ({str: (bool, date, datetime, dict, float, int, list, str, none_type)},)}**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: */*


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **redirect_with_redirect_attributes**
> str redirect_with_redirect_attributes(request_body)



### Example

```python
import time
import kodexa.client
from kodexa.client.api import account_api
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = account_api.AccountApi(api_client)
    request_body = {
        "key": {},
    } # {str: ({str: (bool, date, datetime, dict, float, int, list, str, none_type)},)} | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.redirect_with_redirect_attributes(request_body)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling AccountApi->redirect_with_redirect_attributes: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **request_body** | **{str: ({str: (bool, date, datetime, dict, float, int, list, str, none_type)},)}**|  |

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: */*


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **refresh_jwt_token**
> {str: (bool, date, datetime, dict, float, int, list, str, none_type)} refresh_jwt_token()



Refresh JWT Token

### Example

```python
import time
import kodexa.client
from kodexa.client.api import account_api
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = account_api.AccountApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        api_response = api_instance.refresh_jwt_token()
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling AccountApi->refresh_jwt_token: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **regenerate_my_pat**
> str regenerate_my_pat()



Regenerate personal access token

### Example

```python
import time
import kodexa.client
from kodexa.client.api import account_api
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = account_api.AccountApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        api_response = api_instance.regenerate_my_pat()
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling AccountApi->regenerate_my_pat: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **register_user**
> {str: ({str: (bool, date, datetime, dict, float, int, list, str, none_type)},)} register_user(register_user)



Register for platform

### Example

```python
import time
import kodexa.client
from kodexa.client.api import account_api
from kodexa.client.model.register_user import RegisterUser
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = account_api.AccountApi(api_client)
    register_user = RegisterUser(
        email="email_example",
        first_name="first_name_example",
        last_name="last_name_example",
    ) # RegisterUser | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.register_user(register_user)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling AccountApi->register_user: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **register_user** | [**RegisterUser**](RegisterUser.md)|  |

### Return type

**{str: ({str: (bool, date, datetime, dict, float, int, list, str, none_type)},)}**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: */*


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_me**
> User update_me(user)



Update my profile information

### Example

```python
import time
import kodexa.client
from kodexa.client.api import account_api
from kodexa.client.model.user import User
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = account_api.AccountApi(api_client)
    user = User(
        id="id_example",
        uuid="uuid_example",
        created_on=dateutil_parser('1970-01-01T00:00:00.00Z'),
        updated_on=dateutil_parser('1970-01-01T00:00:00.00Z'),
        created_by="created_by_example",
        updated_by="updated_by_example",
        email="email_example",
        first_name="first_name_example",
        last_name="last_name_example",
        activated=True,
        platform_admin=True,
        password_reset_date=dateutil_parser('1970-01-01T00:00:00.00Z'),
        last_connected=dateutil_parser('1970-01-01T00:00:00.00Z'),
        user_storage=UserStorage(
            favorite_links=[
                FavoriteLink(
                    link="link_example",
                ),
            ],
        ),
    ) # User | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.update_me(user)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling AccountApi->update_me: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user** | [**User**](User.md)|  |

### Return type

[**User**](User.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: */*


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **validate_token**
> AccessTokenDetails validate_token(x_access_token)



Validate an access token

### Example

```python
import time
import kodexa.client
from kodexa.client.api import account_api
from kodexa.client.model.access_token_details import AccessTokenDetails
from pprint import pprint
# Defining the host is optional and defaults to https://lehua.kodexa.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = kodexa.client.Configuration(
    host = "https://lehua.kodexa.ai"
)


# Enter a context with an instance of the API client
with kodexa.client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = account_api.AccountApi(api_client)
    x_access_token = "x-access-token_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.validate_token(x_access_token)
        pprint(api_response)
    except kodexa.client.ApiException as e:
        print("Exception when calling AccountApi->validate_token: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_access_token** | **str**|  |

### Return type

[**AccessTokenDetails**](AccessTokenDetails.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

