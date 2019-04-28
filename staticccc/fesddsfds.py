from selenium import webdriver
import re
import threading
from queue import Queue
import csv

maxThreads = 3


# 1.爬取前n页中每个职位的url保存到列表中（n自定义）
# 2.爬取每个url链接，并将数据保存到xls或csv文件中

class laGou(object):

    def __init__(self,search_name,page=0):
        '''
        系统需要的一些儿数据
        '''
        self.search_url = 'https://www.lagou.com/jobs/list_%s'%search_name
        self.page = page
        self.queue = None
        self.writer = None
        self.jobs_list = [['company','job_name','salary','location','jingyan','xueli','job_type','job_advantage','job_detail']]

    def paser_url(self):
        '''
        爬取职位url
        :return:返回职位url列表
        '''
        driver = webdriver.Chrome()
        try:
            driver.get(self.search_url)
            print(driver.current_url)
            print(dir(driver))
            print(driver.page_source)
            a = driver.find_elements_by_xpath('//a[@class="position_link"]')
            jobs_list = [i.get_attribute('href') for i in a]
            driver.save_screenshot('test.png')
        except Exception as e:
            print('false')
            print(e)
        finally:
            driver.close()

        return jobs_list

    def paser_save1(self,job_url):
        '''
        爬取每一个职位并保存到csv文件中
        :return:
        '''
        driver = webdriver.Chrome()
        try:
            driver.get(job_url)
            print(driver.current_url)
            print(dir(driver))
            print(driver.page_source)
            a = driver.find_elements_by_xpath('//*[@class="job-detail"]/p|//*[@class="job-detail"]/p/strong')
            print([i.text for i in a])
            b = driver.find_element_by_xpath("//*[@class='job_request']//span[5]")
            print(b.text)
            driver.save_screenshot('test.png')
        except Exception as e:
            print('false')
            print(e)
        finally:
            driver.close()

        pass

    def save_csv(self,job_list):
        '''
        save
        :param job_con:
        :return:
        '''
        with open('jobs.csv', 'w', encoding='utf-8') as f:
            writer = csv.writer(f)
            for job_con in job_list:
                writer.writerow(job_con)
        pass

    def paser_save(self,job_url):
        '''
        爬取每一个职位并保存到csv文件中
        :return:
        '''
        driver = webdriver.Chrome()
        try:
            driver.get(job_url)
            print(driver.current_url)
            print(dir(driver))
            print(driver.page_source)
            company = driver.find_element_by_xpath("//*[@class='company']").text
            job_name = driver.find_element_by_xpath("//*[@class='job-name']").get_attribute('title')
            salary = driver.find_element_by_xpath("//*[@class='job_request']//span[1]").text
            location = driver.find_element_by_xpath("//*[@class='job_request']//span[2]").text
            location = re.sub('/| ','',location)
            jingyan = driver.find_element_by_xpath("//*[@class='job_request']//span[3]").text
            jingyan = re.sub('/| ','',jingyan)
            xueli = driver.find_element_by_xpath("//*[@class='job_request']//span[4]").text
            xueli = re.sub('/| ','',xueli)
            job_type = driver.find_element_by_xpath("//*[@class='job_request']//span[5]").text
            job_advantage = driver.find_element_by_xpath('//*[@class="job-advantage"]/p').text
            job_detail = driver.find_element_by_xpath('//*[@class="job-detail"]').text
            job_detail =re.sub("\n| ","",job_detail)
            text_list = [company,job_name,salary,location,jingyan,xueli,job_type,job_advantage,job_detail]
            print(text_list)
            self.jobs_list.append(text_list)
            # self.save_csv(text_list)
            driver.save_screenshot('test.png')
        except Exception as e:
            print('false')
            print(e)
        finally:
            self.queue.get()
            driver.close()


    def run(self):
        '''
        主程序
        :return:
        '''
        title = ['company','job_name','salary','location','jingyan','xueli','job_type','job_advantage','job_detail']
        # self.save_csv(title)
        self.queue = Queue(maxThreads)
        threads = []
        job_list = self.paser_url()
        # for job_url in job_list:
        #     self.queue = put(job_url)
        #     target = threading.Thread(target=self.paser_save,args = [job_url,self.queue])
        #     target.start()
        #     # parser_save(job_url)
        for i in range(10):
            self.queue.put(job_list[i])
            target = threading.Thread(target=self.paser_save,args = [job_list[i]])
            target.start()
            threads.append(target)
            # parser_save(job_url)
        for i in threads:
            i.join()
            # print([i for i in q])
        print(self.jobs_list)
        self.save_csv(self.jobs_list)
        for i in self.jobs_list:
            print(i)
        # for i in threads:
        #     i.join()

# def paser_save(job_url):
#     '''
#     爬取每一个职位并保存到csv文件中
#     :return:
#     '''
#     driver = webdriver.Chrome()
#     try:
#         driver.get(job_url)
#         print(driver.current_url)
#         print(dir(driver))
#         print(driver.page_source)
#         a = driver.find_elements_by_xpath('//*[@class="job-detail"]/p|//*[@class="job-detail"]/p/strong')
#         company = driver.find_element_by_xpath("//*[@class='company']").text
#         job_name = driver.find_element_by_xpath("//*[@class='job-name']").get_attribute('title')
#         salary = driver.find_element_by_xpath("//*[@class='job_request']//span[1]").text
#         location = driver.find_element_by_xpath("//*[@class='job_request']//span[2]").text
#         location = re.sub('/| ','',location)
#         print(location)
#         jingyan = driver.find_element_by_xpath("//*[@class='job_request']//span[3]").text
#         jingyan = re.sub('/| ','',jingyan)
#         xueli = driver.find_element_by_xpath("//*[@class='job_request']//span[4]").text
#         xueli = re.sub('/| ','',xueli)
#         job_type = driver.find_element_by_xpath("//*[@class='job_request']//span[5]").text
#         job_advantage = driver.find_element_by_xpath('//*[@class="job-advantage"]/p').text
#         job_detail = driver.find_element_by_xpath('//*[@class="job-detail"]').text
#         job_detail =re.sub("\n| ","",job_detail)
#         print(job_detail)
#         text_list = [company,job_name,salary,location,jingyan,xueli,job_type,job_advantage,job_detail]
#         # print(len(a))
#         # print([(i.text,i.get_attribute('value')) for i in a])
#         # print("".join([i.text for i in a]))
#         print(text_list)
#         driver.save_screenshot('test.png')
#     except Exception as e:
#         print('false')
#         print(e)
#     finally:
#         driver.close()

if __name__ == '__main__':
    paser = laGou('java')
    paser.run()