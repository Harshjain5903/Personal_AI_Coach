# Personal AI Coach

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## Project Description

Personal AI Coach is a desktop application built with Python and PyQt5 that provides real-time feedback and guidance for your workouts.  It leverages pose detection using MediaPipe to analyze your movements during exercises such as bicep curls, push-ups, squats, and deadlifts.  The application counts repetitions, identifies incorrect postures, and generates a personalized workout report to help you improve your form and achieve your fitness goals. This provides user authentication allowing them to securely log into their account.  The system also saves user credentials in an SQLite database and the Application is also able to retrieve videos from webcams as well as from uploaded videos.

## Key Features

*   **User Authentication:** Secure login and signup using an SQLite database to store user credentials.
*   **Exercise Selection:** Choose from a variety of exercises including bicep curls, push-ups, squats, and deadlifts.
*   **Video Input:** Analyze your workout from uploaded video files or directly from your webcam.
*   **Pose Detection:** Utilizes MediaPipe for real-time pose estimation and tracking.
*   **Rep Counting:** Automatically counts the number of repetitions performed for each exercise.
*   **Posture Analysis:** Detects incorrect postures and provides feedback to improve form.
*   **Real-time Feedback:** Displays rep count and posture analysis results in a user-friendly interface.
*   **Workout Report Generation:** Generates a detailed workout report in PDF format, including exercise summary, rep count, posture analysis, duration, and personalized recommendations.
*   **Customizable Exercise Parameters:** Configuration of parameters specific to each exercise, such as angle ranges for correct form.

## Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd Personal-AI-Coach
    ```

2.  **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

    Create a `requirements.txt` file with the following content:

    ```
    PyQt5
    opencv-python
    mediapipe
    numpy
    fpdf
    reportlab
    matplotlib
    ```

3.  **Run the application:**

    ```bash
    python __init__.py
    ```

## Usage

1.  **Login or Sign Up:** Create a new account or log in with existing credentials.
2.  **Select Exercise:** Choose the exercise you want to perform (e.g., Bicep Curl, Push-Up).
3.  **Choose Video Source:** Select either "Upload Video" to analyze a pre-recorded video or "Start Webcam" to use your webcam for real-time analysis.
4.  **Start Workout:** Click the "Start" button to begin the exercise.
5.  **Perform Exercise:** Follow the on-screen feedback to maintain proper form and count repetitions.
6.  **Stop Workout:** Click the "Stop" button to pause the analysis.
7.  **Reset Workout:** Click the "Reset" button to reset rep count and other parameters.
8.  **Download Report:** Click the "Download Report" button to generate a PDF report of your workout.
9.  **Exit Application:** Click the "Exit" button to close the app.

## Contributing

We welcome contributions to the Personal AI Coach project! To contribute:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Make your changes and commit them with descriptive commit messages.
4.  Submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Credits/Acknowledgments

*   Built with PyQt5.
*   Pose detection powered by MediaPipe.
*   PDF report generation with ReportLab.
*   GUI Design inspired by Modern UI/UX principles.

## Future Enhancements
* Implementing Additional Exercise Routines: Expand the range of supported exercises to offer users a more comprehensive fitness tracking solution.
* Enhancing User Interface/User Experience (UI/UX): Make design more visually appealing and intuitive and provide a more engaging and user friendly environment
* Integrating Advanced Analytics and Performance Tracking: Integrate machine learning to track user progreess
