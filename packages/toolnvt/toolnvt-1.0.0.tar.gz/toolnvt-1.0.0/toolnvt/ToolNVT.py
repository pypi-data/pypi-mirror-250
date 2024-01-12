from googleapiclient.discovery import build
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QTextEdit, QPushButton, QComboBox, QTableWidget, \
    QTableWidgetItem, QHeaderView, QAbstractItemView, QSizePolicy, QHBoxLayout, QMessageBox
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QClipboard

import re
from pytube import YouTube


class YouTubeCheckerApp(QWidget):
    def __init__(self):
        super().__init__()

        self.api_key = "AIzaSyAHv_bXQTCvjJdn49rHJHKerCGBPhrjacU"
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Youtube Checker NVT')
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        self.mode_label = QLabel('Select Mode:')
        layout.addWidget(self.mode_label)

        self.mode_combobox = QComboBox()
        self.mode_combobox.addItem('Check Views')
        self.mode_combobox.addItem('Check Link Channel')
        self.mode_combobox.addItem('Check Subscribers')
        self.mode_combobox.addItem('Check Subscribers Min Max')
        layout.addWidget(self.mode_combobox)

        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)

        button_layout = QHBoxLayout()

        check_button = QPushButton('Check')
        check_button.setStyleSheet("background-color: green; color: white;")
        check_button.clicked.connect(self.check)
        button_layout.addWidget(check_button)

        copy_button = QPushButton('Copy All')
        copy_button.setStyleSheet("background-color: yellow; color: black;")
        copy_button.clicked.connect(self.copy_all)
        button_layout.addWidget(copy_button)

        layout.addLayout(button_layout)

        self.table_widget = QTableWidget()
        layout.addWidget(self.table_widget)

        self.setLayout(layout)

        # Set up the table widget
        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(['Link', 'Information'])
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_widget.setSelectionMode(QAbstractItemView.MultiSelection)
        self.table_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def check(self):
        selected_mode = self.mode_combobox.currentText()
        links_text = self.text_edit.toPlainText()
        links = links_text.split('\n')

        # Remove empty lines
        links = [link.strip() for link in links if link.strip()]

        result_info = []

        for link in links:
            if selected_mode == 'Check Views':
                video_id = self.extract_video_id(link)
                if video_id:
                    views = self.get_video_views(video_id)
                    if views is not None:
                        result_info.append({"link": link, "views": views})
                    else:
                        result_info.append({"link": link, "views": "No views"})
                else:
                    result_info.append({"link": link, "views": "Invalid link format"})
            elif selected_mode == 'Check Link Channel':
                channel_link = self.get_channel_link(link)
                if channel_link:
                    result_info.append({"link": link, "channel_link": channel_link})
                else:
                    result_info.append({"link": link, "channel_link": "Error retrieving channel link"})
            elif selected_mode == 'Check Subscribers':
                channel_id = self.extract_channel_id(link)
                if channel_id:
                    subscribers = self.get_channel_subscribers(channel_id)
                    result_info.append({"link": link, "subscribers": subscribers})
                else:
                    result_info.append({"link": link, "subscribers": "Invalid channel link format"})
            elif selected_mode == 'Check Subscribers Min Max':
                channel_id = self.extract_channel_id(link)
                if channel_id:
                    subscribers = self.get_channel_subscribers(channel_id)
                    result_info.append({"link": link, "subscribers": subscribers})
                else:
                    result_info.append({"link": link, "subscribers": "Invalid channel link format"})

        if selected_mode == 'Check Subscribers Min Max':
            # Sort the result_info list by the number of subscribers from low to high
            result_info.sort(key=lambda x: x.get("subscribers", float('inf')))

        self.show_result_in_table(result_info)

    def show_result_in_table(self, result_info):
        self.table_widget.clearContents()
        self.table_widget.setRowCount(len(result_info))

        for row, info in enumerate(result_info):
            link_item = QTableWidgetItem(info['link'])
            self.table_widget.setItem(row, 0, link_item)

            if 'views' in info:
                views_item = QTableWidgetItem(f" {info['views']}")
                self.table_widget.setItem(row, 1, views_item)
            elif 'channel_link' in info:
                channel_link_item = QTableWidgetItem(f"C {info['channel_link']}")
                self.table_widget.setItem(row, 1, channel_link_item)
            elif 'subscribers' in info:
                subscribers_item = QTableWidgetItem(f" {info['subscribers']}")
                self.table_widget.setItem(row, 1, subscribers_item)

        # Resize columns and rows to contents
        self.table_widget.resizeColumnsToContents()
        self.table_widget.resizeRowsToContents()

    def extract_video_id(self, link):
        video_id_match = re.match(
            r'^.*(?:youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*', link)
        return video_id_match.group(1) if video_id_match and len(video_id_match.groups()) > 0 else None

    def extract_channel_id(self, link):
        user_match = re.search(
            r'^.*(?:youtube\.com\/@|youtube\.com\/user\/)([^#\&\?\/]+).*', link)
        if user_match and len(user_match.groups()) > 0:
            return user_match.group(1)

        channel_match = re.search(
            r'^.*(?:youtube\.com\/channel\/)([^#\&\?\/]+).*', link)
        return channel_match.group(1) if channel_match and len(channel_match.groups()) > 0 else None

    def get_video_views(self, video_id):
        youtube = build('youtube', 'v3', developerKey=self.api_key)
        request = youtube.videos().list(
            part='statistics',
            id=video_id
        )
        response = request.execute()
        return response['items'][0]['statistics']['viewCount'] if 'items' in response and response['items'] else None

    def get_channel_subscribers(self, channel_id):
        youtube = build('youtube', 'v3', developerKey=self.api_key)
        request = youtube.channels().list(
            part='statistics',
            id=channel_id
        )
        response = request.execute()
        return int(response['items'][0]['statistics']['subscriberCount']) if 'items' in response and response['items'] else 0

    def get_channel_link(self, video_url):
        try:
            yt = YouTube(video_url)
            channel_link = yt.channel_url
            return channel_link
        except Exception as e:
            print(f"Lỗi xảy ra khi xử lý link {video_url}: {e}")
            return None

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_A and event.modifiers() & Qt.ControlModifier:
            self.text_edit.selectAll()

    def copy_all(self):
        selected_mode = self.mode_combobox.currentText()
        result_text = ""
        for row in range(self.table_widget.rowCount()):
            link = self.table_widget.item(row, 0).text()
            information = self.table_widget.item(row, 1).text()
            result_text += f"{link} \t {information}\n"

        clipboard = QApplication.clipboard()
        mime_data = QMimeData()
        mime_data.setText(result_text)
        clipboard.setMimeData(mime_data)

        QMessageBox.information(self, 'Copy All', 'Copied all results to clipboard.')


if __name__ == '__main__':
    app = QApplication([])
    youtube_app = YouTubeCheckerApp()
    youtube_app.show()
    app.exec_()
