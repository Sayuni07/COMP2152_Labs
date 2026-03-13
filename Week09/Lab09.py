# ============================================================
#  WEEK 09 LAB — Q1: SYSTEM INFORMATION REPORTER
#  COMP2152 — Sayuni Wimaladharma
# ============================================================

import os
import sys
import platform


# --- Helper (provided) — error handling example from Week 06 ---
def display(title, data):
    print(f"\n--- {title} ---")
    for k, v in data.items():
        print(f"  {k:<12} : {v}")


def safe_run(label, func, *args):
    try:
        result = func(*args)
        if result is None:
            print(f"  [!] {label} returned None — missing return?")
            return {}
        return result
    except Exception as e:
        print(f"  [ERROR] {label}: {e}")
        return {}


# TODO: Complete get_system_info()
#   Return a dict with keys: "os", "node", "release", "machine"
#   Use: platform.system(), platform.node(),
#        platform.release(), platform.machine()
def get_system_info():
    return {
        "os": platform.system(),
        "node": platform.node(),
        "release": platform.release(),
        "machine": platform.machine(),

    }
    

# TODO: Complete get_python_info()
#   Return a dict with keys: "version", "executable", "platform"
#   Use: sys.version, sys.executable, sys.platform
def get_python_info():
    return {
        "version": sys.version,
        "executable": sys.executable,
        "platform": sys.platform, 

    }
   

# TODO: Complete get_directory_info(path)
#   Return a dict with keys: "path", "exists", "file_count", "is_directory"
#   Use: os.path.abspath(), os.path.exists(),
#        os.listdir() (count items), os.path.isdir()
def get_directory_info(path):
    return {
        "path": os.path.abspath(path),
        "exists": os.path.exists(path),
        "file_count": len(os.listdir(path)) if os.path.exists(path) else 0,
        "is_directory":os.path.isdir(path), 
    }

# --- Main (provided) ---
if __name__ == "__main__":
    print("=" * 60)
    print("  SYSTEM INFORMATION REPORTER")
    print("=" * 60)

    info = safe_run("System Info", get_system_info)
    if info: display("System Info", info)

    info = safe_run("Python Info", get_python_info)
    if info: display("Python Info", info)

    info = safe_run("Directory Info", get_directory_info, ".")
    if info: display("Directory Info for '.'", info)

    print("\n" + "=" * 60)

# ============================================================
#  WEEK 09 LAB — Q2: SEQUENTIAL vs THREADED EXECUTION
#  COMP2152 — Sayuni Wimaladharma
# ============================================================

import time
import threading


# TODO: Complete simulate_task(name, duration, lock)
#   1. lock.acquire(), print(f"[START] {name}"), lock.release()
#   2. time.sleep(duration)
#   3. lock.acquire(), print(f"[DONE]  {name} ({duration}s)"), lock.release()
def simulate_task(name, duration, lock):
    lock.acquire()
    print(f"[START] {name}")
    lock.release()
    time.sleep(duration)
    lock.acquire()
    print(f"[DONE] {name} ({duration}s)")
    lock.release()

    

# TODO: Complete run_threaded(tasks, lock)
#   1. Create an empty list: threads = []
#   2. For each (name, duration) in tasks:
#        t = threading.Thread(target=simulate_task, args=(name, duration, lock))
#        threads.append(t)
#   3. Loop to start all threads
#   4. Loop to join  all threads  (separate loop!)
def run_threaded(tasks, lock):
    threads = []
    for name, duration in tasks:
        t = threading.Thread(target=simulate_task, args=(name, duration, lock))
        threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        t.join() 


# --- Provided below — error handling example from Week 06 ---

def run_sequential(tasks, lock):
    for name, duration in tasks:
        simulate_task(name, duration, lock)


