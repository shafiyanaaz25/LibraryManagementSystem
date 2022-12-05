from rest_framework.test import APITestCase
from rest_framework import status

from library_management.helper import create_students


class StudentTestCase(APITestCase):

    def test_add_student(self):
        data = {
            "roll_number": 1,
            "name": "abc",
            "email": "abc@gmail.com",
            "department": "CSE"
        }
        response = self.client.post("/library_management/add_student/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_view_all_students(self):
        create_students()
        response = self.client.get("/library_management/view_all_students/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]["roll_number"], '1')

    def test_delete_student(self):
        create_students()
        response = self.client.get("/library_management/view_all_students/")
        self.assertEqual(len(response.data), 3)
        student_id = 1
        response = self.client.delete(f"/library_management/delete_student/{student_id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get("/library_management/view_all_students/")
        self.assertEqual(len(response.data), 2)

    def test_update_student_details(self):
        create_students()
        student_id = 1
        response = self.client.get(f"/library_management/student_by_id/{student_id}")
        # assert response.data['name'] == "abc"
        self.assertEqual(response.data["name"], "abc")
        data = {
            "id": student_id,
            "roll_number": "1",
            "name": "S Naaz",
            "email": "snaaz@gmail.com",
            "department": "CSE"
        }
        response = self.client.put(f"/library_management/update_student_details/{student_id}", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(f"/library_management/student_by_id/{student_id}")
        # assert response.data['name'] == "S Naaz"
        self.assertEqual(response.data["name"], "S Naaz")
