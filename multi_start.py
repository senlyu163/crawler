import os
import threading

filtered_file_names = []
for names in os.listdir(
        "/home/sen/Workspace/handle_data/lab_scrapy/spider_crawl_start_55/scrapy_spider/scrapy_spider/spiders"):
    if names[-2:] == "py" and names != "__init__.py":
        filtered_file_names.append(names[:-3][1:])

thread_num = 6

file_num = len(filtered_file_names) // 6


def run(thread_id=0):
    split_file = filtered_file_names[file_num * thread_id: file_num * (thread_id + 1)]
    for file in split_file:
        os.system("scrapy crawl " + file)
    # print(len(split_file))


thread_list = []
for i in range(thread_num):
    thread_list.append(threading.Thread(target=run, args=(i,)))

for thread in thread_list:
    thread.start()

print("All done!")
