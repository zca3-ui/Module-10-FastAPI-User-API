
import subprocess
import sys
import time

import pytest
import requests
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="session")
def fastapi_server():
    """Start the FastAPI server for end-to-end testing."""

    fastapi_process = subprocess.Popen(
        [sys.executable, "main.py"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    server_url = "http://127.0.0.1:8000/"
    timeout = 30
    start_time = time.time()
    server_up = False

    print("Starting FastAPI server...")

    while time.time() - start_time < timeout:

        if fastapi_process.poll() is not None:
            raise RuntimeError("FastAPI server stopped unexpectedly.")

        try:
            response = requests.get(server_url, timeout=2)

            if response.status_code == 200:
                server_up = True
                print("FastAPI server is running.")
                break

        except requests.RequestException:
            pass

        time.sleep(1)

    if not server_up:
        fastapi_process.terminate()
        fastapi_process.wait()
        raise RuntimeError(
            "FastAPI server failed to start within 30 seconds."
        )

    yield

    print("Shutting down FastAPI server...")

    fastapi_process.terminate()

    try:
        fastapi_process.wait(timeout=10)
    except subprocess.TimeoutExpired:
        fastapi_process.kill()
        fastapi_process.wait()

    print("FastAPI server has stopped.")


@pytest.fixture(scope="session")
def playwright_instance_fixture():
    """Create a Playwright instance for browser testing."""

    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture(scope="session")
def browser(playwright_instance_fixture):
    """Launch a headless Chromium browser."""

    browser_instance = playwright_instance_fixture.chromium.launch(
        headless=True
    )

    yield browser_instance

    browser_instance.close()


@pytest.fixture(scope="function")
def page(browser):
    """Create a new browser page for each test."""

    page_instance = browser.new_page()

    yield page_instance

    page_instance.close()
