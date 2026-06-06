from django.db import models
import uuid
import random
import string


# =========================
# STAFF MODEL
# =========================

class Staff(models.Model):

    name = models.CharField(max_length=100)

    dob = models.DateField()

    email = models.EmailField(unique=True)

    staff_id = models.CharField(
        max_length=12,
        unique=True,
        editable=False
    )

    password = models.CharField(
        max_length=20,
        editable=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def generate_password(self):
        return ''.join(
            random.choices(string.digits, k=6)
        )

    def save(self, *args, **kwargs):

        if not self.staff_id:

            unique_id = uuid.uuid4().hex[:8].upper()

            self.staff_id = f"STF-{unique_id}"

        if not self.password:

            self.password = self.generate_password()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# =========================
# CURRENT ELECTION MODEL
# =========================

class ElectionLocation(models.Model):

    location = models.CharField(
        max_length=100,
        unique=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.location


# =========================
# PEOPLE MODEL
# =========================

class People(models.Model):

    first_name = models.CharField(max_length=50)

    last_name = models.CharField(max_length=50)

    mobile = models.CharField(
        max_length=10,
        unique=True
    )

    gender = models.CharField(
        max_length=10
    )

    marital_status = models.CharField(
        max_length=10,
        default="Single"
    )

    address = models.TextField()

    aadhaar = models.CharField(
        max_length=8,
        unique=True
    )

    photo = models.ImageField(
        upload_to="people_photos/",
        null=True,
        blank=True
    )

    location = models.ForeignKey(
        "ElectionLocation",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.first_name

# =========================
# CANDIDATE MODEL (NEW)
# =========================

class Candidate(models.Model):

    name = models.CharField(
        max_length=100
    )

    party = models.CharField(
        max_length=100
    )

    logo = models.ImageField(
        upload_to="candidate_logos/"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name
    

class ElectionSettings(models.Model):

    location = models.ForeignKey(
        "ElectionLocation",
        on_delete=models.CASCADE
    )

    election_date = models.DateField()

    start_time = models.TimeField()

    end_time = models.TimeField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return str(self.location)
    
class Vote(models.Model):

    person = models.ForeignKey(
        "People",
        on_delete=models.CASCADE
    )

    candidate = models.ForeignKey(
        "Candidate",
        on_delete=models.CASCADE
    )

    location = models.ForeignKey(
        "ElectionLocation",
        on_delete=models.CASCADE
    )

    voted_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        unique_together = ["person"]



# =========================
# ELECTION MODEL (ADD THIS)
# =========================

class Election(models.Model):

    title = models.CharField(max_length=200)

    description = models.TextField(blank=True)

    start_time = models.DateTimeField()

    end_time = models.DateTimeField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title


# =========================
# ELECTION CANDIDATE MODEL
# =========================

class ElectionCandidate(models.Model):

    election = models.ForeignKey(
        Election,
        related_name="candidates",
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=100)

    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    

class OTP(models.Model):

    mobile = models.CharField(
        max_length=10
    )

    otp = models.CharField(
        max_length=6
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.mobile
    

class Vote(models.Model):

    person = models.ForeignKey(
        "People",
        on_delete=models.CASCADE
    )

    candidate = models.ForeignKey(
        "Candidate",
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.person.first_name} voted for {self.candidate.name}"