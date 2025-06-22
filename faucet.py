from playwright.sync_api import sync_playwright
import time

WALLET_ADDRESS = "0x1fFA0ab35Ff6bBcB7f053683F33eb346860aD469"
URL = "https://cloud.google.com/application/web3/faucet/ethereum/sepolia" 

def run_task():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("Открываю страницу...")
        page.goto(URL)
        page.wait_for_timeout(5000)  # ждём прогрузки JS

        try:
            wallet_input = page.locator('//input[@placeholder="Enter wallet address"]')
            wallet_input.fill(WALLET_ADDRESS)
            print("Адрес кошелька введён")

            page.click('//button[.//span[text()="Request tokens"]]')
            print("Кнопка нажата")

            error_locator = page.locator('//xap-callout-body')
            if error_locator.is_visible(timeout=10000):
                error_text = error_locator.inner_text()
                if "Each Google Account and wallet address gets one drip on Sepolia every 1 day" in error_text:
                    print("Лимит достигнут:", error_text)
                else:
                    print("Другая ошибка:", error_text)
            else:
                print("Запрос успешен!")

        except Exception as e:
            print(f"Ошибка при выполнении: {e}")

        finally:
            browser.close()

if __name__ == "__main__":
    run_task()
