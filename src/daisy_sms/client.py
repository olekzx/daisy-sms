import re
import requests
from .service import Service
from .models import RentNumberResponse, GetCodeResponse, ActivationStatus, ServiceDetails
from .exceptions import MaxPriceExceededError, NoNumbersLeftError, TooManyActiveRentalsError, NotEnoughBalanceLeftError, \
    BadServiceError, WrongRentalIdError, RentalMissingError, InvalidApiKeyError


class DaisySmsClient:
    def __init__(self, api_key: str):
        self._api_key = api_key

    def get_balance(self) -> float:
        r = requests.get(f"https://daisysms.com/stubs/handler_api.php?api_key={self._api_key}&action=getBalance")
        r.raise_for_status()
        return float(r.text.split(":")[1])

    def rent_number(self, service: Service, max_price: float) -> RentNumberResponse:
        r = requests.get(
            f"https://daisysms.com/stubs/handler_api.php?api_key={self._api_key}&action=getNumber&service={service.value}&max_price={max_price:.2f}")
        if r.text == "MAX_PRICE_EXCEEDED":
            raise MaxPriceExceededError
        elif r.text == "NO_NUMBERS":
            raise NoNumbersLeftError
        elif r.text == "TOO_MANY_ACTIVE_RENTALS":
            raise TooManyActiveRentalsError
        elif r.text == "NO_MONEY":
            raise NotEnoughBalanceLeftError
        elif r.text == "BAD_SERVICE":
            raise BadServiceError
        elif r.text.startswith("ACCESS_BALANCE"):
            raise InvalidApiKeyError
        data = r.text.split(":")
        rental_id = int(data[1])
        number = int(data[2])
        return RentNumberResponse(rental_id, number)

    def rent_multiple_numbers(self, service: Service, count: int, max_price: float) -> list[RentNumberResponse]:
        r = requests.get(
            f"https://daisysms.com/stubs/multi/reserve?apikey={self._api_key}&service={service.value}&count={count}&max_price={max_price}")
        if r.text == "MAX_PRICE_EXCEEDED":
            raise MaxPriceExceededError
        elif r.text == "NO_NUMBERS":
            raise NoNumbersLeftError
        elif r.text == "TOO_MANY_ACTIVE_RENTALS":
            raise TooManyActiveRentalsError
        elif r.text == "NO_MONEY":
            raise NotEnoughBalanceLeftError
        elif r.text == "BAD_SERVICE":
            raise BadServiceError
        elif r.text == "":
            raise NotEnoughBalanceLeftError
        elif r.text.startswith("ACCESS_BALANCE"):
            raise InvalidApiKeyError
        id_pattern = r'[?&]id=([^&]+)'
        number_pattern = r'^[^-]+'
        rentals = []
        for rental in r.text.split():
            match = re.search(id_pattern, rental)
            id = match.group(1)
            match = re.match(number_pattern, rental)
            number = match.group(0)
            rentals.append(RentNumberResponse(id, int(number)))
        return rentals

    def rent_number_long_term(self, service: Service, auto_renew: bool = False) -> RentNumberResponse:
        r = requests.get(
            f"https://daisysms.com/stubs/handler_api.php?api_key={self._api_key}&action=getNumber&service={service.value}&ltr=1{'&auto_renew=1' if auto_renew else ''}")
        if r.text == "NO_MONEY":
            raise NotEnoughBalanceLeftError
        elif r.text == "BAD_SERVICE":
            raise BadServiceError
        elif r.text == "NO_NUMBERS":
            raise NoNumbersLeftError
        elif r.text == "TOO_MANY_ACTIVE_RENTALS":
            raise TooManyActiveRentalsError
        elif r.text.startswith("ACCESS_BALANCE"):
            raise InvalidApiKeyError
        data = r.text.split(":")
        rental_id = int(data[1])
        number = int(data[2])
        return RentNumberResponse(rental_id, number)

    def change_auto_renew(self, id: int, value: bool) -> None:
        r = requests.get(
            f"https://daisysms.com/stubs/handler_api.php?api_key={self._api_key}&action=setAutoRenew&id={id}&value={value}")
        if r.text == "BAD_REQUEST":
            raise WrongRentalIdError
        elif r.text.startswith("ACCESS_BALANCE"):
            raise InvalidApiKeyError

    def get_code(self, id: int) -> GetCodeResponse:
        r = requests.get(f"https://daisysms.com/stubs/handler_api.php?api_key={self._api_key}&action=getStatus&id={id}")
        if r.text == "NO_ACTIVATION":
            raise WrongRentalIdError
        elif r.text == "STATUS_WAIT_CODE":
            return GetCodeResponse(ActivationStatus.STATUS_WAIT_CODE)
        elif r.text == "STATUS_CANCEL":
            return GetCodeResponse(ActivationStatus.STATUS_CANCEL)
        elif r.text.startswith("ACCESS_BALANCE"):
            raise InvalidApiKeyError
        code = int(r.text.split(":")[1])
        return GetCodeResponse(ActivationStatus.STATUS_OK, code)

    def mark_rental_as_done(self, id: int) -> None:
        r = requests.get(
            f"https://daisysms.com/stubs/handler_api.php?api_key={self._api_key}&action=setStatus&id={id}&status=6")
        if r.text == "NO_ACTIVATION":
            raise WrongRentalIdError
        elif r.text.startswith("ACCESS_BALANCE"):
            raise InvalidApiKeyError

    def cancel_rental(self, id: int) -> None:
        r = requests.get(
            f"https://daisysms.com/stubs/handler_api.php?api_key={self._api_key}&action=setStatus&id={id}&status=8")
        if r.text == "ACCESS_READY":
            raise RentalMissingError
        elif r.text == "BAD_ID":
            raise WrongRentalIdError
        elif r.text.startswith("ACCESS_BALANCE"):
            raise InvalidApiKeyError

    def get_prices(self) -> list[ServiceDetails]:
        r = requests.get(f"https://daisysms.com/stubs/handler_api.php?api_key={self._api_key}&action=getPrices")
        services = []
        if r.text.startswith("ACCESS_BALANCE"):
            raise InvalidApiKeyError
        data = r.json()["187"]
        for key in data.keys():
            key_data = data[key]
            services.append(
                ServiceDetails("187", key, key_data.get("name"), key_data.get("count"), key_data.get("cost"),
                               key_data.get("repeatable")))
        return services
