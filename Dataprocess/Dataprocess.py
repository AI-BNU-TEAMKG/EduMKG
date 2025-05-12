import docx
from moviepy import VideoFileClip
import time
import concurrent.futures
import re
import google.generativeai as genai
import os
from http import HTTPStatus
import dashscope
# Set the proxy 
os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"
LLM_cnt = 1

def format_transfer(input_file,output_file):
    video = VideoFileClip(input_file)
    video.audio.write_audiofile(output_file)
    video.close()

def extract_time_coded_content(file_path):
    
    doc = docx.Document(file_path)
    
    full_text = '\n'.join([para.text for para in doc.paragraphs])
    

    lines = full_text.split('\n')
    

    time_coded_content = {}
    

    current_time_code = None
    current_content = []
    
    for line in lines:

        if line.startswith('发言人') and ' ' in line:

            if current_time_code:
                time_coded_content[current_time_code] = ' '.join(current_content).strip()
                current_content = []
            

            time_code = line.split()[1]
            current_time_code = time_code
        elif current_time_code:

            current_content.append(line)
    

    if current_time_code:
        time_coded_content[current_time_code] = ' '.join(current_content).strip()
    

    formatted_output = []
    time_codes = sorted(list(time_coded_content.keys()))
    for i in range(len(time_codes)-1):
        start_time = time_codes[i]
        end_time = time_codes[i+1]
        content = time_coded_content[start_time]
        formatted_output.append(f"{start_time}-{end_time}: {content}")
    
    return formatted_output

def extract_timestamp_conversation(file_path):
    output_file_path = file_path.replace('_原文.docx', '.txt')  
    try:
        results = extract_time_coded_content(file_path)
        

        with open(output_file_path, 'w', encoding='utf-8') as f:
            for result in results:

                time_range, content = result.split(': ', 1)
                

                f.write(f'"{time_range}": "{content}"\n')
        
        print(f"Results have been written to {output_file_path}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

def get_filenames_recursive(directory, dataType):

    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith(dataType):
                files.append(os.path.join(root, filename))
    return files

def process_file(mp4_path):


    file_prefix = os.path.splitext(os.path.basename(mp4_path))[0]

    output_dir = os.path.dirname(mp4_path)
    output_path = os.path.join(output_dir, f"{file_prefix}.mp3")

    counter = 1
    while os.path.exists(output_path):
        output_path = os.path.join(output_dir, f"{file_prefix}_{counter}.mp3")
        counter += 1
    print(f"Converting {mp4_path} to {output_path}")
    format_transfer(mp4_path, output_path)

def parse_timestamps(text_file):

    timestamps = {}
    
    with open(text_file, 'r', encoding='utf-8') as f:
        content = f.read()
    

    pattern = r'"(\d{2}:\d{2}-\d{2}:\d{2})"\s*:\s*"([^"]*)"'
    matches = re.findall(pattern, content)
    
    for timestamp, description in matches:

        def time_to_seconds(time_str):
            mins, secs = map(int, time_str.split(':'))
            return mins * 60 + secs
        
        start, end = timestamp.split('-')
        start_sec = time_to_seconds(start)
        end_sec = time_to_seconds(end)
        
 
        key = f"clip_{start.replace(':', '_')}"
        timestamps[key] = (start_sec, end_sec, description)
    
    return timestamps

def trim_video(input_video, output_video, timestamps) -> None:



    video = VideoFileClip(input_video)


    input_folder_name = os.path.basename(os.path.dirname(input_video))
    output_folder = os.path.join(os.path.dirname(input_video), input_folder_name)


    os.makedirs(output_folder, exist_ok=True)


    for clip_name, (start, end, content) in timestamps.items():
        try:

            clip = video.subclipped(start, end)
            

            safe_content = ''.join(c for c in content[:20] if '\u4e00' <= c <= '\u9fff')
            output_filename = os.path.join(output_folder, f"{clip_name}_{safe_content}.mp4")
            

            clip.write_videofile(
                output_filename, 
                codec='libx264', 
                audio_codec='aac' 
            )
            
            print(f" {clip_name}: {start}s - {end}s")
        
        except Exception as e:
            print(f" {clip_name} : {e}")
    

    video.close()

def clipVideo(video) -> None:
    input_file = video
    output_file = video.replace('.mp4', '')
    timestamps = parse_timestamps('\\'.join(input_file.split('\\')[:-1]) + '\\' + '\\'.join(input_file.split('\\')[-2:-1])+ '_.txt')
    trim_video(input_file, output_file, timestamps)

def LLM_SemanticIntegration(filepath: list, LLM_cnt: int) -> str:

    for index,file in enumerate(filepath):
        with open(file, 'r', encoding='utf-8') as f:
            if LLM_cnt > 1450:
                return file
            content = f.read()
            LLM_cnt += 1
            response = model.generate_content("现在需要你将下面的音频段落按照语义重新分段，输出格式为“时间戳”：“内容”，“内容不需要你总结，你只负责按照新的时间戳合并原文内容”："+content)
            response = response.text
            f.close()
        with open(file.replace(".txt","_.txt"), 'w', encoding='utf-8') as f:
            print(response)
            f.write(response)
            f.close()

def remove_blank_lines_from_txt(file_path: str) -> None:

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        with open(file_path, 'w', encoding='utf-8') as file:
            for line in lines:
                if line.strip():  
                    file.write(line)
        
        print(f" {file_path} ")
    
    except Exception as e:
        print(f"{e}")

   
if __name__ == "__main__":

    url_list = ""
    
    # # TODO transfer the video to audio
    for item in url_list:
        mp4_files = get_filenames_recursive(item, '.mp4')    
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(process_file, mp4_files)

    #TODO Obtain the time-stamped content from the Word and employ gemini to re-segment the content
    #Before this step, we need to manually convert the audio to text using the online tool / api
    # for item in url_list:
    #      docx_files = get_filenames_recursive(item, '.docx')
    #     with concurrent.futures.ThreadPoolExecutor() as executor:
    #         executor.map(extract_timestamp_conversation, docx_files)
    #  for item in url_list:
    #      txt_files = get_filenames_recursive(item, '.txt')
    #     content = LLM_SemanticIntegration(txt_files, LLM_cnt)
    # for item in url_list:
    #     txt_files = get_filenames_recursive(item, '.txt')
    #     for file in txt_files:
    #        remove_blank_lines_from_txt(file)
 
    # # TODO Trim the video based on the timestamps
    # for item in url_list:
    #     videos = get_filenames_recursive(item, '.mp4')
    #     with concurrent.futures.ThreadPoolExecutor() as executor:
    #         executor.map(clipVideo, videos)





