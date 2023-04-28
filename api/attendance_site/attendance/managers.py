from django.db import models

class SubjectManager(models.Manager):
    def update_or_create_subject(self, subject_data):
        subject, created = self.update_or_create(
            subject_id=subject_data['subject_id'],
            group_id=subject_data['group_id'],
            teacher_id=subject_data['teacher_id'],
            subject_name=subject_data['subject_name']
        )
        return subject, created