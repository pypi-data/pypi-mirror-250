from logging import Logger
from typing import Union, List
from datetime import date
from .adapter import Adapter
from .models import Employee, Category, Position, Shift, TimeOff


class Client:
    def __init__(self, hostname: str, api_key: str, ssl_verify: bool = True, logger: Logger = None):
        self._adapter = Adapter(hostname, api_key, ssl_verify, logger)
        self.company_id: int = 0
        self.employees: List[Employee] = []
        self.positions: List[Position] = []
        self.categories: List[Category] = []
        self._update_company()

    def _update_company(self):
        self._update_employees()
        self.company_id = self.employees[0].company_id
        self._update_positions()
        self._update_categories()

    def _update_employees(self):
        self.employees = self._adapter.get_from_endpoint('EmployeeList')

    def _update_positions(self):
        self.positions = self._adapter.get_from_endpoint('PositionList')

    def _update_categories(self):
        self.categories = self._adapter.get_from_endpoint('CategoryList')

    def _add_emp_pos_cat_to_shift(self, shift: Shift):
        shift.employee = self.get_employee_by_id(shift.w2w_employee_id)
        shift.position = self.get_position_by_id(shift.position_id)
        shift.category = self.get_category_by_id(shift.category_id)

    def _add_emp_to_timeoff(self, timeoff: TimeOff):
        timeoff.employee = self.get_employee_by_id(timeoff.w2w_employee_id)

    def get_employee_by_id(self, w2w_employee_id: int) -> Union[Employee, None]:
        for employee in self.employees:
            if w2w_employee_id == employee.w2w_employee_id:
                return employee
        return None

    def get_position_by_id(self, position_id: int) -> Union[Position, None]:
        for position in self.positions:
            if position_id == position.position_id:
                return position
        return None

    def get_category_by_id(self, category_id: int) -> Union[Category, None]:
        for category in self.categories:
            if category_id == category.category_id:
                return category
        return None

    def get_shifts_by_date(self, start_date: date, end_date: date) -> List[Shift]:
        shifts = self._adapter.get_from_endpoint('AssignedShiftList', start_date, end_date)
        for shift in shifts:
            self._add_emp_pos_cat_to_shift(shift)
        return shifts

    def get_timeoff_by_date(self, start_date: date, end_date: date) -> List[TimeOff]:
        timeoff_requests = self._adapter.get_from_endpoint('ApprovedTimeOff', start_date, end_date)
        for request in timeoff_requests:
            self._add_emp_to_timeoff(request)
        return timeoff_requests
