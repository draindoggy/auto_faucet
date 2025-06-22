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

        try:
            wallet_input = page.locator("input[placeholder='Enter wallet address']")
            wallet_input.wait_for_selector_state("visible", timeout=60000)
            wallet_input.fill(WALLET_ADDRESS)
            print("Адрес кошелька введён")

            page.click("button:has-text('Request tokens')", timeout=30000)
            print("Кнопка нажата")

            try:
                error_text = page.text_content("//xap-callout-body", timeout=10000)
                if "gets one drip on Sepolia every 1 day" in error_text:
                    print("Лимит достигнут:", error_text)
                else:
                    print("Другое сообщение:", error_text)
            except:
                print("Сообщение об ошибке не найдено.")

        except Exception as e:
            print(f"Ошибка при выполнении: {e}")
            # Для диагностики: сохрани HTML и сделай скриншот
            page.screenshot(path="error_screenshot.png")
            with open("page_source.html", "w") as f:
                f.write(page.content())

        finally:
            browser.close()

if __name__ == "__main__":
    run_task()
