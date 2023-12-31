import os
import cv2
import time
import datetime

from utils import CFEVideoConf
import glob

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

frames_per_seconds = 20
save_path = 'saved/timelapse.mp4'
config = CFEVideoConf(cap, filepath=save_path, res='720p')
out = cv2.VideoWriter(save_path, config.video_type, frames_per_seconds, config.dims)
timelapse_img_dir = 'images/timelapse/'
seconds_duration = 40
seconds_between_shots = 0.25

if not os.path.exists(timelapse_img_dir):
    os.mkdir(timelapse_img_dir)

now = datetime.datetime.now()
finish_time = now + datetime.timedelta(seconds=seconds_duration)
i = 0
while datetime.datetime.now() < finish_time:
    '''
    Ensure that the current time is still less
    than the preset finish time
    '''
    ret, frame = cap.read()
    filename = f"{timelapse_img_dir}/{i}.jpg"
    i += 1
    cv2.imwrite(filename, frame)
    time.sleep(seconds_between_shots)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break


def images_to_video(out, image_dir, clear_images=True):
    image_list = glob.glob(f"{image_dir}/*.jpg")
    sorted_images = sorted(image_list, key=os.path.getmtime)
    for file in sorted_images:
        image_frame = cv2.imread(file)
        out.write(image_frame)
    if clear_images:
        '''
        Remove stored timelapse images
        '''


images_to_video(out, timelapse_img_dir)
# When everything done, release the capture
cap.release()
out.release()
cv2.destroyAllWindows()
