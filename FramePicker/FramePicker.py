import cv2


vid_path = "FramePicker/Videos/2021-12-17_09-35_Evt02-Camera1.avi"


def main():
    print(cv2.__version__)
    # count_frames(vid_path)


def count_frames(path, override=False):
	video = cv2.VideoCapture(path)
	total = 0




if __name__ == "__main__":
    main()