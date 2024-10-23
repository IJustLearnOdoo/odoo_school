from odoo.tests.common import TransactionCase
from datetime import date


class TestPatient(TransactionCase):

    def test_compute_age(self):
        # Create a patient with a birthday
        patient = self.env['hr_hospital.patient'].create({
            'name': 'John Doe',
            'birthday': '2000-01-01'
        })

        # Manually compute age
        patient._compute_age()

        # Check if age is correctly computed
        today = date.today()
        expected_age = today.year - 2000
        if (today.month, today.day) < (1, 1):
            expected_age -= 1
        self.assertEqual(patient.age, expected_age)

    def test_update_all_ages(self):
        # Create patients with different birthdays
        self.env['hr_hospital.patient'].create(
            {'name': 'Alice', 'birthday': '1990-05-15'})
        self.env['hr_hospital.patient'].create(
            {'name': 'Bob', 'birthday': '1985-12-22'})

        # Update all ages
        self.env['hr_hospital.patient']._update_all_ages()

        # Fetch updated patients
        patients = self.env['hr_hospital.patient'].search([])

        # Assert that the ages were computed
        for patient in patients:
            self.assertGreater(patient.age, 0)

        def test_action_view_visits(self):
            # Create a patient
            patient = self.env['hr_hospital.patient'].create({
                'name': 'Jane Doe',
                'birthday': '1992-02-02'
            })

            # Call action_view_visits method
            action = patient.action_view_visits()

            # Assert correct action dict is returned
            self.assertEqual(action['res_model'], 'hr_hospital.visit')
            self.assertEqual(action['domain'],
                             [('patient_id', '=', patient.id)])
            self.assertEqual(action['type'], 'ir.actions.act_window')