import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium_stealth import stealth

from cache import Cache


cache = Cache(60 * 60 * 24)  # Cache for 24 hours


async def gather_with_concurrency(n, *coros):
    semaphore = asyncio.Semaphore(n)

    async def sem_coro(coro):
        async with semaphore:
            return await coro

    return await asyncio.gather(*(sem_coro(c) for c in coros))


class WebpageGetter:

    async def get(
        self,
        urls: list[str],
        wait_for_class: str = None,
        delay_between_page_loads: int = 0,
        max_concurrent_requests: int = 0,
        cache_only: bool = False,
    ) -> list[str]:

        if max_concurrent_requests > 0:
            print(f"Using max concurrency of {max_concurrent_requests}")
            tasks = [
                self._fetch_page(
                    url, wait_for_class=wait_for_class, cache_only=cache_only
                )
                for url in urls
            ]
            results = await gather_with_concurrency(max_concurrent_requests, *tasks)
            return results

        results = []
        for url in urls:
            page_content = await self._fetch_page(
                url, wait_for_class=wait_for_class, cache_only=cache_only
            )

            results.append(page_content)

            if delay_between_page_loads > 0:
                print(f"Waiting {delay_between_page_loads} seconds before next page...")
                await asyncio.sleep(delay_between_page_loads)

        return results

    async def _fetch_page(
        self,
        url,
        wait_for_class: str = None,
        cache_only: bool = False,
    ) -> str:
        # Check if the URL is cached
        cached_content = await asyncio.to_thread(lambda: cache.get(url))
        if cached_content:
            print(f"Using cached content for {url}")
            return cached_content

        if cache_only:
            print(f"Cache only mode enabled, skipping fetch for {url}")
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

        print(f"Fetching {url}")
        await asyncio.to_thread(lambda: driver.get(url))

        try:
            if wait_for_class:
                # Wait for a specific element to be present
                wait_for = (By.CLASS_NAME, wait_for_class)
            else:
                # Wait for the page to load completely
                wait_for = (By.TAG_NAME, "body")

            WebDriverWait(driver, 10).until(EC.presence_of_element_located(wait_for))

        except TimeoutException as e:
            print(f"Timeout while waiting for {url}")
            print(driver.page_source)
            raise e

        finally:
            source = driver.page_source
            driver.quit()

        # Cache the fetched content
        cache.set(url, source)

        print(f"Fetched {url} successfully")
        return source
