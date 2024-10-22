from datetime import datetime, timedelta
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestHospital(TransactionCase):
    def setUp(self):
        super(TestHospital, self).setUp()

        # Create test users
        self.patient_user = self.env['res.users'].create({
            'name': 'Test Patient',
            'login': 'test_patient',
            'groups_id': [
                (4, self.env.ref('hr_hospital.group_hospital_patient').id)]
        })

        self.doctor_user = self.env['res.users'].create({
            'name': 'Test Doctor',
            'login': 'test_doctor',
            'groups_id': [
                (4, self.env.ref('hr_hospital.group_hospital_doctor').id)]
        })

        # Create test records
        self.doctor = self.env['hr_hospital.doctor'].create({
            'name': 'Dr. House',
            'specialization': 'therapist',
            'user_id': self.doctor_user.id,
        })

        self.patient = self.env['hr_hospital.patient'].create({
            'name': 'John Doe',
            'birthday': '1990-01-01',
            'doctor_id': self.doctor.id,
            'user_id': self.patient_user.id,
        })

        self.disease = self.env['hr_hospital.disease'].create({
            'name': 'Test Disease',
            'description': 'Test Description',
        })

    def test_patient_age_computation(self):
        """Test the age computation of patients"""
        self.patient.birthday = datetime.now().date() - timedelta(
            days=365 * 25)
        self.patient._compute_age()
        self.assertEqual(self.patient.age, 25)

    def test_visit_duplicate_constraint(self):
        """Test the constraint preventing duplicate visits"""
        visit_date = datetime.now()

        # Create first visit
        self.env['hr_hospital.visit'].create({
            'patient_id': self.patient.id,
            'doctor_id': self.doctor.id,
            'scheduled_date': visit_date,
        })

        # Try to create duplicate visit
        with self.assertRaises(ValidationError):
            self.env['hr_hospital.visit'].create({
                'patient_id': self.patient.id,
                'doctor_id': self.doctor.id,
                'scheduled_date': visit_date,
            })

    def test_diagnosis_approval_workflow(self):
        """Test the diagnosis approval workflow"""
        # Create intern doctor
        intern_doctor = self.env['hr_hospital.doctor'].create({
            'name': 'Dr. Intern',
            'specialization': 'therapist',
            'is_intern': True,
            'mentor_id': self.doctor.id,
        })

        # Create visit
        visit = self.env['hr_hospital.visit'].create({
            'patient_id': self.patient.id,
            'doctor_id': intern_doctor.id,
            'scheduled_date': datetime.now(),
        })

        # Create diagnosis as intern
        diagnosis = self.env['hr_hospital.diagnosis'].with_user(
            intern_doctor.user_id).create({
                'visit_id': visit.id,
                'disease_id': self.disease.id,
                'description': 'Test diagnosis',
            })

        self.assertFalse(
            diagnosis.is_approved,
            "Intern's diagnosis should not be auto-approved"
        )

        # Approve diagnosis as mentor
        diagnosis.with_user(self.doctor_user).write({'is_approved': True})
        self.assertTrue(
            diagnosis.is_approved,
            "Mentor should be able to approve diagnosis"
        )
