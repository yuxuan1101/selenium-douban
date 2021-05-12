import random

from matplotlib.pyplot import show
import libs.slide_img_libs as slide_libs
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException

# url consts
home_url = "https://www.douban.com"

# selector consts
test_elem_selector = (By.ID, 'anony-reg-new')
account_iframe_selector = (By.XPATH, '//*[@id="anony-reg-new"]/div/div[1]/iframe')
account_tab_selector = (By.XPATH, '/html/body/div[1]/div[1]/ul[1]/li[2]')
username_input_selector = (By.XPATH, '//*[@id="username"]')
password_input_selector = (By.XPATH, '//*[@id="password"]')
login_button_selector = (By.XPATH, '/html/body/div[1]/div[2]/div[1]/div[5]/a')

# phone_input_selector = (By.XPATH, '/html/body/div[1]/div[2]/div[1]/div[3]/div/input')
# code_button_selector = (By.XPATH, '/html/body/div[1]/div[2]/div[1]/div[5]/div/div/a')
tcaptcha_iframe_selector = (By.ID, 'tcaptcha_iframe')
slide_img_selector = (By.ID, 'slideBlock')
target_img_selector = (By.ID, 'slideBg')

# other consts
FIREFOX_DRIVER_PATH = '/Users/user/workspace/selenium-drivers/geckodriver'
USERNAME = '*****'
PASSWORD = '*****'
OPTS_HEADLESS = True

def wait_for(timeout = 10, round_time = 3):
    def decorator(func):
        def wrapper(*args, **kw):
            start = time.perf_counter()
            while 1:
                try:
                    return func(*args, **kw)
                except Exception as err:
                    end = time.perf_counter()
                    if end - start > timeout:
                        pass
                    time.sleep(round_time)
        return wrapper
    return decorator

@wait_for()
def wait_for_elem(selector):
    return browser.find_element(selector[0], selector[1])

@wait_for()
def wait_for_attribute(elem, attr, allow_none = False):
    attrVal = elem.get_attribute(attr)
    if not allow_none and attrVal is None:
        raise Exception('val can\'t be None.')
    return attrVal

def switch_frame(frameSelector):
    elem = wait_for_elem(frameSelector)
    browser.switch_to.frame(elem)

def get_slide_distance(slide, target):
    # slide_img = slide_libs.url2image(slide.get_attribute("src"))
    # target_img = slide_libs.url2image(target.get_attribute("src"))
    slide_img = slide_libs.url2image(wait_for_attribute(slide, "src"))
    target_img = slide_libs.url2image(wait_for_attribute(target, "src"))
    
    position = slide_libs.check_position(slide_img, target_img)

    t_size = target.size
    t_loc = target.location
    s_loc = slide.location
    # slide_libs.show(slide_img, target_img, position)
    
    return t_loc['x'] +t_size['width'] * position['x'] - s_loc['x']

# 将一个滑动距离 拆为 多个逐渐减小的 滑动距离
def fuck_distance(rest_dis, dis_list = None):
    if dis_list is None:
        dis_list = []
    
    this_dis = rest_dis / 2 + random.uniform(0, 30.0)
    dis_list.append(this_dis)
    rest_dis = rest_dis - this_dis

    if rest_dis > 0:
        return fuck_distance(rest_dis, dis_list=dis_list)
    if rest_dis < 0:
        dis_list[-1] = dis_list[-1] + rest_dis + random.uniform(-1.0, 1.0)
    return dis_list



options = Options()
options.headless = OPTS_HEADLESS
browser = webdriver.Firefox(executable_path = FIREFOX_DRIVER_PATH, options = options)
browser.set_page_load_timeout(5.0)

print("opening home page.")
start = time.perf_counter()
try:
    browser.get(home_url)
except TimeoutException as err:
    print('timeout')


switch_frame(account_iframe_selector)
wait_for_elem(account_tab_selector).click()

wait_for_elem(username_input_selector).send_keys(USERNAME)
wait_for_elem(password_input_selector).send_keys(PASSWORD)
wait_for_elem(login_button_selector).click()
switch_frame(tcaptcha_iframe_selector)
slide_elem = wait_for_elem(slide_img_selector)
target_elem = wait_for_elem(target_img_selector)

dis = get_slide_distance(slide_elem, target_elem)

action = ActionChains(browser)
action.click_and_hold(slide_elem).perform()

action.move_by_offset(dis, 0).perform()

# print(dis)
# dis_list = fuck_distance(dis)
# print(dis_list)
# move_dis = 0
# for dis_item in dis_list:
#     move_dis += dis_item
#     print('move: ' + str(move_dis))
#     action.move_to_element_with_offset(slide_elem, move_dis, random.uniform(0, 1)).perform()
#     print('rest dis: ' + str(get_slide_distance(slide_elem, target_elem)))
#     time.sleep(random.uniform(0.5, 1))

action.reset_actions()
time.sleep(3)

print('success')
time.sleep(3)

# browser.quit()
