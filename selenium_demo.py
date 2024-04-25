import time
from urllib import parse
from selenium import webdriver
from selenium.common import NoSuchElementException

url = 'https://www.google.com/maps'
if __name__ == '__main__':
    hotels=[]
    driver = webdriver.Chrome()
    driver.get(url)
    current_handle=driver.current_window_handle
    # 模拟搜索
    search_element = driver.find_element("xpath","//input[contains(@class,'searchboxinput')]")  # 用xpath定位到搜索的输入框
    search_element.clear()  # 清除输入框原本的数据
    search_element.send_keys("美国旧金山酒店")
    searchBtn = driver.find_element("xpath", "//button[@id='searchbox-searchbutton']")
    searchBtn.click()
    time.sleep(6)

    #模拟滚动
    # 定位到需要滚动的元素
    scroll_element = driver.find_element("xpath","//div[@class='aIFcqe']//div[contains(@class,'m6QErb WNBkOb')]/div[contains(@class,'m6QErb DxyBCb kA9KIf dS8AEf ecceSd')]/div[contains(@class,'m6QErb DxyBCb kA9KIf dS8AEf ecceSd')]")
    # 定义滚动次数
    scroll_count = 50
    for _ in range(scroll_count):
        # 使用JavaScript滚动到指定元素的底部
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll_element)
        time.sleep(4)
        try:
            #检测是否翻滚到了底部
            last_element = driver.find_element("xpath",
                                               "//div[@class='aIFcqe']//div[contains(@class,'m6QErb tLjsW eKbjU')]//p[contains(@class,'fontBodyMedium')]//span[@class='HlvSq']")
            break
        except NoSuchElementException:
            pass

    nodes=[]
    try:
        #获取所有酒店节点
        nodes = driver.find_elements("xpath", "//div[@class='aIFcqe']//div[contains(@class,'Nv2PK')]")
        hotel={}
        for node in nodes:
            try:
                #酒店名称
                name_element=node.find_element("xpath",".//a[@class='hfpxzc']")
                name=name_element.get_attribute("aria-label")
                link_url=name_element.get_attribute("href")
                hotel['name'] = name
                try:
                    #酒店图片
                    image_element = node.find_element("xpath", ".//div[@class='SpFAAb']//div[contains(@class,'p0Hhde FQ2IWe')]/img")
                    hotel['imageUrl']=image_element.get_attribute("src")
                except NoSuchElementException:
                    pass
                #酒店价格
                price_element = node.find_element("xpath",
                                                 ".//div[@class='SpFAAb']//div[contains(@class,'wcldff fontHeadlineSmall Cbys4b')]")
                hotel['price'] = price_element.text

                #酒店星级
                starname_element = node.find_element("xpath", ".//div[@class='W4Efsd']/div[@class='W4Efsd']")
                star_name=starname_element.text
                hotel['starName']=star_name

                star_element = node.find_element("xpath", ".//div[@class='W4Efsd']/div[@class='AJB7ye']//span[@class='MW4etd']")
                star = star_element.text
                hotel['star'] = star
                comment_element = node.find_element("xpath", ".//div[@class='W4Efsd']/div[@class='AJB7ye']//span[@class='UY7F9']")
                comment = comment_element.text
                comment=comment.replace("(","")
                comment = comment.replace(")", "")
                hotel['comment'] = comment

                #酒店设施
                device_elements = node.find_elements("xpath", ".//div[@class='ktbgEf']/div[@class='Yfjtfe']")
                devices=[]
                for device_element in device_elements:
                    devices.append(device_element.get_attribute("aria-label"))
                hotel['device']=",".join(devices)

                try:
                    #坐标
                    quota_url=parse.unquote(link_url)
                    quota_url = quota_url[quota_url.find("!3d") + 3:]
                    x = quota_url[0:quota_url.find("!4d")]
                    quota_url = quota_url[quota_url.find("!4d") + 3:]
                    y = quota_url[0:quota_url.find("!")]
                    hotel['location']=x+","+y
                except NoSuchElementException:
                    pass


                # 酒店详情，在新的标签页打开链接
                driver.execute_script(f'window.open("{link_url}", "_blank");')
                time.sleep(6)
                driver.switch_to.window(driver.window_handles[-1])
                try:
                    english_element=driver.find_element("xpath",
                                     "//div[contains(@class,'aIFcqe')]//div[contains(@class,'m6QErb WNBkOb')]/div[contains(@class,'TIHn2')]//h2[@class='bwoZTb']/span")
                    hotel['englishName'] = english_element.text
                except NoSuchElementException:
                    pass

                try:
                    # 地址
                    location_element = info_elements = driver.find_element("xpath",
                                                           "//div[contains(@class,'m6QErb')]/div[contains(@class,'RcCsl fVHpi w4vB1d NOE9ve M0S7ae AG25L')]/button[@data-item-id='address']")
                    address = location_element.get_attribute("aria-label")
                    hotel['address'] = address
                except NoSuchElementException:
                   pass
                try:
                    # 地址
                    location_element = info_elements = driver.find_element("xpath",
                                                                            "//div[contains(@class,'m6QErb')]/div[contains(@class,'RcCsl fVHpi w4vB1d NOE9ve M0S7ae AG25L')]/button[@data-item-id='locatedin']")
                    address = location_element.get_attribute("aria-label")
                    hotel['address'] = hotel['address']+" "+address if 'address' in hotel else address
                except Exception as e:
                    pass

                try:
                    # 网站
                    web_element = info_elements = driver.find_element("xpath",
                                                                            "//div[contains(@class,'m6QErb')]/div[contains(@class,'RcCsl fVHpi w4vB1d NOE9ve M0S7ae AG25L')]/a[@data-item-id='authority']")
                    web_url = web_element.get_attribute("href")
                    hotel['weburl'] = web_url
                except NoSuchElementException:
                    pass

                try:
                    # 电话
                    phone_element = info_elements = driver.find_element("xpath",
                                                                       "//div[contains(@class,'m6QErb')]/div[contains(@class,'RcCsl fVHpi w4vB1d NOE9ve M0S7ae AG25L')]/button[contains(@data-item-id,'phone:')]")
                    phone = phone_element.get_attribute("aria-label")
                    hotel['phone'] = phone
                except NoSuchElementException:
                    pass


                try:
                    #plus code
                    pluscode_element = info_elements = driver.find_element("xpath",
                                                                         "//div[contains(@class,'m6QErb')]/div[contains(@class,'RcCsl fVHpi w4vB1d NOE9ve M0S7ae AG25L')]/button[@data-item-id='oloc']")
                    pluscode = pluscode_element.get_attribute("aria-label")
                    hotel['pluscode'] = pluscode
                except NoSuchElementException:
                    pass


                driver.close()
                driver.switch_to.window(current_handle)
                hotels.append(hotel)
                print(hotel)
                print("-------------------")
            except Exception as e1:
                print(e1)
    except Exception as e:
        print(e)

    print(len(hotels))
    print(hotels)
