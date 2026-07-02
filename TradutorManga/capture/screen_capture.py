import dxcam
import cv2

class ScreenCapture:
    def __init__(self):
        self.camera = dxcam.create(output_color="BGR")

    def get_frame(self):
        frame = self.camera.grab()
        return frame


if __name__ == "__main__":
    cap = ScreenCapture()

    while True:
        frame = cap.get_frame()

        if frame is None:
            continue

        cv2.imshow("Captura da Tela", frame)

        if cv2.waitKey(1) == 27:  # ESC
            break

    cv2.destroyAllWindows()