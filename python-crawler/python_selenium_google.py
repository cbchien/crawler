from selenium import webdriver
import time 
import pandas as pd
import sys
import datetime

data = []

driver = webdriver.Chrome()
driver.get("https://some_domain/")

try:
    # Login to some_domain via Google
    if "Forwarding" in driver.title:
        elem = driver.find_element_by_id("identifierId").send_keys(sys.argv[1])
        driver.find_element_by_id("identifierNext").click()
        time.sleep(1.5)
        driver.find_element_by_name("password").send_keys(sys.argv[2])
        driver.find_element_by_id("passwordNext").click()
        time.sleep(2)
        # Check if login success
        if driver.find_elements_by_xpath("//*[contains(text(), 'Wrong password')]"):
            print("The email/password you've enter is incorrect")
            print("Closing app...")
            print("Please restart")
            driver.close()
            sys.exit()
        # Check if login authorization
        if driver.find_elements_by_xpath("//*[contains(text(), 'Login denied')]"):
            print("Your account is not authorized to view this webpage")
            print("Closing app...")
            print("Please restart")
            driver.close()
            sys.exit()
    # Exit program due to change in login/website process
    else:
        print("url process flow is incorrect")
        driver.close()
    
    # Get a list of user id from xlsx
    xl = pd.read_excel("C:\\path\\to\\excel\\list.xlsx")
    total_count = len(xl.index)
    for index in range(0, total_count):
        user_id = xl.values[index][4]
        print("\n", "Start parsing user id:", user_id, "===", index, "of", total_count, "===")
        url_receipt = "https://some_domain/user/receipt_setting/{}/".format(user_id)
        print("moving to receipt->", url_receipt)
        driver.get(url_receipt)
        (driver.page_source).encode('utf-8')
        driver.forward()
        # Add time delay for no purpose but to slow the process down
        time.sleep(0.5)
        entry = {}
        entry.update({
                "id": user_id,
                "email": driver.find_element_by_xpath(".//div[@id='personal']/table/tbody/tr/td[1]").text,
                "Address": driver.find_element_by_xpath(".//div[@id='personal']/table/tbody/tr/td[2]").text,
                "City": driver.find_element_by_xpath(".//div[@id='personal']/table/tbody/tr/td[3]").text,
                "Country": driver.find_element_by_xpath(".//div[@id='personal']/table/tbody/tr/td[4]").text,
                "District": driver.find_element_by_xpath(".//div[@id='personal']/table/tbody/tr/td[5]").text,
                "Name": driver.find_element_by_xpath(".//div[@id='personal']/table/tbody/tr/td[6]").text,
                "Phone": driver.find_element_by_xpath(".//div[@id='personal']/table/tbody/tr/td[7]").text,
                "State": driver.find_element_by_xpath(".//div[@id='personal']/table/tbody/tr/td[8]").text,
                "Town": driver.find_element_by_xpath(".//div[@id='personal']/table/tbody/tr/td[9]").text,
                "Zipcode": driver.find_element_by_xpath(".//div[@id='personal']/table/tbody/tr/td[10]").text,
                "兌換期限": xl.values[index][0],
                "中獎期別": xl.values[index][1],
                "發票號碼": xl.values[index][2],
                "訂單編號": xl.values[index][3]
                })
        
        # Parse user account information for status and contact
        time.sleep(0.5)
        url_account_info = "https://some_domain/user/account_info/{}/".format(user_id)
        print("moving to account info->", url_account_info)
        driver.get(url_account_info)
        (driver.page_source).encode('utf-8')
        driver.forward()
        try:
            corss_border = driver.find_element_by_xpath(".//div[@data-tab='general-info']/div/div[15]/span/button").text
        except:
            corss_border = "No"
        entry.update({
                "status" : driver.find_element_by_xpath(".//button[contains(@class, 'status')]").text,
                "account_cell_number": driver.find_element_by_xpath(".//div[@data-tab='general-info']/div/div[6]/input").get_attribute("value"),
                "corss_border": corss_border
                })      

        data.append(entry)
        print("Finish parsing", user_id)
    
    # Save to file
    print("\n", "Start file saving process")
    date = datetime.datetime.now().date()
    hh = datetime.datetime.now().time().strftime("%H")
    mm = datetime.datetime.now().time().strftime("%M")
    file_name = "receipt" + str(date) + "-" + str(hh) + "-" + str(mm) + ".xlsx"
    df = pd.DataFrame(data)
    print("Saving", file_name, "....")
    df.to_excel(file_name, sheet_name= 'summary', index=False, encoding='utf-8')
    print("Filing saving process complete!")
    time.sleep(1)
    print("\n", "Closing app...")
    time.sleep(2)
    driver.close()
    sys.exit()

except Exception as e: 
    print("Encounter error. Please contact someone for help")
    print(e)
    print("Closing app...")
    driver.close()
    sys.exit()

