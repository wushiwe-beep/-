import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# 指定 ChromeDriver 的路径
service = Service("/usr/local/bin/chromedriver")

# 配置无头模式
chrome_options = Options()
chrome_options.add_argument("--headless")  # 无头模式
chrome_options.add_argument("--disable-gpu")  # 禁用 GPU（可选）
chrome_options.add_argument("--no-sandbox")  # 在某些环境下需要
chrome_options.add_argument("--disable-dev-shm-usage")  # 防止资源不足

# 初始化 WebDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

# 目标 URL
url = "https://www.wjx.cn/vm/mBq4AbT.aspx"

# 题目权重设置：例如某些题目选择某个选项的概率更高
question_weights = {
    0: [0.3, 0.7],  # 第一题
    1: [0.1, 0.4, 0.3, 0.1, 0.1],  # 第二题
    2: [0.5, 0.1, 0.1, 0.1, 0.1, 0.1],  # 第三题
    3: [0.6, 0.2, 0.1, 0.1],  # 第四题
    4: [0.2, 0.6, 0.1, 0.1],  # 第五题
    5: [0.5, 0.3, 0.1, 0.1],  # 第六题
    6: [0.1, 0.4, 0.5],  # 第七题
    7: [0.4, 0.3, 0.1, 0.1, 0.1],  # 第八题
    8: [0.6, 0.1, 0.1, 0.1, 0.1],  # 第九题
    9: [0.2, 0.2, 0.3, 0.1, 0.1, 0.1],  # 第十题
    10: [0.3, 0.2, 0.3, 0.2],  # 第十一题
    11: [0.5, 0.1, 0.1, 0.1, 0.1, 0.1],  # 第十二题
    12: [0.3, 0.2, 0.2, 0.1, 0.1, 0.1],  # 第十三题
    13: [0.1, 0.1, 0.3, 0.1, 0.1, 0.3],  # 第十四题
    14: [0.1, 0.1, 0.3, 0.2, 0.3],  # 第十五题
    15: [0.1, 0.2, 0.1, 0.3, 0.2, 0.1],  # 第十六题
    16: [0.3, 0.3, 0.4],  # 第十七题
    17: [0.3, 0.3, 0.1, 0.2, 0.1],  # 第十八题
    18: [0.2, 0.1, 0.1, 0.2, 0.2, 0.1, 0.1],  # 第十九题
    19: [0.4, 0.1, 0.3, 0.1, 0.1],  # 第二十题
}


def fill_questionnaire():
    try:
        driver.get(url)  # 加载问卷页面
        time.sleep(3)  # 等待页面加载完成

        # 获取所有题目
        question_elements = driver.find_elements(By.CLASS_NAME, "ui-controlgroup")
        print(f"共找到 {len(question_elements)} 道题目。")

        # 遍历所有题目
        for idx, question in enumerate(question_elements):
            print(f"正在处理第 {idx + 1} 道题目...")

            # 获取该题目是否为单选（ui-radio）或多选（ui-checkbox）
            radio_options = question.find_elements(By.CLASS_NAME, "ui-radio")  # 单选题
            checkbox_options = question.find_elements(By.CLASS_NAME, "ui-checkbox")  # 多选题

            # 如果是单选题
            if radio_options:
                if idx in question_weights:  # 如果题目有设置权重
                    weights = question_weights[idx]
                    chosen_radio = random.choices(radio_options, weights=weights)[0]  # 按权重选择
                    chosen_radio.click()
                else:
                    random.choice(radio_options).click()
                print(f"第 {idx + 1} 道题目是单选题，已随机选择一个选项。")

            elif checkbox_options:
                num_choices = random.randint(2, 3)  # 随机选择 2 或 3 个选项
                num_choices = min(num_choices, len(checkbox_options))  # 不超过实际可选项数量
                random_choices = random.sample(checkbox_options, num_choices)  # 随机选择选项

                for choice in random_choices:
                    # 滚动到目标元素
                    driver.execute_script("arguments[0].scrollIntoView(true);", choice)
                    time.sleep(0.5)  # 等待滚动完成
                    choice.click()  # 点击选项

                print(f"第 {idx + 1} 道题目是多选题，已随机选择 {len(random_choices)} 个选项。")

        # 提交按钮
        submit_button = driver.find_element(By.ID, "ctlNext")
        submit_button.click()
        print("问卷已提交！")
        time.sleep(2)  # 等待提交完成
    except Exception as e:
        print(f"填写问卷时发生错误: {e}")


# 填写 200 份问卷
for i in range(200):
    print(f"正在填写第 {i + 1} 份问卷...")
    fill_questionnaire()
    print(f"第 {i + 1} 份问卷填写完成。")

    # 间隔一定时间再填写下一份
    if i < 199:
        wait_time = random.randint(10, 15)  # 随机等待 10 到 15 秒
        print(f"等待 {wait_time} 秒后继续填写...")
        time.sleep(wait_time)

# 关闭 WebDriver
driver.quit()
