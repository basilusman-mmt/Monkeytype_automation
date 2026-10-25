import time
import pydirectinput
from playwright.sync_api import sync_playwright

pydirectinput.PAUSE = 0

def smooth_move_to(target_x, target_y, steps=500, delay=0):
    start_x, start_y = pydirectinput.position()

    for i in range(1, steps + 1):
        current_x = int(start_x + (target_x - start_x) * (i / steps))
        current_y = int(start_y + (target_y - start_y) * (i / steps))
        pydirectinput.moveTo(current_x, current_y)
        time.sleep(delay)

def click():
    pydirectinput.mouseDown()
    time.sleep(0.05)
    pydirectinput.mouseUp()

def run_monkeytype_bot():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=["--start-maximized"])
        context = browser.new_context(no_viewport=True)
        page = context.new_page()

        page.goto("https://monkeytype.com")

        try:
            smooth_move_to(1614, 815)
            click()
        except Exception:
            pass

        page.wait_for_selector(".word.active", timeout=15000)
        smooth_move_to(334, 607)
        click()
        time.sleep(0.5)

        start_time = time.time()
        last_word = ""

        while time.time() - start_time < 205:
            if not page.locator("#words").is_visible():
                break

            active_word_text = page.evaluate("""() => {
                const activeWord = document.querySelector('#words .word.active');
                if (!activeWord) return null;
                const letters = activeWord.querySelectorAll('letter');
                return Array.from(letters).map(l => l.innerText).join('');
            }""")

            if active_word_text and active_word_text != last_word:
                pydirectinput.write(active_word_text + " ", interval=0.0000002)
                last_word = active_word_text
                time.sleep(0.000002)
            else:
                time.sleep(0.000001)
        time.sleep(50)
        browser.close()

if __name__ == "__main__":
    run_monkeytype_bot()
