import requests
import json
import re
import time
from concurrent.futures import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup
import argparse
import os
# Function to perform the POST request
def perform_request(mz):
    url = "https://m.xingming.com/dafen/"
    headers = {
        "authority": "m.xingming.com",
        "method": "POST",
        "path": "/dafen/",
        "scheme": "https",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
        "cache-control": "max-age=0",
        "content-length": "46",
        "content-type": "application/x-www-form-urlencoded",
        "origin": "https://m.xingming.com",
        "priority": "u=0, i",
        "referer": "https://m.xingming.com/dafen/",
        "sec-ch-ua": '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": '"Android"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36"
    }

    data = {
        "xs": "王",
        "mz": mz,
        "action": "test"
    }

    response = requests.post(url, headers=headers, data=data)

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    # Extract the score from the read-content div
    score_element = soup.find(string=re.compile("姓名评分为："))
    score = 0
    if score_element:
        # Navigate to the parent element and find the <font> tag
        parent = score_element.find_parent()
        if parent:
            font_tag = parent.find('font')
            if font_tag and font_tag.string:
                score = float(font_tag.string)  # Convert the score to an integer
    if score < 99:
        print(f"名字 {mz} " + f"得分: {score}" + " 不入选")
        return
    print(f"名字 {mz} " + f"得分: {score}" + " 入选，继续考察天地人三才配置。。。")

    # Find the div with class "read-content"
    read_content_div = soup.find('div', class_='read-content')
    # Initialize a dictionary to hold the extracted information
    extracted_info = {}
    # Check if the div is found
    if read_content_div:
        # Iterate through all paragraphs and tables in the div
        for element in read_content_div.find_all(['p', 'table']):
            if element.name == 'p':
                # For paragraphs, extract text and check for colons
                text = element.get_text(strip=True)
                if '：' in text:
                    parts = text.split('：', 1)
                elif ':' in text:
                    parts = text.split(':', 1)
                else:
                    parts = [text]  # If neither delimiter is found, treat the whole text as a single part

                # Ensure we have at least one part
                if len(parts) > 1:
                    key, value = parts
                    key = key.strip()
                    value = value.strip()
                    # Append value to the list for the key, or create a new list if the key doesn't exist
                    if key in extracted_info:
                        extracted_info[key].append(value)
                    else:
                        extracted_info[key] = [value]  # Initialize a new list with the value
                else:
                    # If there's no valid key-value pair, you can choose to skip or handle it
                    extracted_info[parts[0]] = [' ']  # Store the text as a key with a space as value in a list
            elif element.name == 'table':
                # For tables, create a nested dictionary
                table_data = {}
                rows = element.find_all('tr')
                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) >= 2:
                        key = cols[0].get_text(strip=True)
                        value = cols[1].get_text(strip=True)
                        # Append value to the list for the key, or create a new list if the key doesn't exist
                        if key in table_data:
                            table_data[key].append(value)
                        else:
                            table_data[key] = [value]  # Initialize a new list with the value
                extracted_info['Table Data'] = table_data

        if '凶' in extracted_info['您姓名的天地人三才配置为'][0]:
            print(f"名字 {mz} " + "天地人三才配置为凶" + " 不入选")
            return
        print(f"名字 {mz} " + "天地人三才配置为吉" + " 继续考察五格数理。。。")
        
        for i in range(len(extracted_info['『数理』'])):
            if '凶' in extracted_info['『数理』'][i]:
                print(f"名字 {mz} " + "五格数理有凶" + " 不入选")
                return
        print(f"名字 {mz} " + "五格数理都为吉" + " 入选！")

        # Create a directory to store output files
        output_dir = 'qualified_names'
        os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist

        output_filename = os.path.join(output_dir, f"{mz}.txt") # Create a filename based on the mz value
        with open(output_filename, 'w', encoding='utf-8') as output_file:
            output_file.write(json.dumps(extracted_info, ensure_ascii=False, indent=4))
        
        print(f"信息已保存到 {output_filename}，请查看文件以获取更多信息。")
    else:
        print("No content found in <div class='read-content'>.")

    

# Set up argument parsing
parser = argparse.ArgumentParser(description='Process names for scoring.')
parser.add_argument('--mz', type=str, help='Single name to be processed.')
parser.add_argument('-f', '--file', type=str, help='File containing names to be processed.')

args = parser.parse_args()

# Determine mz values based on input arguments
if args.mz:
    mz_values = [args.mz]  # Single name provided
elif args.file:
    with open(args.file, 'r', encoding='utf-8') as file:
        mz_values = file.read().strip().split('，')  # Read names from the specified file
else:
    parser.print_help()  # Print help information
    exit(1)  # Exit the program

# Use a thread pool to start 10 threads
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = []
    for mz in mz_values:
        mz = mz.strip()  # Clean up any whitespace
        future = executor.submit(perform_request, mz)
        futures.append(future)
        
        time.sleep(1)  # Sleep for 1 second before starting a new thread 


    # Optionally, wait for all threads to complete and process results
    for future in futures:
        try:
            result = future.result()  # Get the result of the thread
            #print(result)  # Print or process the result as needed
        except Exception as e:
            print(f"An error occurred: {e}")

