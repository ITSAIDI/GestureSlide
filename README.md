# GestureSlide: Control PowerPoint Presentations with Hand Gestures

**GestureSlide** is an advanced web application designed to allow users to control their PowerPoint presentations using hand gestures. It leverages gesture recognition technology to provide a more immersive and interactive presentation experience. GestureSlide is perfect for use in professional presentations, academic lectures, or meetings, enabling smooth slide navigation and control without the need for a remote or mouse.

## Key Features

- **Hand Gesture Control**: Navigate through PowerPoint slides using simple, predefined hand gestures, providing a seamless and touchless experience.
  
- **Real-time Gesture Recognition**: The app uses your device's camera to continuously track hand movements and processes them in real-time to detect gestures.

- **PowerPoint Integration**: Once a gesture is recognized, GestureSlide sends the corresponding command to PowerPoint, enabling actions such as moving to the next or previous slide.

- **No External Devices**: You no longer need a physical remote control or mouse to interact with your presentation.

## How It Works

1. **Camera Activation**: The application uses the device's camera to monitor the user's hand movements during the presentation.
   
2. **Gesture Detection**: Hand gestures are analyzed in real-time, and when a predefined gesture (e.g., swipe left, swipe right) is recognized, the app identifies the corresponding action.We use for that the [MediaPipe](https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker) Model

3. **Slide Control**: Based on the recognized gesture, the App executes the appropriate shortcut on the keyboard  to move between slides or perform other presentation-related tasks.

## Use Cases

- **Professional Presentations**: Perfect for business professionals who want a more engaging way to control their slides.
  
- **Academic Lectures**: Useful for educators or students presenting academic content, freeing up their hands for other tasks.

## Privacy

GestureSlide respects user privacy by processing all gesture recognition locally on the user's device. No third-party services are involved, and no data is sent or stored externally. Your hand movements and video feed remain entirely private.
