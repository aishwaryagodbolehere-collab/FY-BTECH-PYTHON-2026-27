from django.db import models


class Student(models.Model):
    BRANCH_CHOICES = [
        ('AI & Data Science', 'AI & Data Science'),
        ('Computer Science & Engineering', 'Computer Science & Engineering'),
        ('Information Technology', 'Information Technology'),
        ('Mechanical Engineering', 'Mechanical Engineering'),
        ('Electronics & Telecom', 'Electronics & Telecom'),
    ]

    full_name = models.CharField(max_length=255)
    branch = models.CharField(max_length=100, choices=BRANCH_CHOICES)
    cgpa = models.DecimalField(max_digits=4, decimal_places=2, default=9.12)
    graduation_year = models.IntegerField(default=2030)
    skills = models.TextField(default="Python, Django, SQL, Machine Learning")
    github_link = models.URLField(blank=True, null=True)
    resume_link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.branch} ({self.cgpa})"


class StudentProfile(models.Model):
    full_name = models.CharField(max_length=255, default="New Student")
    email = models.EmailField(max_length=255, default="student@mitwpu.edu.in")
    password = models.CharField(max_length=128, blank=True, null=True)
    security_pin = models.CharField(max_length=10, blank=True, null=True)
    firebase_uid = models.CharField(max_length=128, blank=True, null=True, help_text="Google Auth or Password UID")
    prn = models.CharField(max_length=25, unique=True, help_text="Permanent Registration Number")
    branch = models.CharField(max_length=100, default="AI & Data Science")
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    graduation_year = models.CharField(max_length=10, blank=True, null=True, default="2030")
    class_of = models.CharField(max_length=10, blank=True, null=True)
    current_year_study = models.CharField(max_length=50, blank=True, null=True)
    preferred_location = models.CharField(max_length=150, blank=True, null=True)
    interested_roles = models.CharField(max_length=250, blank=True, null=True)
    bio = models.TextField(max_length=5000, blank=True, null=True)
    cgpa = models.DecimalField(max_digits=4, decimal_places=2, default=9.12)
    skills = models.TextField(blank=True, null=True, help_text="Comma separated skills")
    github_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    open_to_internships = models.BooleanField(default=True)
    profile_picture = models.TextField(blank=True, null=True, help_text="Cropped Base64 profile picture")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.prn})"


class RecruiterProfile(models.Model):
    firebase_uid = models.CharField(max_length=128, blank=True, null=True, db_index=True)
    username = models.CharField(max_length=150, blank=True, null=True)
    password = models.CharField(max_length=128, blank=True, null=True)
    security_pin = models.CharField(max_length=10, blank=True, null=True)
    full_name = models.CharField(max_length=255)
    work_email = models.EmailField(unique=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    company_name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    linkedin_url = models.URLField(blank=True, null=True)
    profile_picture = models.TextField(blank=True, null=True, help_text="Cropped Base64 profile picture")
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} - {self.company_name}"


class ChatConnection(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Request'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ]
    student_prn = models.CharField(max_length=25, db_index=True)
    student_name = models.CharField(max_length=255, default="Student")
    recruiter_email = models.EmailField(db_index=True)
    recruiter_name = models.CharField(max_length=255, default="Recruiter")
    company_name = models.CharField(max_length=255, default="Company")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    blocked_by_student = models.BooleanField(default=False)
    blocked_by_recruiter = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student_prn', 'recruiter_email')

    def __str__(self):
        return f"{self.recruiter_name} ({self.company_name}) -> {self.student_name} [{self.status}]"


class EncryptedMessage(models.Model):
    connection = models.ForeignKey(ChatConnection, on_delete=models.CASCADE, related_name='messages')
    sender_role = models.CharField(max_length=20)  # 'recruiter' or 'student'
    sender_name = models.CharField(max_length=255)
    msg_type = models.CharField(max_length=20, default='text')  # 'text' or 'audio'
    ciphertext = models.TextField(help_text="End-to-End Encrypted Ciphertext")
    audio_data = models.TextField(blank=True, null=True, help_text="Base64 encoded voice note")
    is_edited = models.BooleanField(default=False)
    visible_to_sender_only = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"E2EE {self.msg_type} by {self.sender_name} at {self.created_at:%H:%M}"

class VerificationCode(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=6)
    purpose = models.CharField(max_length=20)  # 'pin' or 'password'
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} ({self.purpose}) - {self.code}"


class UserFeedback(models.Model):
    user_name = models.CharField(max_length=120, blank=True, default='Anonymous')
    user_email = models.EmailField(blank=True, default='')
    user_role = models.CharField(max_length=20, default='student')
    rating = models.IntegerField(default=5)
    message = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rating}★ - {self.user_name} ({self.user_email})"