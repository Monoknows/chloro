import cv2
import os

def vision():
    print("[SYSTEM]: Powering on visual sensor lenses...")
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("[VISION ERROR]: Could not open webcam device.")
        return

    window_name = 'Chloro Visual Input Stream'
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    snapshot_path = os.path.join(backend_dir, "snapshot.jpg")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[VISION ERROR]: Failed to read frame.")
            break

        # 🖥️ 1. Display the high-res stream to YOU on your desktop
        cv2.imshow(window_name, frame)

        # 📉 2. Downscale a copy of the frame to a 512px tile for CHLORO
        # This forces the token cost down to the absolute minimum tier (255 tokens)
        chloro_vision_tile = cv2.resize(frame, (512, 384))

        # 📸 3. Overwrite the snapshot with the ultra-lightweight optimized tile
        cv2.imwrite(snapshot_path, chloro_vision_tile, [int(cv2.IMWRITE_JPEG_QUALITY), 70])

        if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
            break

    cap.release()
    cv2.destroyAllWindows()
    if os.path.exists(snapshot_path):
        os.remove(snapshot_path)
    print("[SYSTEM]: Visual cortex arrays powered down cleanly.")