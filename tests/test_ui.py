from playwright.sync_api import sync_playwright

def test_login_aruba_webmail():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        pagina = browser.new_page()

        pagina.goto("https://webmaildominitest.aruba.it/new/auth/login")
        pagina.wait_for_load_state("networkidle")

        pagina.locator("input[type='text']").fill("postmaster@testperdomini.it")
        pagina.locator("input[type='password']").fill("Test123!")

        try:
            pagina.locator("button:has-text('Accetta tutti')").click(timeout=5000)
            pagina.wait_for_timeout(1000)
        except:
            pass

        pagina.locator("button:has-text('Accedi')").click()

        pagina.wait_for_url("**/management/home", timeout=15000)

        assert "/management/home" in pagina.url
        assert pagina.is_visible("text=Gestione caselle e dominio")

        browser.close()
