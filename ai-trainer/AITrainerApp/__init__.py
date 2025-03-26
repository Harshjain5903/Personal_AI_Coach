from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import cv2
import numpy as np
import time
import PoseModule as pm
import sqlite3
import sys
from fpdf import FPDF
import os

# Color Palette
PRIMARY_COLOR = "#3498db"  # Blue
SECONDARY_COLOR = "#2980b9"  # Darker Blue
ACCENT_COLOR = "#f39c12"  # Orange-Yellow
BACKGROUND_COLOR = "#f0f0f0"  # Light Gray
TEXT_COLOR = "#333333"  # Dark Gray

#Import Reportlab Libraries
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import matplotlib.pyplot as plt
from io import BytesIO

# LoginPage Class
class LoginPage(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Personal AI Coach - Login")
        self.setGeometry(0, 0, QtWidgets.QDesktopWidget().availableGeometry().width(),
                         QtWidgets.QDesktopWidget().availableGeometry().height())

        self.setStyleSheet(f"""
            QDialog {{
                background-color: {BACKGROUND_COLOR};
                border-radius: 10px;
            }}
            QLabel {{
                font: bold 30pt 'Roboto';
                color: {TEXT_COLOR};
                text-align: center;
                margin-bottom: 20px;
            }}
            QLineEdit {{
                padding: 12px;
                font: 14pt 'Roboto';
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 8px;
                color: {TEXT_COLOR};
                font-weight: normal;
            }}
            QPushButton {{
                font: bold 16pt 'Roboto';
                background-color: {PRIMARY_COLOR};
                color: white;
                border-radius: 10px;
                padding: 15px 25px;
                margin-top: 20px;
                box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
            }}
            QPushButton:hover {{
                background-color: {SECONDARY_COLOR};
            }}
            QPushButton:pressed {{
                box-shadow: none;
                transform: translate(1px, 1px);
            }}
        """)

        self.layout = QtWidgets.QVBoxLayout()

        self.heading = QtWidgets.QLabel("Login to Personal AI Coach", self)
        self.heading.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.heading)

        self.username = QtWidgets.QLineEdit(self)
        self.username.setPlaceholderText("Username")
        self.password = QtWidgets.QLineEdit(self)
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.layout.addWidget(self.username)
        self.layout.addWidget(self.password)

        self.login_button = QtWidgets.QPushButton("Login", self)
        self.sign_up_button = QtWidgets.QPushButton("Sign Up", self)
        self.layout.addWidget(self.login_button)
        self.layout.addWidget(self.sign_up_button)

        self.setLayout(self.layout)

        self.login_button.clicked.connect(self.check_login)
        self.sign_up_button.clicked.connect(self.show_sign_up)

        self.login_successful = False

    def check_login(self):
        username = self.username.text()
        password = self.password.text()

        if self.validate_login(username, password):
            self.login_successful = True
            self.accept()  # Close the login window and move forward
        else:
            # Use placeholder text to display error message
            self.username.setPlaceholderText("Invalid Username or Password!")
            self.password.clear() # Clear password for re-entry

    def show_sign_up(self):
        sign_up_page = SignUpPage()
        sign_up_page.exec_()

    def validate_login(self, username, password):
        conn = sqlite3.connect('user_credentials.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        result = c.fetchone()
        conn.close()
        return result is not None


# Sign-Up Page
class SignUpPage(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Personal AI Coach - Sign Up")
        self.setGeometry(0, 0, QtWidgets.QDesktopWidget().availableGeometry().width(),
                         QtWidgets.QDesktopWidget().availableGeometry().height())

        self.setStyleSheet(f"""
            QDialog {{
                background-color: {BACKGROUND_COLOR};
                border-radius: 10px;
            }}
            QLabel {{
                font: bold 24pt 'Roboto';
                color: {TEXT_COLOR};
                margin-bottom: 10px;
            }}
            QLineEdit {{
                padding: 12px;
                font: 14pt 'Roboto';
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 8px;
                color: {TEXT_COLOR};
                font-weight: normal;
            }}
            QPushButton {{
                font: bold 16pt 'Roboto';
                background-color: {PRIMARY_COLOR};
                color: white;
                border-radius: 10px;
                padding: 15px 25px;
                margin-top: 20px;
                box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
            }}
            QPushButton:hover {{
                background-color: {SECONDARY_COLOR};
            }}
            QPushButton:pressed {{
                box-shadow: none;
                transform: translate(1px, 1px);
            }}
        """)

        layout = QtWidgets.QVBoxLayout()

        self.username = QtWidgets.QLineEdit(self)
        self.username.setPlaceholderText("Username")
        self.password = QtWidgets.QLineEdit(self)
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirm_password = QtWidgets.QLineEdit(self)
        self.confirm_password.setPlaceholderText("Confirm Password")
        self.confirm_password.setEchoMode(QtWidgets.QLineEdit.Password)

        self.sign_up_button = QtWidgets.QPushButton("Sign Up", self)
        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(self.confirm_password)
        layout.addWidget(self.sign_up_button)

        self.setLayout(layout)

        self.sign_up_button.clicked.connect(self.check_sign_up)

    def check_sign_up(self):
        username = self.username.text()
        password = self.password.text()
        confirm_password = self.confirm_password.text()

        if password == confirm_password:
            self.save_user_credentials(username, password)
            QMessageBox.information(self, "Success", "Account created successfully!") #Popup for successful sign-up
            self.accept()  # Close the sign-up window
        else:
            QMessageBox.warning(self, "Error", "Passwords do not match!") # Use a standard warning popup
            self.password.clear()   #Clear the password fields
            self.confirm_password.clear()


    def save_user_credentials(self, username, password):
        conn = sqlite3.connect('user_credentials.db')
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()


# Exercise Selection Page
class ExerciseSelectionPage(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Personal AI Coach - Choose Exercise")
        self.setGeometry(0, 0, QtWidgets.QDesktopWidget().availableGeometry().width(),
                         QtWidgets.QDesktopWidget().availableGeometry().height())

        self.setStyleSheet(f"""
            QDialog {{
                background-color: {BACKGROUND_COLOR};
                border-radius: 10px;
            }}
            QLabel {{
                font: bold 30pt 'Roboto';
                color: {TEXT_COLOR};
                text-align: center;
                margin-bottom: 20px;
            }}
            QPushButton {{
                font: bold 18pt 'Roboto';
                background-color: {PRIMARY_COLOR};
                color: white;
                border-radius: 15px;
                padding: 20px;
                margin-top: 20px;
                width: 200px;
                height: 200px;
                text-align: center;  /* Center the text */
            }}
            QPushButton:hover {{
                background-color: {SECONDARY_COLOR};
            }}
            QPushButton:pressed {{
                box-shadow: none;
                transform: translate(1px, 1px);
            }}
        """)

        self.layout = QtWidgets.QVBoxLayout()

        self.heading = QtWidgets.QLabel("Choose an Exercise", self)
        self.heading.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.heading)

        self.buttons_layout = QtWidgets.QHBoxLayout()
        self.buttons_layout.setAlignment(QtCore.Qt.AlignCenter) # Center the buttons horizontally

        # Placeholder - Replace with actual icon paths
        icon_size = QtCore.QSize(80, 80)
        self.bicep_button = self.create_exercise_button("Bicep Curl", "icons/bicep.png", icon_size)
        self.pushup_button = self.create_exercise_button("Push-Up", "icons/pushup.png", icon_size)
        self.squats_button = self.create_exercise_button("Squats", "icons/squats.png", icon_size)
        self.deadlift_button = self.create_exercise_button("Deadlifts", "icons/deadlift.png", icon_size)

        self.buttons_layout.addWidget(self.bicep_button)
        self.buttons_layout.addWidget(self.pushup_button)
        self.buttons_layout.addWidget(self.squats_button)
        self.buttons_layout.addWidget(self.deadlift_button)

        self.layout.addLayout(self.buttons_layout)
        self.setLayout(self.layout)

        self.bicep_button.clicked.connect(self.select_bicep_curl)
        self.pushup_button.clicked.connect(self.select_push_up)
        self.squats_button.clicked.connect(self.select_squats)
        self.deadlift_button.clicked.connect(self.select_deadlift)

    def create_exercise_button(self, text, icon_path, icon_size):
        button = QtWidgets.QPushButton(text, self)
        if os.path.exists(icon_path):
            icon = QtGui.QIcon(icon_path)
            button.setIcon(icon)
            button.setIconSize(icon_size)
            button.setText(f"\n{text}") # Add a newline for icon above text
            button.setStyleSheet(f"text-align: center; padding-top: 10px;") #padding above text
        return button

    def select_bicep_curl(self):
        self.exercise = "Bicep Curl"
        self.open_video_or_webcam_page()

    def select_push_up(self):
        self.exercise = "Push-Up"
        self.open_video_or_webcam_page()

    def select_squats(self):
        self.exercise = "Squats"
        self.open_video_or_webcam_page()

    def select_deadlift(self):
        self.exercise = "Deadlifts"
        self.open_video_or_webcam_page()

    def open_video_or_webcam_page(self):
        video_webcam_page = VideoWebcamPage(self.exercise)
        video_webcam_page.exec_()


# Video or Webcam Selection Page
class VideoWebcamPage(QtWidgets.QDialog):
    def __init__(self, exercise):
        super().__init__()

        self.exercise = exercise
        self.setWindowTitle(f"Personal AI Coach - {self.exercise} Workout")
        self.setGeometry(0, 0, QtWidgets.QDesktopWidget().availableGeometry().width(),
                         QtWidgets.QDesktopWidget().availableGeometry().height())

        self.setStyleSheet(f"""
            QDialog {{
                background-color: {BACKGROUND_COLOR};
                border-radius: 10px;
            }}
            QLabel {{
                font: bold 30pt 'Roboto';
                color: {TEXT_COLOR};
                text-align: center;
                margin-bottom: 20px;
            }}
            QPushButton {{
                font: bold 18pt 'Roboto';
                background-color: {PRIMARY_COLOR};
                color: white;
                border-radius: 15px;
                padding: 20px;
                margin-top: 20px;
                width: 300px;
                height: 150px;
            }}
            QPushButton:hover {{
                background-color: {SECONDARY_COLOR};
            }}
            QPushButton:pressed {{
                box-shadow: none;
                transform: translate(1px, 1px);
            }}
        """)

        self.layout = QtWidgets.QVBoxLayout()

        self.heading = QtWidgets.QLabel(f"Choose to {self.exercise} from the following", self)
        self.heading.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.heading)

        self.upload_button = QtWidgets.QPushButton("Upload Video", self)
        self.start_button = QtWidgets.QPushButton("Start Webcam", self)

        self.buttons_layout = QtWidgets.QHBoxLayout()
        self.buttons_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.buttons_layout.addWidget(self.upload_button)
        self.buttons_layout.addWidget(self.start_button)

        self.layout.addLayout(self.buttons_layout)

        self.setLayout(self.layout)

        self.upload_button.clicked.connect(self.upload_video)
        self.start_button.clicked.connect(self.start_webcam)

    def upload_video(self):
        self.video_path, _ = QFileDialog.getOpenFileName(self, "Upload Video", "", "Video Files (*.mp4 *.avi)")
        if self.video_path:
            self.open_workout_page(is_video=True)

    def start_webcam(self):
        self.video_path = None  # Set video_path to None
        self.open_workout_page(is_video=False)

    def open_workout_page(self, is_video=False):
        workout_page = WorkoutPage(self.exercise, is_video, self.video_path)
        workout_page.exec_()


# Workout Page (Live Workout with Webcam)
class WorkoutPage(QtWidgets.QDialog):
    def __init__(self, exercise, is_video, video_path):
        super().__init__()

        self.exercise = exercise
        self.is_video = is_video
        self.video_path = video_path
        self.setWindowTitle(f"Personal AI Coach - {self.exercise} Workout")
        self.setGeometry(0, 0, QtWidgets.QDesktopWidget().availableGeometry().width(),
                         QtWidgets.QDesktopWidget().availableGeometry().height())

        self.setStyleSheet(f"""
            QDialog {{
                background-color: #2c3e50; /* Darker Background for Focus */
                border-radius: 10px;
            }}
            QLabel {{
                font: bold 24pt 'Roboto';
                color: white;
                text-align: center;
            }}
            QPushButton {{
                font: bold 14pt 'Roboto';
                background-color: {PRIMARY_COLOR};
                color: white;
                border-radius: 10px;
                padding: 15px;
                margin-top: 10px;
                width: 100px;
                height: 50px;
            }}
            QPushButton:hover {{
                background-color: {SECONDARY_COLOR};
            }}
            QPushButton:pressed {{
                box-shadow: none;
                transform: translate(1px, 1px);
            }}
        """)

        self.layout = QtWidgets.QVBoxLayout()

        # Rep Count Label above the video feed
        self.rep_count_label = QtWidgets.QLabel("Count: 0", self)
        self.rep_count_label.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.rep_count_label)

        self.video_label = QtWidgets.QLabel(self)
        self.video_label.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.video_label)

        self.button_layout = QtWidgets.QHBoxLayout()
        self.button_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.start_button = QtWidgets.QPushButton("Start")
        self.stop_button = QtWidgets.QPushButton("Stop")
        self.reset_button = QtWidgets.QPushButton("Reset")
        self.exit_button = QtWidgets.QPushButton("Exit")
        self.download_button = QtWidgets.QPushButton("Download Report")

        self.button_layout.addWidget(self.start_button)
        self.button_layout.addWidget(self.stop_button)
        self.button_layout.addWidget(self.reset_button)
        self.button_layout.addWidget(self.exit_button)
        self.button_layout.addWidget(self.download_button)

        self.layout.addLayout(self.button_layout)
        self.setLayout(self.layout)

        self.start_button.clicked.connect(self.start)
        self.stop_button.clicked.connect(self.stop)
        self.reset_button.clicked.connect(self.reset)
        self.exit_button.clicked.connect(self.exit_app)
        self.download_button.clicked.connect(self.download_report)

        self.detector = pm.poseDetector()
        self.count = 0
        self.dir = 0
        self.incorrect_reps = 0
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_frame)

        self.start_time = None  # Start time for duration

        # Exercise-specific parameters
        self.exercise_params = {
            "Bicep Curl": {
                "angle_points": (12, 14, 16),  # Shoulder, Elbow, Wrist
                "angle_range": (210, 310),  # Example range (adjust as needed)
                "reps_direction": (0, 1),  # Example directions for reps
            },
            "Push-Up": {
                "angle_points": (11, 13, 15),  # Shoulder, Elbow, Wrist (Left Arm)
                "angle_range": (170, 280),  # Adjusted range for easier push-ups, this range will more appropriate
                "reps_direction": (0, 1),  # Direction for counting reps
                "lower_threshold": 230,    # Angle to be considered 'down' position, lower will cause repititions
                "upper_threshold": 250      # Angle to be considered 'up' position, increased so even when a little above the ground it counts as a push up
            },
            "Squats": {
                "angle_points": (23, 25, 27),  # Hip, Knee, Ankle (one side)
                "angle_range": (90, 170),
                "reps_direction": (0, 1)  #Example
            },
            "Deadlifts": {
                "angle_points": (11, 23, 25),  # Example Points (adjust)
                "angle_range": (90, 170),
                "reps_direction": (0, 1)   #Example
            }
        }

        # Set exercise params based on the selected exercise
        self.angle_points = self.exercise_params[self.exercise]["angle_points"]
        self.angle_range = self.exercise_params[self.exercise]["angle_range"]
        self.reps_direction = self.exercise_params[self.exercise]["reps_direction"]

        # Setting exercise parameter for pushups if this exercise is selected
        if self.exercise == "Push-Up":
            self.lower_threshold = self.exercise_params[self.exercise]["lower_threshold"]
            self.upper_threshold = self.exercise_params[self.exercise]["upper_threshold"]

        if self.is_video:
            self.cap = cv2.VideoCapture(self.video_path)
        else:
            self.cap = cv2.VideoCapture(0)

        self.is_rep_started = False  # Flag to track if a rep has started
        self.last_angle = None # Store the last angle

    def start(self):
        if self.start_time is None:  # Only set the start time once
            self.start_time = time.time()
        self.timer.start(30)

    def stop(self):
        if self.cap:
            self.cap.release()
        self.timer.stop()

    def reset(self):
        self.count = 0
        self.dir = 0
        self.incorrect_reps = 0
        self.rep_count_label.setText(f"Count: {int(self.count)}")
        self.is_rep_started = False # Also reset this value

    def exit_app(self):
        self.close()

    def update_frame(self):
        success, img = self.cap.read()
        if not success:
            return

        img = cv2.resize(img, (1280, 720))
        img = self.detector.findPose(img, False)
        lmList = self.detector.findPosition(img, False)

        per = 0  # Default value for `per`
        color = (255, 0, 255)  # Assign a default value
        bar = 0 # Assign a default value
        if len(lmList) != 0:
            p1, p2, p3 = self.angle_points
            angle = self.detector.findAngle(img, p1, p2, p3)

            # Push-up-specific counting logic
            if self.exercise == "Push-Up":
                if angle < self.lower_threshold and self.dir == 0:
                    if not self.is_rep_started: #Check if the rep has been started to prevent counting incorect reps
                        self.is_rep_started = True #Rep is started
                    self.dir = 1  # Transition to the 'up' position (coming up from the ground)
                elif angle > self.upper_threshold and self.dir == 1:
                    if self.is_rep_started: # Checking if the rep was started to prevent counting incorect reps
                        self.count += 0.5
                        self.is_rep_started = False #Rep is completed
                    self.dir = 0  # Transition to the 'down' position (going towards the ground)
                per = np.interp(angle, self.angle_range, (0, 100))  # Calculate 'per'
                bar = np.interp(angle, (self.angle_range[0], self.angle_range[1]), (650, 100))  # Calculate 'bar'

            else:
                per = np.interp(angle, self.angle_range, (0, 100))
                bar = np.interp(angle, (self.angle_range[0]+10, self.angle_range[1]-10), (650, 100))

                color = (255, 0, 255)
                if per == 100:
                    if not self.is_rep_started: #Check if the rep has been started to prevent counting incorect reps
                        self.is_rep_started = True #Rep is started
                    color = (0, 255, 0)
                    if self.dir == self.reps_direction[0]:
                        if self.is_rep_started: # Checking if the rep was started to prevent counting incorect reps
                            self.count += 0.5
                            self.is_rep_started = False #Rep is completed
                        self.dir = self.reps_direction[1]
                if per == 0:
                    if not self.is_rep_started: #Check if the rep has been started to prevent counting incorect reps
                        self.is_rep_started = True #Rep is started
                    color = (0, 255, 0)
                    if self.dir == self.reps_direction[1]:
                        if self.is_rep_started: # Checking if the rep was started to prevent counting incorect reps
                            self.count += 0.5
                            self.is_rep_started = False #Rep is completed
                        self.dir = self.reps_direction[0]
            # Incorrect posture counting
            if self.last_angle is not None and self.is_rep_started: #Adding the is_rep_started condition to prevent counting an incorect rep multiple times if it is already being considered correct rep
                #For push ups
                if self.exercise == "Push-Up":
                    if angle < self.lower_threshold and angle < self.upper_threshold and not self.is_rep_started:
                        self.incorrect_reps += 0.5
                        self.is_rep_started = False # Rep is incompelete
                else:
                    #For Bicep Curl, Squats, Deadlifts
                    if per < 100 and per > 0 and not self.is_rep_started:
                        self.incorrect_reps += 0.5
                        self.is_rep_started = False # Rep is incompelete
            self.last_angle = angle

            # Update counter label
            self.rep_count_label.setText(f"Count: {int(self.count)}")
            cv2.rectangle(img, (1100, 100), (1175, 650), color, 3)
            cv2.rectangle(img, (1100, int(bar)), (1175, 650), color, cv2.FILLED)
            cv2.putText(img, f'{int(per)}%', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 4, color, 4)

            # Display rep count inside the screen
            cv2.putText(
                img,
                f'Count: {int(self.count)}',
                (50, 670),
                cv2.FONT_HERSHEY_SIMPLEX,
                3,
                (255, 0, 0),
                10
            )

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, ch = img_rgb.shape
        bytes_per_line = ch * w
        convert_to_qt_format = QtGui.QImage(img_rgb.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(convert_to_qt_format)
        self.video_label.setPixmap(pixmap)

    def download_report(self):
        # Calculate duration
        if self.start_time is not None:
            duration = time.time() - self.start_time
            minutes = int(duration // 60)
            seconds = int(duration % 60)
        else:
            minutes = 0
            seconds = 0

        # Prompt user for location to save the file
        save_path, _ = QFileDialog.getSaveFileName(self, "Save Report", "", "PDF Files (*.pdf)")

        if save_path:
            # Create a fancy report with ReportLab
            doc = SimpleDocTemplate(save_path, pagesize=letter)
            styles = getSampleStyleSheet()
            custom_style = ParagraphStyle(
            name='TitleStyle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.darkblue,
            alignment=1, #TA_CENTER
            spaceAfter=24,
            fontName='Helvetica-Bold'
                )
            elements = []

            # Title
            title_text = f"Workout Report: {self.exercise}"
            title = Paragraph(title_text, custom_style)

            elements.append(title)
            elements.append(Spacer(1, 12))

            # Workout Summary
            summary_text = f"""
                <b>Exercise:</b> {self.exercise}<br/>
                <b>Reps Completed:</b> {int(self.count)}<br/>
                <b>Incorrect Posture Reps:</b> {int(self.incorrect_reps)}<br/>
                <b>Duration:</b> {minutes} min {seconds} sec
            """
            summary = Paragraph(summary_text, styles['Normal'])
            elements.append(summary)
            elements.append(Spacer(1, 12))

            # Create a sample bar chart for reps
            reps_data = {'Correct': int(self.count) - int(self.incorrect_reps), 'Incorrect': int(self.incorrect_reps)}
            fig, ax = plt.subplots()
            bars = ax.bar(reps_data.keys(), reps_data.values(), color=['green', 'red'])
            ax.set_ylabel('Number of Reps')
            ax.set_title('Correct vs. Incorrect Reps')
            # Add value labels on bars
            for bar in bars:
                yval = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), ha='center', va='bottom')
            # Convert plot to image
            buf = BytesIO()
            plt.savefig(buf, format='png')
            plt.close(fig)
            rep_chart = Image(buf, width=4*inch, height=3*inch) #Scale the image to fit the report
            elements.append(rep_chart)
            elements.append(Spacer(1, 12))

            # Analysis and Recommendations
            analysis_text = "<br/><b>Analysis and Recommendations:</b><br/>"
            if self.exercise == "Push-Up":
                if self.count < 10:
                    analysis_text += "Consider lowering yourself closer to the ground or holding yourself for some time. This will allow you to gain extra strength and improve your pushup quality. <br/>"
                if self.incorrect_reps > (int(self.count) / 2):
                    analysis_text += "Focus on maintaining a straight line from head to heels. Avoid sagging or arching your back during the exercise. <br/>"
            elif self.exercise == "Bicep Curl":
                if self.count < 10:
                    analysis_text += "Focus on slower, controlled movements. This will help you build strength and muscle more effectively. <br/>"
                if self.incorrect_reps > (int(self.count) / 2):
                    analysis_text += "Keep your elbows close to your sides and avoid swinging your body. A slight movement is okay as long as you don't over do it <br/>"
            else:
                analysis_text += "Continue practicing your chosen exercise <br/>"

            analysis = Paragraph(analysis_text, styles['Normal'])
            elements.append(analysis)

            # Build the PDF
            doc.build(elements)

            QtWidgets.QMessageBox.information(self, "Download", "Enhanced report downloaded successfully!")

# Main Function to Start the App
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    login_page = LoginPage()  # Show login page first
    login_page.exec_()  # Show the login dialog

    if login_page.login_successful:  # Check if login was successful
        window = ExerciseSelectionPage()  # Open the exercise selection page
        window.show()  # Show the exercise selection page
        sys.exit(app.exec_())  # Start the event loop