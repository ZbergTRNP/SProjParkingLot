import cv2
import yaml
from coordinates_generator import CoordinatesGenerator
from motion_detector import MotionDetector
from vidstab import VidStab
import gradio as gr
import time

# Testing Variables
image_file = 'carParkImg.png'
data_base = 'data/coordinates.yml'
filepath = 'carPark.mp4'
start_frame = 1

# Stabilizes Output (Have to Find a Way to Do This Outside of Videos)
stabilizer = VidStab()
stabilizer.stabilize(input_path=filepath, output_path=filepath.replace('.mp4', '') + 'StbOut.avi')
video_file = filepath.replace('.mp4', '') + 'StbOut.avi'

# Sets Up For Demo
data_file = data_base.replace('/', '/' + video_file.replace('.avi', ''))
init = open(data_base.replace('/', '/' + video_file.replace('.avi', '')), "w")
init.close()

# Sets Up Image Analysis
def img(Stream_Link):
    global data_file, imageName
    if Stream_Link is not None:
        vidCap = cv2.VideoCapture(Stream_Link)
        if vidCap.isOpened():
            time.sleep(0.5)
            ret, frame = vidCap.read()  # capture a frame from live video
            imageName = Stream_Link.replace('.avi', '') + 'img.jpg'
            f = open(data_base.replace('/', '/' + video_file.replace('.avi', '')), "w")
            data_file = data_base.replace('/', '/' + video_file.replace('.avi', ''))
            f.close()
            cv2.imwrite(imageName, frame)
        with open(data_file, "w+") as points:
            generator = CoordinatesGenerator(imageName, points, (255, 0, 0))
            generator.generate()
    return data_file

# Sets Up Motion Detection
def vid(streamInput, dataFile):
    while True:
        with open(dataFile, "r") as data:
            points = yaml.safe_load(data)
            detector = MotionDetector(streamInput, points, int(start_frame))
            detector.detect_motion()
            # Experimental
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

# Sets Up Web-Face
with gr.Blocks() as demo:
    gr.Markdown("Analyze Parking Lots With This Demo.")
    with gr.Tab("Parking Lot Analysis"):
        with gr.Row():
            text_input = gr.Textbox(placeholder="Stream Link Here: ")
        with gr.Row():
            output = gr.File(interactive=False)
        text_button = gr.Button("Analyze")
    with gr.Tab("Motion Detector"):
        with gr.Row():
            strmInput = gr.Textbox(label="Input Stream:", placeholder="Stream Link Here: ")
            data_input = gr.File(label="Input Analyzed Lot", interactive=True)
        video_button = gr.Button("Detect")
    text_button.click(img, inputs=text_input, outputs=output)
    video_button.click(vid, inputs=[strmInput, data_input], outputs=None)
demo.launch()
