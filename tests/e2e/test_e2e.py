
import pytest
from playwright.sync_api import Page, expect


BASE_URL = "http://127.0.0.1:8000"


@pytest.mark.e2e
def test_hello_world(page: Page, fastapi_server):
    """Verify that the homepage displays the Hello World heading."""

    page.goto(BASE_URL)

    expect(page.locator("h1")).to_have_text("Hello World")


@pytest.mark.e2e
def test_calculator_add(page: Page, fastapi_server):
    """Verify that the calculator correctly adds two numbers."""

    page.goto(BASE_URL)

    page.locator("#a").fill("10")
    page.locator("#b").fill("5")

    page.get_by_role("button", name="Add").click()

    expect(page.locator("#result")).to_contain_text("Result: 15")


@pytest.mark.e2e
def test_calculator_subtract(page: Page, fastapi_server):
    """Verify that the calculator correctly subtracts two numbers."""

    page.goto(BASE_URL)

    page.locator("#a").fill("10")
    page.locator("#b").fill("5")

    page.get_by_role("button", name="Subtract").click()

    expect(page.locator("#result")).to_contain_text("Result: 5")


@pytest.mark.e2e
def test_calculator_multiply(page: Page, fastapi_server):
    """Verify that the calculator correctly multiplies two numbers."""

    page.goto(BASE_URL)

    page.locator("#a").fill("10")
    page.locator("#b").fill("5")

    page.get_by_role("button", name="Multiply").click()

    expect(page.locator("#result")).to_contain_text("Result: 50")


@pytest.mark.e2e
def test_calculator_divide(page: Page, fastapi_server):
    """Verify that the calculator correctly divides two numbers."""

    page.goto(BASE_URL)

    page.locator("#a").fill("10")
    page.locator("#b").fill("5")

    page.get_by_role("button", name="Divide").click()

    expect(page.locator("#result")).to_contain_text("Result: 2")


@pytest.mark.e2e
def test_calculator_divide_by_zero(page: Page, fastapi_server):
    """Verify that dividing by zero displays an error."""

    page.goto(BASE_URL)

    page.locator("#a").fill("10")
    page.locator("#b").fill("0")

    page.get_by_role("button", name="Divide").click()

    expect(page.locator("#result")).to_contain_text(
        "Error: Cannot divide by zero!"
    )