if __name__ == "__main__":
    print("=" * 60)
    print("  SEQUENTIAL vs THREADED EXECUTION")
    print("=" * 60)

    tasks = [("Brew Coffee", 3), ("Toast Bread", 2), ("Fry Eggs", 4)]
    lock = threading.Lock()

    print("\n--- Running SEQUENTIALLY ---")
    try:
        t0 = time.time()
        run_sequential(tasks, lock)
        seq = time.time() - t0
        print(f"Sequential time: {seq:.2f} seconds")
    except Exception as e:
        print(f"[ERROR] {e}")
        seq = None

    print("\n--- Running with THREADS ---")
    try:
        t0 = time.time()
        run_threaded(tasks, lock)
        thr = time.time() - t0
        print(f"Threaded time: {thr:.2f} seconds")
    except Exception as e:
        print(f"[ERROR] {e}")
        thr = None

    if seq and thr and thr > 0:
        print(f"\nSpeedup: {seq / thr:.2f}x faster with threads!")

    print("\n" + "=" * 60)

    # ============================================================
#  WEEK 09 LAB — Q3: UNIT TESTING
#  COMP2152 — [Your Name Here]
# ============================================================

import unittest


# --- Functions to test (provided) ---
# Error handling example from Week 06 is inside is_valid_ip().

def celsius_to_fahrenheit(c):
    """Convert Celsius to Fahrenheit: c * 9/5 + 32"""
    return c * 9 / 5 + 32


def is_valid_ip(address):
    """Return True if address is a valid IPv4 string (4 octets, 0-255)."""
    try:
        parts = address.split(".")
        if len(parts) != 4:
            return False
        for p in parts:
            if int(p) < 0 or int(p) > 255:
                return False
        return True
    except (ValueError, AttributeError):
        return False


def fizzbuzz(n):
    """Return 'FizzBuzz', 'Fizz', 'Buzz', or str(n)."""
    if n % 15 == 0: return "FizzBuzz"
    if n % 3 == 0:  return "Fizz"
    if n % 5 == 0:  return "Buzz"
    return str(n)


# TODO: Complete TestCelsius
#   test_freezing  → celsius_to_fahrenheit(0)   == 32.0
#   test_boiling   → celsius_to_fahrenheit(100) == 212.0
#   test_negative  → celsius_to_fahrenheit(-40) == -40.0
class TestCelsius(unittest.TestCase):
    def test_freezing(self):
        self.assertEqual(celsius_to_fahrenheit(0), 32.0)
    def test_boiling(self):
        self.assertEqual(celsius_to_fahrenheit(100), 212.0)
    def test_negative(self):
        self.assertEqual(celsius_to_fahrenheit(-40), -40.0)       



# TODO: Complete TestValidIP
#   test_valid         → is_valid_ip("192.168.1.1") is True
#   test_invalid_octet → is_valid_ip("256.1.1.1")   is False
#   test_too_few_parts → is_valid_ip("1.2.3")       is False
#   test_empty         → is_valid_ip("")            is False
class TestValidIP(unittest.TestCase):
    def test_valid(self):
        self.assertTrue(is_valid_ip("10.10.10.10"))
    def test_invalid_octet(self):
        self.assertFalse(is_valid_ip("258.10.10.10"))
    def test_too_few_parts(self):
        self.assertFalse(is_valid_ip("10.10.10"))
    def test_empty(self):
        self.assertFalse(is_valid_ip(""))

    
# TODO: Complete TestFizzBuzz
#   test_fizz     → fizzbuzz(3)  == "Fizz"
#   test_buzz     → fizzbuzz(5)  == "Buzz"
#   test_fizzbuzz → fizzbuzz(15) == "FizzBuzz"
#   test_number   → fizzbuzz(7)  == "7"
class TestFizzBuzz(unittest.TestCase):
    def test_fizz(self):
        self.assertEqual(fizzbuzz(3), "Fizz")
    def test_buzz(self):
        self.assertEqual(fizzbuzz(5), "Buzz")
    def test_fizzbuzz(self):
        self.assertEqual(fizzbuzz(15), "FizzBuzz")
    def test_number(self):
        self.assertEqual(fizzbuzz(7), "7")       


if __name__ == "__main__":
    unittest.main()