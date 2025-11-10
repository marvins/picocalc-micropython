# test_dashboard.py - Test suite for PicoCalc Dashboard
# Run this to verify all components work correctly

import time

import picocalc.colors as colors
from battery import get_status, get_voltage, get_percentage
import menu
import turtle

import ui_temp


def test_battery():
    """Test battery monitoring module"""
    print("=" * 40)
    print("Testing Battery Module")
    print("=" * 40)

    print("\n1. Getting battery status...")
    status = get_status()
    print(f"   Status: {status}")

    print("\n2. Getting voltage...")
    voltage = get_voltage()
    print(f"   Voltage: {voltage}V")

    print("\n3. Getting percentage...")
    pct = get_percentage()
    print(f"   Percentage: {pct}%")

    print("\n✓ Battery module OK")
    return True

def test_ui():
    """Test UI components"""
    print("\n" + "=" * 40)
    print("Testing UI Module")
    print("=" * 40)

    print("\n1. Clearing screen...")
    turtle.fill( colors.RGB_565.BLACK )

    print("2. Drawing text...")
    turtle.draw_text("Test", 10, 10, colors.RGB_565.WHITE )
    ui_temp.center_text("Centered Test", 50, ui_temp.COLOR_GREEN)
    time.sleep(1)

    print("3. Drawing battery icon...")
    battery_status = get_status()
    ui_temp.draw_battery_status(10, 100, battery_status)
    time.sleep(1)

    print("4. Drawing progress bar...")
    ui_temp.draw_progress_bar(10, 150, 200, 20, 75, ui_temp.COLOR_GREEN)
    time.sleep(1)

    print("5. Drawing title bar...")
    ui_temp.draw_title_bar("Test Dashboard", battery_status)
    time.sleep(1)

    ui_temp.center_text("UI Test - Press any key", 200, ui_temp.COLOR_YELLOW)

    print("\nScreen updated. Check display.")
    print("Press any key to continue...")
    ui_temp.wait_key_raw()

    print("\n✓ UI module OK")
    return True


def test_fileselect():
    """Test file selector"""
    print("\n" + "=" * 40)
    print("Testing File Selector")
    print("=" * 40)

    from fileselect import select_file

    print("\n1. Checking if select_file is callable...")
    print(f"   Function: {select_file}")

    print("2. Starting file selector (cancel to continue test)...")
    result = select_file(path="/sd", exts=(".py",), title="Test File Selector")

    if result:
        print(f"   Selected: {result}")
    else:
        print("   Cancelled (OK)")

    print("\n✓ File selector OK")
    return True


def test_menu():
    """Test menu system (visual only)"""
    print("\n" + "=" * 40)
    print("Testing Menu System")
    print("=" * 40)

    print("\n1. Importing menu module...")

    print("2. Checking functions exist...")
    assert hasattr(menu, 'main'), "main() not found"
    assert hasattr(menu, 'show_main_menu'), "show_main_menu() not found"
    assert hasattr(menu, 'show_memory_stats'), "show_memory_stats() not found"
    assert hasattr(menu, 'show_battery_details'), "show_battery_details() not found"

    print("\n✓ Menu module OK")
    print("   (Run menu.main() to test interactively)")
    return True

def test_all():
    """Run all tests"""
    print("\n" + "=" * 40)
    print("PicoCalc Dashboard Test Suite")
    print("=" * 40)

    results = []

    # Test battery module
    results.append(("Battery", test_battery()))

    # Test UI module
    results.append(("UI", test_ui()))

    # Test file selector
    results.append(("File Selector", test_fileselect()))

    # Test menu
    results.append(("Menu", test_menu()))

    # Summary
    print("\n" + "=" * 40)
    print("Test Summary")
    print("=" * 40)

    passed = 0
    failed = 0

    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{name:20s} {status}")
        if result:
            passed += 1
        else:
            failed += 1

    print("\n" + "=" * 40)
    print(f"Total: {passed} passed, {failed} failed")
    print("=" * 40)

    if failed == 0:
        print("\n🎉 All tests passed! Dashboard is ready to use.")
        print("\nTo start the dashboard, run:")
        print(">>> from menu import main")
        print(">>> main()")
    else:
        print("\n⚠️  Some tests failed. Check errors above.")

    return failed == 0


# Run tests if executed directly
if __name__ == "__main__":
    test_all()
