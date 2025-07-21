import asyncio
import logging
from typing import AsyncGenerator, Coroutine
from django.conf import settings
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium_stealth import stealth

from cache import Cache


logger = logging.getLogger(__name__)

cache = Cache(settings.CACHE_EXPIRY)


async def gather_with_concurrency(
    n: int,
    *coroutines: list[Coroutine],
) -> AsyncGenerator[Coroutine]:
    semaphore = asyncio.Semaphore(n)

    async def coroutine_with_semaphore(coroutine):
        async with semaphore:
            return await coroutine

    async for coroutine in asyncio.as_completed(
        (coroutine_with_semaphore(c) for c in coroutines)
    ):
        yield coroutine.result()


class WebpageGetter:

    async def get(
        self,
        urls: list[str],
        wait_for_class: str = None,
        delay_between_page_loads: int = 0,
        max_concurrent_requests: int = 0,
    ) -> AsyncGenerator[str]:

        if max_concurrent_requests > 0:
            logger.debug(f"Using max concurrency of {max_concurrent_requests}")
            tasks = [
                self._fetch_page(url, wait_for_class=wait_for_class) for url in urls
            ]
            # Use gather_with_concurrency to limit the number of concurrent requests
            async for result in gather_with_concurrency(
                max_concurrent_requests, *tasks
            ):
                yield result
            return

        for url in urls:
            page_content = await self._fetch_page(url, wait_for_class=wait_for_class)

            yield page_content

            if delay_between_page_loads > 0:
                logger.info(
                    f"Waiting {delay_between_page_loads} seconds before next page..."
                )
                await asyncio.sleep(delay_between_page_loads)

    async def _fetch_page(
        self,
        url,
        wait_for_class: str = None,
    ) -> str:
        if settings.USE_CACHE:
            # Check if the URL is cached
            cached_content = await asyncio.to_thread(
                lambda: cache.get(url, ignore_expiry=True)
            )
            if cached_content:
                logger.debug(f"Using cached content for {url}")
                return cached_content

            if settings.USE_CACHE_ONLY:
                logger.debug(f"Cache only mode enabled, skipping fetch for {url}")
                return ""

        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--disable-extensions")

        driver = webdriver.Chrome(options=options)
        stealth(
            driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )

        logger.debug(f"Fetching {url}")
        await asyncio.to_thread(lambda: driver.get(url))

        try:
            if wait_for_class:
                # Wait for a specific element to be present
                wait_for = (By.CLASS_NAME, wait_for_class)
            else:
                # Wait for the page to load completely
                wait_for = (By.TAG_NAME, "body")

            WebDriverWait(driver, 20).until(EC.presence_of_element_located(wait_for))

        except TimeoutException as e:
            logger.warning(f"Timeout while waiting for {url}")
            logger.debug(driver.page_source)

        finally:
            source = driver.page_source
            driver.quit()

        if settings.USE_CACHE:
            # Cache the fetched content
            cache.set(url, source)

        logger.debug(f"Fetched {url} successfully")
        return source
