# daisy-sms
Simple daisy sms api wrapper

## Installation

    pip install daisy-sms

## Examples

#### Rent a number

```python
from daisy_sms.client import DaisySmsClient, Service

API_KEY = "YOUR_API_KEY"

client = DaisySmsClient(API_KEY)
client.rent_number(Service.TINDER, 0.40)
```

#### Rent multiple numbers

```python
from daisy_sms.client import DaisySmsClient, Service


API_KEY = "YOUR_API_KEY"

client = DaisySmsClient(API_KEY)
list_of_rentals = client.rent_multiple_numbers(Service.TINDER, 10, 0.40)
for rental in list_of_rentals:
    print(rental.id)
    print(rental.number)
```

#### Get code

```python
from daisy_sms.client import DaisySmsClient, Service
from daisy_sms.models import ActivationStatus
import time

API_KEY = "YOUR_API_KEY"

client = DaisySmsClient(API_KEY)
rent_number_response = client.rent_number(Service.TINDER, 0.40)
get_code_response = client.get_code(rent_number_response.id)
time.sleep(30)
if get_code_response.status == ActivationStatus.STATUS_OK:
    print(get_code_response.code)
```

#### Error handling

```python
from daisy_sms.client import DaisySmsClient, Service
from daisy_sms.exceptions import NotEnoughBalanceLeftError


API_KEY = "YOUR_API_KEY"

client = DaisySmsClient(API_KEY)
try:
    rent_number_response = client.rent_number(Service.TINDER, 0.40)
except NotEnoughBalanceLeftError as e:
    print(e.message)

```

This project, **daisy-sms**, is licensed under the MIT License.  
See the [LICENSE](./LICENSE) file for details.