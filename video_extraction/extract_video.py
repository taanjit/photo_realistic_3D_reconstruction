import os
import numpy as np
import cv2
import shutil

from rembg import remove 
from PIL import Image 
import subprocess



scale_factor=0.1

fps=23.976023976023978
time=9 # 9 second for one rotation
total_frame=int(fps*time)

temp_dir='video_extraction/temp_dir/'
temp_inter='video_extraction/temp_interpolation/'

def list_mp4_files(folder_path):
    list=[]
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".MP4"):
                list.append(os.path.join(root, file))
    return np.sort(list)

def sorting_file(folder_path,folder_name):
    list=[]
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.startswith(folder_name):
                list.append(os.path.join(root, file))
    return np.sort(list)

    


def extract_frames(input_file, num_frames=total_frame):
    
    path, filename = os.path.split(input_file)
    filename, extension = os.path.splitext(filename)

    # os.makedirs(f"{temp_dir}{filename}", exist_ok=True)
      # Calculate interval between extracted frames
    frame_interval = np.ceil(num_frames / 36)
    cap = cv2.VideoCapture(input_file)
    if not cap.isOpened():
        raise Exception("Error opening video file:", input_file)
    frame_count,extracted_frame_count = 0,0
    while frame_count < num_frames:
        ret, frame = cap.read()
        height, width = frame.shape[:2]
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)
        frame = cv2.resize(frame, (new_width, new_height))
        if not ret:
            break
        # Use f-string for cleaner frame number formatting
        if extracted_frame_count < num_frames:
            frame_filename = f"{temp_dir}frame_{extracted_frame_count:04d}_{filename}.png"
            cv2.imwrite(frame_filename, frame)
            extracted_frame_count += 1
        frame_count += frame_interval
    cap.release()


def read_png_files(folder_path):
    png_files = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".png"):
                png_files.append(os.path.join(root, file))
    return np.sort(png_files)



def move_files(source, dest):
        shutil.move(source, dest)


# def run_interpolation_command(dir):
#     command = "python -m eval.interpolator_cli --pattern \"/home/thinkpalm/Documents/My Projects/Frame-Interpolation/frame-interpolation/video_extraction/temp_interpolation/{dir}\" --model_path film_net/Style/saved_model --times_to_interpolate 3 --output_video"
#     subprocess.run(command, shell=True)


def run_interpolation_command(pattern, model_path, times_to_interpolate):
    command = f"python -m eval.interpolator_cli --pattern \"{pattern}\" --model_path {model_path} --times_to_interpolate {times_to_interpolate}"
    subprocess.run(command, shell=True)

if __name__=="__main__":
    # print("function to collect all the video from the uploaded folder")
    # folder_path='video_extraction/input videos/sample1'
    # files=list_mp4_files(folder_path)

    
    # for file in files:
    #     extract_frames(file)

    # frame_list = [f"frame_{i:04d}" for i in range(0, 35 + 1)]
    # folder_list = [frame for frame in frame_list if int(frame[6:]) <= 35]
    # for folder_name in folder_list:
    #     files=sorting_file(temp_dir,folder_name)  
    #     os.makedirs(f"{temp_inter}{folder_name}", exist_ok=True)
    #     for file in files:
    #         move_files(file,f"{temp_inter}{folder_name}")     

    # print("Removing Background ....")
    # files=read_png_files(temp_inter)
    # for file in files:
    #     output=remove(Image.open(file))
    #     output.save(file)


    frame_list = [f"frame_{i:04d}" for i in range(0, 35 + 1)]
    folder_list = [frame for frame in frame_list if int(frame[6:]) <= 35]
    for folder_name in folder_list:
        pattern = f"/home/thinkpalm/Documents/My Projects/Frame-Interpolation/frame-interpolation/video_extraction/temp_interpolation/{folder_name}"
        model_path = "film_net/Style/saved_model"
        times_to_interpolate = 3
        run_interpolation_command(pattern, model_path, times_to_interpolate)





#     python -m eval.interpolator_cli --pattern "/home/thinkpalm/Documents/My Projects/Frame-Interpolation/frame-interpolation/video_extraction/temp_interpolation/frame_0000" --model_path film_net/Style/saved_model --times_to_interpolate 3 --output_video