import cv2
import numpy as np

# Définir les plages HSV pour les couleurs
color_bounds = {
    "noir": ([0, 0, 0], [180, 255, 30]),
    "blanc": ([0, 0, 200], [180, 30, 255]),
    "rouge1": ([0, 120, 70], [10, 255, 255]),
    "rouge2": ([170, 120, 70], [180, 255, 255]),
    "vert": ([35, 100, 100], [85, 255, 255]),
    "bleu": ([100, 150, 0], [140, 255, 255])
}

selected_color = None

def select_color(event, x, y, flags, param):
    global selected_color
    if event == cv2.EVENT_LBUTTONDOWN:
        if 10 < x < 110:
            if 10 < y < 60:
                selected_color = "noir"
            elif 70 < y < 120:
                selected_color = "blanc"
            elif 130 < y < 180:
                selected_color = "rouge"
            elif 190 < y < 240:
                selected_color = "vert"
            elif 250 < y < 300:
                selected_color = "bleu"

def get_color_bounds(color):
    if color == "noir":
        return [np.array(color_bounds["noir"][0]), np.array(color_bounds["noir"][1])]
    elif color == "blanc":
        return [np.array(color_bounds["blanc"][0]), np.array(color_bounds["blanc"][1])]
    elif color == "rouge":
        return [np.array(color_bounds["rouge1"][0]), np.array(color_bounds["rouge1"][1]), np.array(color_bounds["rouge2"][0]), np.array(color_bounds["rouge2"][1])]
    elif color == "vert":
        return [np.array(color_bounds["vert"][0]), np.array(color_bounds["vert"][1])]
    elif color == "bleu":
        return [np.array(color_bounds["bleu"][0]), np.array(color_bounds["bleu"][1])]

def main():
    global selected_color

    cv2.namedWindow("Selection")
    cv2.setMouseCallback("Selection", select_color)

    while selected_color is None:
        selection_frame = np.zeros((310, 120, 3), dtype=np.uint8)
        
        cv2.rectangle(selection_frame, (10, 10), (110, 60), (0, 0, 0), -1)
        cv2.putText(selection_frame, "Noir", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        cv2.rectangle(selection_frame, (10, 70), (110, 120), (255, 255, 255), -1)
        cv2.putText(selection_frame, "Blanc", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        
        cv2.rectangle(selection_frame, (10, 130), (110, 180), (0, 0, 255), -1)
        cv2.putText(selection_frame, "Rouge", (20, 160), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        cv2.rectangle(selection_frame, (10, 190), (110, 240), (0, 255, 0), -1)
        cv2.putText(selection_frame, "Vert", (20, 220), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        
        cv2.rectangle(selection_frame, (10, 250), (110, 300), (255, 0, 0), -1)
        cv2.putText(selection_frame, "Bleu", (20, 280), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow("Selection", selection_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyWindow("Selection")
    
    if selected_color is None:
        return

    color_bounds = get_color_bounds(selected_color)
    is_red = (selected_color == "rouge")

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        if is_red:
            lower1, upper1, lower2, upper2 = color_bounds
            mask1 = cv2.inRange(hsv, lower1, upper1)
            mask2 = cv2.inRange(hsv, lower2, upper2)
            mask = cv2.bitwise_or(mask1, mask2)
        else:
            lower, upper = color_bounds
            mask = cv2.inRange(hsv, lower, upper)

        # Appliquer des filtres pour réduire le bruit
        mask = cv2.GaussianBlur(mask, (5, 5), 0)
        
        # Trouver les contours
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # Trouver le plus grand contour
            contour = max(contours, key=cv2.contourArea)
            
            # Dessiner le contour en vert
            cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)
            
            # Calculer et dessiner le barycentre en bleu
            M = cv2.moments(contour)
            if M['m00'] != 0:
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                cv2.circle(frame, (cx, cy), 5, (255, 0, 0), -1)
        
        cv2.imshow("Video Frame", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
