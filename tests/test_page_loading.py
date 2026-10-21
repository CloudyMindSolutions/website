import asyncio
import functools
import json
import os
from pathlib import Path
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
import unittest

from playwright.async_api import async_playwright, expect


ROOT = Path(__file__).resolve().parents[1]
PAGES = sorted(
    path.relative_to(ROOT).as_posix()
    for path in ROOT.rglob("*.html")
    if not any(part.startswith(".") for part in path.relative_to(ROOT).parts)
)
BACKGROUNDS = {"light": "rgb(248, 250, 252)", "dark": "rgb(15, 23, 42)"}


class SiteHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass


class PageLoadingTests(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        handler = functools.partial(SiteHandler, directory=str(ROOT))
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
        cls.server_thread = Thread(target=cls.server.serve_forever, daemon=True)
        cls.server_thread.start()
        cls.base_url = f"http://127.0.0.1:{cls.server.server_port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.server_thread.join()

    async def asyncSetUp(self):
        self.playwright = await async_playwright().start()
        self.addAsyncCleanup(self.playwright.stop)
        self.browser = await self.playwright.chromium.launch(
            channel=os.environ.get("BROWSER_CHANNEL") or None
        )
        self.addAsyncCleanup(self.browser.close)

    async def assert_render_without_main_script(self, path, system_theme, saved_theme):
        context = await self.browser.new_context(color_scheme=system_theme)
        if saved_theme is not None:
            await context.add_init_script(
                f"localStorage.setItem('cloudymind-theme', {json.dumps(saved_theme)});"
            )
        release_script = asyncio.Event()
        script_requested = asyncio.Event()

        async def hold_script(route):
            script_requested.set()
            await release_script.wait()
            await route.continue_()

        await context.route("**/js/main.js", hold_script)
        page = await context.new_page()
        errors = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        expected_theme = system_theme
        if saved_theme:
            expected_theme = "dark" if saved_theme == "dark" else "light"
        try:
            response = await page.goto(f"{self.base_url}/{path}", wait_until="commit")
            self.assertEqual(response.status, 200)
            await asyncio.wait_for(script_requested.wait(), timeout=5)
            await expect(page.locator("main")).to_be_visible(timeout=3000)
            await page.wait_for_function(
                "performance.getEntriesByName('first-contentful-paint').length > 0",
                timeout=3000,
            )
            await expect(page.locator("html")).to_have_css(
                "background-color", BACKGROUNDS[expected_theme]
            )
            self.assertEqual(await page.evaluate("document.readyState"), "interactive")
            self.assertEqual(
                await page.evaluate(
                    "performance.getEntriesByType('resource')"
                    ".filter(entry => entry.name.endsWith('/js/main.js')).length"
                ),
                0,
            )
        finally:
            release_script.set()
            await page.wait_for_load_state()
            await context.close()
        self.assertEqual(errors, [])

    async def test_every_page_paints_before_external_script_arrives(self):
        self.assertTrue(PAGES)
        for path in PAGES:
            with self.subTest(page=path):
                await self.assert_render_without_main_script(path, "light", "dark")

    async def test_first_paint_respects_saved_and_system_themes(self):
        for system_theme in ("light", "dark"):
            for saved_theme in (None, "", "light", "dark", "invalid"):
                with self.subTest(system=system_theme, saved=saved_theme):
                    await self.assert_render_without_main_script(
                        "index.html", system_theme, saved_theme
                    )

    async def test_theme_and_mobile_menu_work_on_every_page(self):
        for path in PAGES:
            with self.subTest(page=path):
                context = await self.browser.new_context(
                    color_scheme="light", viewport={"width": 390, "height": 844}
                )
                try:
                    page = await context.new_page()
                    errors = []
                    page.on("pageerror", lambda error: errors.append(str(error)))
                    response = await page.goto(f"{self.base_url}/{path}")
                    self.assertEqual(response.status, 200)
                    toggle = page.locator(".theme-toggle-btn")
                    await expect(toggle).to_have_attribute(
                        "aria-label", "Toggle theme (current: light)"
                    )
                    await toggle.click()
                    await expect(page.locator("html")).to_have_attribute(
                        "data-theme", "dark"
                    )
                    self.assertEqual(
                        await page.evaluate("localStorage.getItem('cloudymind-theme')"),
                        "dark",
                    )
                    await page.reload()
                    await expect(toggle).to_have_attribute(
                        "aria-label", "Toggle theme (current: dark)"
                    )
                    await toggle.click()
                    await expect(page.locator("html")).to_have_attribute(
                        "data-theme", "light"
                    )
                    menu = page.locator(".mobile-menu-toggle")
                    if await menu.count():
                        await expect(page.locator(".nav-links")).to_be_hidden()
                        await menu.click()
                        await expect(menu).to_have_attribute("aria-expanded", "true")
                        await expect(page.locator(".nav-links")).to_be_visible()
                        await menu.click()
                        await expect(menu).to_have_attribute("aria-expanded", "false")
                        await expect(page.locator(".nav-links")).to_be_hidden()
                    self.assertEqual(errors, [])
                finally:
                    await context.close()

    async def test_system_theme_changes_until_user_overrides_it(self):
        page = await self.browser.new_page(color_scheme="light")
        await page.goto(f"{self.base_url}/index.html")
        await page.emulate_media(color_scheme="dark")
        await expect(page.locator("html")).to_have_attribute("data-theme", "dark")
        await page.locator(".theme-toggle-btn").click()
        await expect(page.locator("html")).to_have_attribute("data-theme", "light")
        await page.emulate_media(color_scheme="light")
        await page.emulate_media(color_scheme="dark")
        await expect(page.locator("html")).to_have_attribute("data-theme", "light")

    async def test_content_remains_available_without_javascript(self):
        for system_theme in ("light", "dark"):
            page = await self.browser.new_page(
                java_script_enabled=False, color_scheme=system_theme
            )
            await page.goto(f"{self.base_url}/index.html")
            await expect(page.locator("main")).to_be_visible()
            await expect(page.locator("html")).to_have_css(
                "background-color", BACKGROUNDS[system_theme]
            )
            await page.close()


if __name__ == "__main__":
    unittest.main()
