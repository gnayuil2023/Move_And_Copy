import sys
import shutil
import os
import zipfile
from datetime import datetime
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QLabel, QVBoxLayout, QWidget, QMessageBox, QMenuBar

class FileCopyApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置窗口标题和大小
        self.setWindowTitle("Move And Copy")
        self.setGeometry(300, 300, 400, 200)

        # 初始化文件路径和目标路径
        self.source_file = ""
        self.destination_dir = ""

        # 创建菜单栏并添加“关于”和“关闭”按钮
        menu_bar = self.menuBar()

        # 关于按钮
        about_action = menu_bar.addAction("关于")
        about_action.triggered.connect(self.show_about)

        # 关闭按钮
        exit_action = menu_bar.addAction("关闭")
        exit_action.triggered.connect(self.close_application)

        # 创建界面元素
        self.file_label = QLabel("请选择要复制的文件", self)
        self.destination_label = QLabel("请选择目标文件夹", self)

        self.select_file_button = QPushButton("选择文件", self)
        self.select_file_button.clicked.connect(self.select_file)

        self.select_destination_button = QPushButton("选择目标文件夹", self)
        self.select_destination_button.clicked.connect(self.select_destination)

        self.copy_button = QPushButton("开始复制", self)
        self.copy_button.clicked.connect(self.copy_file)

        # 布局
        layout = QVBoxLayout()
        layout.addWidget(self.file_label)
        layout.addWidget(self.select_file_button)
        layout.addWidget(self.destination_label)
        layout.addWidget(self.select_destination_button)
        layout.addWidget(self.copy_button)

        # 主窗口设置
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def show_about(self):
        # 显示关于信息
        QMessageBox.information(self, "关于", "文件复制程序-测试版\n版本: 0.01\n作者: Gnay- Nuctech")

    def close_application(self):
        # 确认关闭应用程序
        reply = QMessageBox.question(self, "确认关闭", "确定要退出程序吗？", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close()

    def select_file(self):
        # 打开文件选择对话框，选择要复制的源文件
        self.source_file, _ = QFileDialog.getOpenFileName(self, "选择文件")
        if self.source_file:
            self.file_label.setText(f"已选择文件: {self.source_file}")

    def select_destination(self):
        # 打开文件夹选择对话框，选择目标目录
        self.destination_dir = QFileDialog.getExistingDirectory(self, "选择目标文件夹")
        if self.destination_dir:
            self.destination_label.setText(f"已选择目标文件夹: {self.destination_dir}")

    def copy_file(self):
        # 检查文件和目录是否已选择
        if not self.source_file or not self.destination_dir:
            QMessageBox.warning(self, "警告", "请先选择文件和目标文件夹")
            return

        # 获取文件名并创建目标路径
        file_name = os.path.basename(self.source_file)
        destination_file = os.path.join(self.destination_dir, file_name)

        # 检查目标文件是否存在
        if os.path.exists(destination_file):
            # 显示确认对话框
            reply = QMessageBox.question(
                self,
                "文件已存在",
                f"{file_name} 已存在于目标文件夹中。\n是否备份原文件并覆盖？",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )

            # 如果用户选择"Yes"，则备份并覆盖
            if reply == QMessageBox.Yes:
                # 生成备份文件夹名称（精确到秒）
                backup_folder_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                backup_folder_path = os.path.join(self.destination_dir, backup_folder_name)

                # 创建备份文件夹
                os.makedirs(backup_folder_path, exist_ok=True)

                # 将原文件压缩并放入备份文件夹
                backup_zip_path = os.path.join(backup_folder_path, f"{file_name}.zip")
                with zipfile.ZipFile(backup_zip_path, 'w') as zipf:
                    zipf.write(destination_file, arcname=file_name)

                # 删除原目标文件
                os.remove(destination_file)
                self.file_label.setText(f"已备份并覆盖文件: {destination_file}")
            else:
                # 用户选择"否"，中止操作
                self.file_label.setText("操作已取消")
                return

        # 复制文件到目标目录
        try:
            shutil.copy(self.source_file, destination_file)
            self.file_label.setText(f"文件已复制到: {destination_file}")
        except Exception as e:
            self.file_label.setText(f"复制失败: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileCopyApp()
    window.show()
    sys.exit(app.exec())
