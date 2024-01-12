# selenium-supporter

https://pypi.org/project/selenium-supporter
<pre>
pip install selenium-supporter
</pre>

Supported APIs:
<pre>
import selenium_supporter

selenium_supporter.drivers.ChromeDriver()
selenium_supporter.drivers.ChromeDebuggingDriver()

selenium_supporter.utils.get_chrome_web_browser_path()
selenium_supporter.utils.kill_all_chrome_web_browser_processes()
selenium_supporter.utils.kill_all_chrome_web_browser_driver_processes()
selenium_supporter.utils.open_chrome_web_browser(user_data_dir=None, proxy_server=None)
selenium_supporter.utils.open_chrome_web_browser_with_remote_debugging_mode(remote_debugging_port, remote_debugging_address, user_data_dir=None, proxy_server=None, headless=False)
selenium_supporter.utils.check_port_open(ip, port)
selenium_supporter.utils.save_partial_screenshot(element, image_file)
selenium_supporter.utils.save_full_screenshot(driver, image_file)     
selenium_supporter.utils.save_full_screenshot_with_scroll(driver, image_file)
selenium_supporter.utils.save_partial_screenshot_with_scroll(driver, partial_element, image_file)
selenium_supporter.utils.set_value(driver, element, value)
selenium_supporter.utils.set_value_send_keys(driver, element, value)
selenium_supporter.utils.set_attribute(driver, element, attribute, value)
selenium_supporter.utils.remove_element(driver, element)
selenium_supporter.utils.remove_x_scrollbar(driver)
selenium_supporter.utils.click(element)
selenium_supporter.utils.click_send_keys(driver, element)    
selenium_supporter.utils.click_javascript(driver, element)
selenium_supporter.utils.scroll_down_to_bottom(driver)
</pre>

Examples:  
https://github.com/automatethem/selenium-supporter/blob/main/examples/server.py  
https://github.com/automatethem/selenium-supporter/blob/main/examples/client.py
