from playwright.sync_api import sync_playwright

def test_login_aruba_webmail():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        pagina = browser.new_page()

        # 1. Vai alla pagina di login
        pagina.goto("https://webmaildominitest.aruba.it/new/auth/login")
        pagina.wait_for_load_state("networkidle")

        # 2. Compila i campi PRIMA di chiudere il banner
        pagina.locator("input[type='text']").fill("postmaster@testperdomini.it")
        pagina.locator("input[type='password']").fill("Test123!")

        # 3. Chiudi il banner cookie cliccando "Accetta tutti"
        try:
            pagina.locator("button:has-text('Accetta tutti')").click(timeout=5000)
            pagina.wait_for_timeout(1000)  # aspetta che il banner sparisca
        except:
            pass

        # 4. Ora clicca "Accedi" con il banner sparito
        pagina.locator("button:has-text('Accedi')").click()

        # 5. Aspetta il redirect
        pagina.wait_for_url("**/management/home", timeout=15000)

        # 6. Verifica URL e contenuto pagina
        assert "/management/home" in pagina.url
        assert pagina.is_visible("text=Gestione caselle e dominio")

        browser.close()