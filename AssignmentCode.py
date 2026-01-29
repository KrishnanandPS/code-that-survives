from abc import ABC, abstractmethod
from datetime import datetime
import functools


class AppConfig:
    # SINGLETON PATTERN
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.app_name = "MiniCab"
            cls._instance.currency_symbol = "₹"
        return cls._instance


class PricingStrategy(ABC):
    # STRATEGY PATTERN - Pricing
    @abstractmethod
    def calculate_fare(self, distance_km: float) -> float:
        pass


class NormalPricing(PricingStrategy):
    def calculate_fare(self, distance_km: float) -> float:
        return distance_km * 10


class SurgePricing(PricingStrategy):
    def calculate_fare(self, distance_km: float) -> float:
        return distance_km * 25


class PaymentMethod(ABC):
    # STRATEGY PATTERN - Payment
    @abstractmethod
    def process_payment(self, amount: float) -> bool:
        pass


class UPIPayment(PaymentMethod):
    def process_payment(self, amount: float) -> bool:
        print(f"UPI payment of {AppConfig().currency_symbol}{amount:.2f} - Success!")
        return True


class CardPayment(PaymentMethod):
    def process_payment(self, amount: float) -> bool:
        print(f"Card payment of {AppConfig().currency_symbol}{amount:.2f} - Success!")
        return True


class WalletPayment(PaymentMethod):
    def process_payment(self, amount: float) -> bool:
        print(f"Wallet payment of {AppConfig().currency_symbol}{amount:.2f} - Success!")
        return True


def authenticate(func):
    # DECORATOR PATTERN - Authentication
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        print(f"\n[AUTH] User: {self.user_name}")
        if not self.is_authenticated:
            print("[AUTH] Failed - Not logged in!\n")
            return None
        print("[AUTH] Success!")
        return func(self, *args, **kwargs)
    return wrapper


def log_operation(func):
    # DECORATOR PATTERN - Logging
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        print(f"[LOG] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Booking started")
        result = func(self, *args, **kwargs)
        status = "Success" if result else "Failed"
        print(f"[LOG] Booking {status}\n")
        return result
    return wrapper


class CabBookingSystem:
    def __init__(self, user_name: str, is_authenticated: bool = True):
        self.user_name = user_name
        self.is_authenticated = is_authenticated
        self.pricing_strategy = None
        self.payment_method = None
        self.config = AppConfig()
    
    def set_pricing(self, strategy: PricingStrategy):
        self.pricing_strategy = strategy
    
    def set_payment(self, method: PaymentMethod):
        self.payment_method = method
    
    @authenticate
    @log_operation
    def book_ride(self, pickup: str, destination: str, distance_km: float):
        if not self.pricing_strategy or not self.payment_method:
            print("[ERROR] Set pricing and payment method first!")
            return None
        
        fare = self.pricing_strategy.calculate_fare(distance_km)
        print(f"\nRide: {pickup} → {destination} ({distance_km} km)")
        print(f"Fare: {self.config.currency_symbol}{fare:.2f}")
        
        if self.payment_method.process_payment(fare):
            return {"pickup": pickup, "destination": destination, "fare": fare}
        return None


if __name__ == "__main__":
    print("=" * 60)
    print(f"Welcome to {AppConfig().app_name}")
    print("=" * 60)
    
    print("\n### SCENARIO 1: Normal Pricing + UPI ###")
    system = CabBookingSystem("John")
    system.set_pricing(NormalPricing())
    system.set_payment(UPIPayment())
    system.book_ride("MG Road", "Koramangala", 5.0)
    
    print("\n### SCENARIO 2: Surge Pricing + Card ###")
    system.set_pricing(SurgePricing())
    system.set_payment(CardPayment())
    system.book_ride("Airport", "Whitefield", 15.0)
    
    print("\n### SCENARIO 3: Normal Pricing + Wallet ###")
    system.set_pricing(NormalPricing())
    system.set_payment(WalletPayment())
    system.book_ride("Indiranagar", "HSR Layout", 8.0)
    
    print("\n### SCENARIO 4: Unauthenticated User ###")
    failed_system = CabBookingSystem("Jane", is_authenticated=False)
    failed_system.set_pricing(NormalPricing())
    failed_system.set_payment(UPIPayment())
    failed_system.book_ride("Jayanagar", "BTM", 6.0)
    
    print("\n### SINGLETON DEMO ###")
    config1, config2 = AppConfig(), AppConfig()
    print(f"Same instance: {config1 is config2}")
    print(f"App: {config1.app_name}, Currency: {config1.currency_symbol}")
