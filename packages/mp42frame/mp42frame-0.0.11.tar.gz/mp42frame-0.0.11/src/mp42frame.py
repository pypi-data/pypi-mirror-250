import cv2
import sys
import os
import glob

if len(sys.argv) < 2:
    print("enter video name")
    sys.exit()


def conver_image_from_video(input_path, output_path):
    os.makedirs(output_path, exist_ok=True)
    vidcap = cv2.VideoCapture(input_path)
    # success,image = vidcap.read()
    count = 0
    # success = True

    while True:
        success, image = vidcap.read()
        if success == False:
            break
        cv2.imwrite(output_path + "/" + "frame_%d.jpg" % count, image)  # save frame as JPEG file
        if cv2.waitKey(10) == 27:  # exit if Escape is hit
            break
        count += 1

    vidcap.release()


def main():
    if '.mp4' in sys.argv[1]:
        print('convert video ing')
        input_path = sys.argv[1]
        output_path = sys.argv[1].replace('.mp4', '')
        # output_path="pic_result"+"/"+sys.argv[1].replace('.mp4', '')
        conver_image_from_video(input_path, output_path)


    else:
        print('convert %d videos in forlder' % len(glob.glob(sys.argv[1] + '/*.mp4')))
        fileNo = 1

        for filename in glob.glob(sys.argv[1] + '/*.mp4'):
            print("%d " % fileNo + filename + " begins")
            input_path = filename
            output_path = filename.replace('.mp4', '')
            # output_path="pic_result"+"/"+filename.replace('.mp4', '')
            conver_image_from_video(input_path, output_path)
            print("%d " % fileNo + filename + " ended" + "\n")
            fileNo += 1

    print('converting finished')


if __name__ == "__main__":
    main()
