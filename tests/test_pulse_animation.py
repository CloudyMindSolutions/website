import functools
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import os
from pathlib import Path
from threading import Thread
import unittest

from playwright.async_api import async_playwright, expect


ROOT = Path(__file__).resolve().parents[1]
PAGES = ("index.html", "fi/index.html")
DOT_COLORS = {"light": "rgb(16, 185, 129)", "dark": "rgb(52, 211, 153)"}


class SiteHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass


class PulseAnimationTests(unittest.IsolatedAsyncioTestCase):
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

    async def assert_dot(self, page, theme):
        dot = page.locator(".pulse-dot")
        await expect(dot).to_be_visible()
        await expect(dot).to_have_css("width", "8px")
        await expect(dot).to_have_css("height", "8px")
        self.assertEqual(
            await dot.evaluate(
                "dot => getComputedStyle(dot, '::after').backgroundColor"
            ),
            DOT_COLORS[theme],
        )
        await expect(page.locator(".hero-badge-wrap")).to_be_visible()

    async def test_pulse_animates_only_transform_and_opacity(self):
        for path in PAGES:
            for theme in ("light", "dark"):
                for width in (390, 1280):
                    with self.subTest(page=path, theme=theme, width=width):
                        context = await self.browser.new_context(
                            color_scheme=theme,
                            reduced_motion="no-preference",
                            viewport={"width": width, "height": 900},
                        )
                        try:
                            page = await context.new_page()
                            response = await page.goto(f"{self.base_url}/{path}")
                            self.assertEqual(response.status, 200)
                            dot = page.locator(".pulse-dot")
                            animations = await dot.evaluate("""dot =>
                                dot.getAnimations({subtree: true}).map(animation => ({
                                    duration: animation.effect.getTiming().duration,
                                    infinite: animation.effect.getTiming().iterations === Infinity,
                                    frames: animation.effect.getKeyframes()
                                }))
                            """)
                            self.assertEqual(len(animations), 1)
                            animation = animations[0]
                            self.assertEqual(animation["duration"], 2000)
                            self.assertTrue(animation["infinite"])
                            for frame in animation["frames"]:
                                properties = set(frame) - {
                                    "offset", "computedOffset", "easing", "composite"
                                }
                                self.assertEqual(properties, {"transform", "opacity"})
                            self.assertEqual(
                                [frame["offset"] for frame in animation["frames"]],
                                [0, 0.7, 1],
                            )
                            self.assertEqual(
                                [frame["transform"] for frame in animation["frames"]],
                                ["scale(1)", "scale(3)", "scale(1)"],
                            )
                            self.assertEqual(
                                [float(frame["opacity"]) for frame in animation["frames"]],
                                [1, 0, 0],
                            )
                            await self.assert_dot(page, theme)
                            await dot.evaluate("""dot => {
                                const animation = dot.getAnimations({subtree: true})[0];
                                animation.pause();
                                animation.currentTime = 700;
                            }""")
                            await self.assert_dot(page, theme)
                        finally:
                            await context.close()

    async def test_reduced_motion_keeps_static_dot_and_updates_live(self):
        for path in PAGES:
            for theme in ("light", "dark"):
                with self.subTest(page=path, theme=theme):
                    context = await self.browser.new_context(
                        color_scheme=theme, reduced_motion="reduce"
                    )
                    try:
                        page = await context.new_page()
                        await page.goto(f"{self.base_url}/{path}")
                        await self.assert_dot(page, theme)
                        dot = page.locator(".pulse-dot")
                        self.assertEqual(
                            await dot.evaluate(
                                "dot => dot.getAnimations({subtree: true}).length"
                            ),
                            0,
                        )
                        self.assertEqual(
                            await dot.evaluate(
                                "dot => getComputedStyle(dot, '::before').opacity"
                            ),
                            "0",
                        )
                        await page.emulate_media(reduced_motion="no-preference")
                        await page.wait_for_function(
                            "document.querySelector('.pulse-dot')"
                            ".getAnimations({subtree: true}).length === 1"
                        )
                        await page.emulate_media(reduced_motion="reduce")
                        await page.wait_for_function(
                            "document.querySelector('.pulse-dot')"
                            ".getAnimations({subtree: true}).length === 0"
                        )
                        await self.assert_dot(page, theme)
                    finally:
                        await context.close()

    async def test_static_badge_without_javascript(self):
        for path in PAGES:
            for theme in ("light", "dark"):
                with self.subTest(page=path, theme=theme):
                    context = await self.browser.new_context(
                        java_script_enabled=False,
                        color_scheme=theme,
                        reduced_motion="reduce",
                    )
                    try:
                        page = await context.new_page()
                        await page.goto(f"{self.base_url}/{path}")
                        await self.assert_dot(page, theme)
                    finally:
                        await context.close()


if __name__ == "__main__":
    unittest.main()
