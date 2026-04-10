from PySide6.QtWidgets import (
    QLabel, QWidget, QTableWidget, QTableWidgetItem, 
    QVBoxLayout, QHeaderView, QMessageBox, QMenu, 
    QPushButton, QHBoxLayout
    )
from PySide6.QtCore import Qt

from DATA.Commands import (
    get_all_college, add_college, delete_college,
    get_all_program, add_program, delete_program,
    get_all_students, add_students, delete_students
    )
from USERVIEW.AddEdit import (
    EditCollegeDialog, EditProgramDialog, EditStudentDialog
    )

ROWS_PER_PAGE = 15 

#COLLEGE FUNCTIONS
class CollegeTable(QWidget):
    def __init__(self):
        super().__init__()
        self.current_page = 0      
        self.filtered_data = []
        self.collegetable_setup()

    def collegetable_setup(self):
        college_Layout = QVBoxLayout()

        self.collegeTable = QTableWidget()
        self.collegeTable.setColumnCount(2)
        self.collegeTable.setHorizontalHeaderLabels(["College Name", "College Code"])
        self.collegeTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.collegeTable.setContextMenuPolicy(Qt.CustomContextMenu)
        self.collegeTable.customContextMenuRequested.connect(self.show_contextMenu)

        college_Layout.addWidget(self.collegeTable)

        page_layout = QHBoxLayout()
        self.prev_btn  = QPushButton("← Prev")
        self.next_btn  = QPushButton("Next →")
        self.page_label = QLabel()
        self.prev_btn.clicked.connect(self.prev_page)
        self.next_btn.clicked.connect(self.next_page)
        page_layout.addStretch()
        page_layout.addWidget(self.prev_btn)
        page_layout.addWidget(self.page_label)
        page_layout.addWidget(self.next_btn)
        page_layout.addStretch()
        college_Layout.addLayout(page_layout)
 
        self.load_collegeTable()
        self.setLayout(college_Layout)

    def load_collegeTable(self):
        self._all_colleges = get_all_college()    
        self.filtered_data = self._all_colleges   
        self.current_page = 0                     
        self.refresh_page()  

    def populate_collegeTable(self, data):
        self.collegeTable.setRowCount(len(data))
        for row_no, college in enumerate(data):
            name_item = QTableWidgetItem(college["college_name"])
            name_item.setData(Qt.UserRole, college["id"])
            self.collegeTable.setItem(row_no, 0, name_item)
            self.collegeTable.setItem(row_no, 1, QTableWidgetItem(college["college_code"]))

    def refresh_page(self):
        total_pages = max(1, -(-len(self.filtered_data) // ROWS_PER_PAGE)) 
        self.current_page = max(0, min(self.current_page, total_pages - 1))
 
        start = self.current_page * ROWS_PER_PAGE
        end   = start + ROWS_PER_PAGE
        self.populate_collegeTable(self.filtered_data[start:end])
 
        self.page_label.setText(f"Page {self.current_page + 1} of {total_pages}")
        self.prev_btn.setEnabled(self.current_page > 0)
        self.next_btn.setEnabled(self.current_page < total_pages - 1)
 
    # go to previous page
    def prev_page(self):
        self.current_page -= 1
        self.refresh_page()
 
    #go to next page
    def next_page(self):
        self.current_page += 1
        self.refresh_page()

    def search(self, text):
        text = text.lower()
        filtered_data = [
            c for c in self._all_colleges
            if text in c["college_name"].lower() or text in c["college_code"].lower()
        ]
        self.current_page = 0  
        self.refresh_page()

    def sort(self, col):
        self.collegeTable.sortItems(col, Qt.AscendingOrder)

    def show_contextMenu(self, postion):
        AE_menu = QMenu()
        edit_action = AE_menu.addAction("Edit")
        delete_action = AE_menu.addAction("Delete")

        action = AE_menu.exec(self.collegeTable.viewport().mapToGlobal(postion))
        
        if action == edit_action:
            self.handle_edit()
        elif action == delete_action:
            self.handle_delete()

    def handle_edit(self):
        row = self.collegeTable.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Error", "Please select a college to edit.")
            return
 
        college_id   = self.collegeTable.item(row, 0).data(Qt.UserRole)
        college_name = self.collegeTable.item(row, 0).text()
        college_code = self.collegeTable.item(row, 1).text()
 
        dialog = EditCollegeDialog(college_id, college_name, college_code, self)
        dialog.college_updated.connect(self.load_collegeTable)
        dialog.exec()

    def handle_delete(self):
        row = self.collegeTable.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Error", "Please select a college to delete.")
            return
 
        college_id   = self.collegeTable.item(row, 0).data(Qt.UserRole)
        college_name = self.collegeTable.item(row, 0).text()
 
        confirm = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete '{college_name}'?\n\n"
            "Warning: This will also delete all associated Programs and "
            "unassign Students!",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            delete_college(college_id)
            self.load_collegeTable()


# PROGRAM FUNCTIONS
class ProgramTable(QWidget):
    def __init__(self):
        super().__init__()
        self.current_page = 0  
        self.filtered_data = []  
        self.programtable_setup()

    def programtable_setup(self):
        program_Layout = QVBoxLayout()

        self.programTable = QTableWidget()
        self.programTable.setColumnCount(3)
        self.programTable.setHorizontalHeaderLabels(["Program Code", "Program Name", "College ID"])
        self.programTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.programTable.setContextMenuPolicy(Qt.CustomContextMenu)
        self.programTable.customContextMenuRequested.connect(self.show_contextMenu)

        program_Layout.addWidget(self.programTable)

        page_layout = QHBoxLayout()
        self.prev_btn   = QPushButton("← Prev")
        self.next_btn   = QPushButton("Next →")
        self.page_label = QLabel()
        self.prev_btn.clicked.connect(self.prev_page)
        self.next_btn.clicked.connect(self.next_page)
        page_layout.addStretch()
        page_layout.addWidget(self.prev_btn)
        page_layout.addWidget(self.page_label)
        page_layout.addWidget(self.next_btn)
        page_layout.addStretch()
        program_Layout.addLayout(page_layout)

        self.load_programTable()
        self.setLayout(program_Layout)

    def load_programTable(self):
        self._all_programs = get_all_program()   
        self.filtered_data = self._all_programs  
        self.current_page  = 0                    
        self.refresh_page()

    def populate_programTable(self, data):
        self.programTable.setRowCount(len(data))
        for row_no, program in enumerate(data):
            code_item = QTableWidgetItem(program["program_code"])
            code_item.setData(Qt.UserRole, program["id"]) 
            self.programTable.setItem(row_no, 0, code_item)
            self.programTable.setItem(row_no, 1, QTableWidgetItem(program["program_name"]))
            self.programTable.setItem(row_no, 2, QTableWidgetItem(str(program["college_code"])))

    def refresh_page(self):
        total_pages = max(1, -(-len(self.filtered_data) // ROWS_PER_PAGE))
        self.current_page = max(0, min(self.current_page, total_pages - 1))
 
        start = self.current_page * ROWS_PER_PAGE
        end   = start + ROWS_PER_PAGE
        self.populate_programTable(self.filtered_data[start:end])
 
        self.page_label.setText(f"Page {self.current_page + 1} of {total_pages}")
        self.prev_btn.setEnabled(self.current_page > 0)
        self.next_btn.setEnabled(self.current_page < total_pages - 1)
 
    def prev_page(self):
        self.current_page -= 1
        self.refresh_page()
 
    def next_page(self):
        self.current_page += 1
        self.refresh_page()

    def search(self, text):
        text = text.lower()
        filtered_data = [
            p for p in self._all_programs
            if text in p["program_code"].lower()
            or text in p["program_name"].lower()
            or text in str(p["college_code"]).lower()
        ]
        self.current_page = 0        
        self.refresh_page()

    def sort(self, col):
        self.programTable.sortItems(col, Qt.AscendingOrder)
 
    def show_contextMenu(self, postion):
        AE_menu = QMenu()
        edit_action = AE_menu.addAction("Edit")
        delete_action = AE_menu.addAction("Delete")

        action = AE_menu.exec(self.programTable.viewport().mapToGlobal(postion))
        
        if action == edit_action:
            self.handle_edit()
        elif action == delete_action:
            self.handle_delete()

    def handle_edit(self):
        row = self.programTable.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Error", "Please select a program to edit.")
            return
 
        program_id   = self.programTable.item(row, 0).data(Qt.UserRole)
        program_code = self.programTable.item(row, 0).text()
        program_name = self.programTable.item(row, 1).text()
        college_code = self.programTable.item(row, 2).text()
 
        dialog = EditProgramDialog(program_id, program_name, program_code, college_code, self)
        dialog.program_updated.connect(self.load_programTable)
        dialog.exec()

    def handle_delete(self):
        row = self.programTable.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Error", "Please select a program to delete.")
            return
 
        program_id   = self.programTable.item(row, 0).data(Qt.UserRole)
        program_name = self.programTable.item(row, 1).text()
 
        confirm = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete '{program_name}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            delete_program(program_id)
            self.load_programTable()


# STUDENT FUNCTIONS
class StudentsTable(QWidget):
    def __init__(self ):
        super().__init__()
        self.current_page = 0       
        self.filtered_data = [] 
        self.studentstable_setup()

    def studentstable_setup(self):
        student_Layout = QVBoxLayout()

        self.studentTable = QTableWidget()
        self.studentTable.setColumnCount(6)
        self.studentTable.setHorizontalHeaderLabels(["Student ID", "First Name", "Last Name", "Gender", "Year", "Program"])
        self.studentTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.studentTable.setContextMenuPolicy(Qt.CustomContextMenu)
        self.studentTable.customContextMenuRequested.connect(self.show_contextMenu)

        student_Layout.addWidget(self.studentTable)

        page_layout = QHBoxLayout()
        self.prev_btn   = QPushButton("← Prev")
        self.next_btn   = QPushButton("Next →")
        self.page_label = QLabel()
        self.prev_btn.clicked.connect(self.prev_page)
        self.next_btn.clicked.connect(self.next_page)
        page_layout.addStretch()
        page_layout.addWidget(self.prev_btn)
        page_layout.addWidget(self.page_label)
        page_layout.addWidget(self.next_btn)
        page_layout.addStretch()
        student_Layout.addLayout(page_layout)

        self.load_studentTable()
        self.setLayout(student_Layout)

    def load_studentTable(self):
        self._all_students = get_all_students()
        self.filtered_data = self._all_students   
        self.current_page  = 0                    
        self.refresh_page()    

    def populate_studentTable(self, data):
        self.studentTable.setRowCount(len(data))
        for row_no, student in enumerate(data):
            sid_item = QTableWidgetItem(student["student_id"])
            sid_item.setData(Qt.UserRole, student["id"])    # store real DB id
            self.studentTable.setItem(row_no, 0, sid_item)
            self.studentTable.setItem(row_no, 1, QTableWidgetItem(student["first_name"]))
            self.studentTable.setItem(row_no, 2, QTableWidgetItem(student["last_name"]))
            self.studentTable.setItem(row_no, 3, QTableWidgetItem(student["gender"]))
            self.studentTable.setItem(row_no, 4, QTableWidgetItem(str(student["year"])))
            program_value = student["program_code"] or "N/A"
            self.studentTable.setItem(row_no, 5, QTableWidgetItem(program_value))

    def refresh_page(self):
        total_pages = max(1, -(-len(self.filtered_data) // ROWS_PER_PAGE))
        self.current_page = max(0, min(self.current_page, total_pages - 1))
 
        start = self.current_page * ROWS_PER_PAGE
        end   = start + ROWS_PER_PAGE
        self.populate_studentTable(self.filtered_data[start:end])
 
        self.page_label.setText(f"Page {self.current_page + 1} of {total_pages}")
        self.prev_btn.setEnabled(self.current_page > 0)
        self.next_btn.setEnabled(self.current_page < total_pages - 1)
 
    def prev_page(self):
        self.current_page -= 1
        self.refresh_page()
 
    def next_page(self):
        self.current_page += 1
        self.refresh_page()

    def search(self, text):
        text = text.lower()
        self.filtered_data = [
            s for s in self._all_students
            if text in s["student_id"].lower()
            or text in s["first_name"].lower()
            or text in s["last_name"].lower()
            or text in s["gender"].lower()
            or text in str(s["year"])
            or text in (s["program_code"] or "").lower()
        ]
        self.current_page = 0      
        self.refresh_page()
 
    def sort(self, col):
        self.studentTable.sortItems(col, Qt.AscendingOrder)
        
    def show_contextMenu(self, postion):
        AE_menu = QMenu()
        edit_action = AE_menu.addAction("Edit")
        delete_action = AE_menu.addAction("Delete")

        action = AE_menu.exec(self.studentTable.viewport().mapToGlobal(postion))
        
        if action == edit_action:
            self.handle_edit()
        elif action == delete_action:
            self.handle_delete()

    def handle_edit(self):
        row = self.studentTable.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Error", "Please select a student to edit.")
            return
 
        db_id      = self.studentTable.item(row, 0).data(Qt.UserRole)  # real DB id
        student_data = {
            "student_id":   self.studentTable.item(row, 0).text(),
            "first_name":   self.studentTable.item(row, 1).text(),
            "last_name":    self.studentTable.item(row, 2).text(),
            "gender":       self.studentTable.item(row, 3).text(),
            "year":         self.studentTable.item(row, 4).text(),
            "program_code": self.studentTable.item(row, 5).text(),
        }
 
        dialog = EditStudentDialog(db_id, student_data, self)
        dialog.student_updated.connect(self.load_studentTable)
        dialog.exec()


    def handle_delete(self):
        row = self.studentTable.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Error", "Please select a student to delete.")
            return
 
        db_id      = self.studentTable.item(row, 0).data(Qt.UserRole)
        student_id = self.studentTable.item(row, 0).text()
 
        confirm = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete student '{student_id}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            delete_students(db_id)
            self.load_studentTable() 