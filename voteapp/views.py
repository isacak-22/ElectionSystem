from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count
from .models import Election, ElectionCandidate
from .models import OTP
import random
from datetime import timedelta
from django.utils import timezone
from rest_framework.decorators import api_view
from datetime import datetime

from .serializers import (
    StaffSerializer,
    ElectionLocationSerializer,
    PeopleSerializer,
    CandidateSerializer,
    ElectionSettingsSerializer
)

from .models import (
    Staff,
    ElectionLocation,
    People,
    Candidate,
    ElectionSettings,
    Vote
)

# =========================
# STAFF
# =========================

@api_view(["POST"])
def register_staff(request):

    serializer = StaffSerializer(data=request.data)

    if serializer.is_valid():

        staff = serializer.save()

        return Response({
            "message": "Staff registered successfully",
            "staff_id": staff.staff_id,
            "password": staff.password
        })

    return Response(serializer.errors)


@api_view(["GET"])
def get_staff(request):

    staff = Staff.objects.all().order_by("-id")

    serializer = StaffSerializer(
        staff,
        many=True
    )

    return Response(serializer.data)


@api_view(["DELETE"])
def delete_staff(request, id):

    try:

        staff = Staff.objects.get(id=id)

        staff.delete()

        return Response({
            "message": "Staff deleted successfully"
        })

    except Staff.DoesNotExist:

        return Response({
            "error": "Staff not found"
        })


# =========================
# LOCATION
# =========================

@api_view(["POST"])
def add_location(request):

    serializer = ElectionLocationSerializer(
        data=request.data
    )

    if serializer.is_valid():

        serializer.save()

        return Response({
            "message": "Location added successfully"
        })

    return Response(serializer.errors)


@api_view(["GET"])
def get_locations(request):

    locations = ElectionLocation.objects.all()

    serializer = ElectionLocationSerializer(
        locations,
        many=True
    )

    return Response(serializer.data)


@api_view(["DELETE"])
def delete_location(request, id):

    location = ElectionLocation.objects.get(id=id)

    location.delete()

    return Response({
        "message": "Location deleted"
    })


# =========================
# PEOPLE
# =========================

@api_view(["POST"])
def register_people(request):

    serializer = PeopleSerializer(
        data=request.data
    )

    if serializer.is_valid():

        serializer.save()

        return Response({
            "message": "People registered"
        })

    return Response(serializer.errors)


@api_view(["GET"])
def get_people(request):

    people = People.objects.all()

    serializer = PeopleSerializer(
        people,
        many=True
    )

    return Response(serializer.data)


@api_view(["DELETE"])
def delete_people(request, id):

    person = People.objects.get(id=id)

    person.delete()

    return Response({
        "message": "Person deleted"
    })


@api_view(["PUT"])
def update_people(request, id):

    person = People.objects.get(id=id)

    serializer = PeopleSerializer(
        person,
        data=request.data
    )

    if serializer.is_valid():

        serializer.save()

        return Response({
            "message": "Updated"
        })

    return Response(serializer.errors)


# =========================
# CANDIDATE
# =========================

@api_view(["POST"])
def add_candidate(request):

    serializer = CandidateSerializer(
        data=request.data
    )

    if serializer.is_valid():

        serializer.save()

        return Response({
            "message": "Candidate added"
        })

    return Response(serializer.errors)


@api_view(["GET"])
def get_candidates(request):

    candidates = Candidate.objects.all()

    serializer = CandidateSerializer(
        candidates,
        many=True
    )

    return Response(serializer.data)


@api_view(["DELETE"])
def delete_candidate(request, id):

    candidate = Candidate.objects.get(id=id)

    candidate.delete()

    return Response({
        "message": "Candidate deleted"
    })


# =========================
# STAFF LOGIN
# =========================

@api_view(["POST"])
def staff_login(request):

    staff_id = request.data.get("staff_id")
    password = request.data.get("password")

    try:

        Staff.objects.get(
            staff_id=staff_id,
            password=password
        )

        return Response({
            "success": True,
            "message": "Login successful"
        })

    except Staff.DoesNotExist:

        return Response({
            "success": False,
            "message": "Invalid ID or Password"
        })


# =========================
# ELECTION SETTINGS
# =========================

@api_view(["POST"])
def set_election_settings(request):

    serializer = ElectionSettingsSerializer(
        data=request.data
    )

    if serializer.is_valid():

        serializer.save()

        return Response({
            "message":
            "Election settings saved"
        })

    return Response(serializer.errors)


@api_view(["GET"])
def get_election_settings(request):

    settings = (
        ElectionSettings.objects
        .select_related("location")
        .all()
        .order_by("-id")
    )

    data = []

    for s in settings:
        data.append({
            "id": s.id,
            "location": (
                s.location.location
                if s.location else ""
            ),
            "election_date": s.election_date,
            "start_time": s.start_time,
            "end_time": s.end_time,
        })

    return Response(data)



@api_view(["POST"])
def set_election_settings(request):

    serializer = ElectionSettingsSerializer(
        data=request.data
    )

    if serializer.is_valid():

        serializer.save()

        return Response({
            "message": "Election created successfully"
        })

    return Response(
        serializer.errors,
        status=400
    )


# =========================
# VERIFY USER PROFILE (NEW)
# =========================

@api_view(["GET"])
def verify_user(request, aadhaar):

    try:

        person = People.objects.get(
            aadhaar=aadhaar
        )

        serializer = PeopleSerializer(
            person,
            context={"request": request}
        )

        return Response(serializer.data)

    except People.DoesNotExist:

        return Response(
            {"error": "User not found"},
            status=404
        )

# =========================
# VERIFY VOTER
# =========================

@api_view(["POST"])
def verify_voter(request):

    aadhaar = request.data.get("aadhaar")

    try:

        person = People.objects.get(
            aadhaar=aadhaar
        )

        already_voted = Vote.objects.filter(
            person=person
        ).exists()

        if already_voted:

            return Response({
                "allowed": False,
                "message": "Already voted"
            })

        return Response({
            "allowed": True,
            "person_id": person.id
        })

    except People.DoesNotExist:

        return Response({
            "allowed": False,
            "message": "Invalid Aadhaar"
        })


# =========================
# SUBMIT VOTE
# =========================

@api_view(["POST"])
def submit_vote(request):

    person_id = request.data.get("person")
    candidate_id = request.data.get("candidate")
    location_id = request.data.get("location")

    try:

        person = People.objects.get(id=person_id)

        candidate = Candidate.objects.get(id=candidate_id)

        Vote.objects.create(

            person=person,
            candidate=candidate,
            location_id=location_id

        )

        return Response({
            "message":
            "Vote submitted successfully"
        })

    except Exception as e:

        print("VOTE ERROR:", e)

        return Response({
            "message":
            "Error submitting vote"
        })


# =========================
# DASHBOARD STATS
# =========================

@api_view(["GET"])
def dashboard_stats(request):

    return Response({

        "total_staff":
        Staff.objects.count(),

        "total_people":
        People.objects.count(),

        "total_candidates":
        Candidate.objects.count(),

        "total_locations":
        ElectionLocation.objects.count(),

        "total_votes":
        Vote.objects.count()

    })


# =========================
# RESULTS
# =========================

@api_view(["GET"])
def get_elections(request):
    elections = Election.objects.prefetch_related("candidates").all()

    data = []

    for election in elections:
        data.append({
            "id": election.id,
            "title": election.title,
            "description": election.description,
            "start_time": election.start_time.strftime("%Y-%m-%d %H:%M"),
            "end_time": election.end_time.strftime("%Y-%m-%d %H:%M"),
            "candidates": [
                {
                    "name": c.name,
                    "description": c.description
                }
                for c in election.candidates.all()
            ]
        })

    return Response(data)

@api_view(["POST"])
def set_election(request):
    try:
        title = request.data.get("title")
        description = request.data.get("description")
        start_time = request.data.get("start_time")
        end_time = request.data.get("end_time")
        candidates = request.data.get("candidates", [])

        # ✅ FIX: convert datetime
        start_time = datetime.fromisoformat(start_time)
        end_time = datetime.fromisoformat(end_time)

        election = Election.objects.create(
            title=title,
            description=description,
            start_time=start_time,
            end_time=end_time,
        )

        for c in candidates:
            ElectionCandidate.objects.create(
                election=election,
                name=c.get("name"),
                description=c.get("description", "")
            )

        return Response({
            "message": "Election created successfully"
        })

    except Exception as e:
        print("CREATE ERROR:", e)
        return Response({"error": str(e)}, status=400)
    
@api_view(["GET"])
def election_results(request):

    results = (
        Vote.objects
        .values("candidate__name")
        .annotate(total_votes=Count("id"))
        .order_by("-total_votes")
    )

    return Response(results)



@api_view(["POST"])
def submit_vote(request):

    person_id = request.data.get("person")
    candidate_id = request.data.get("candidate")
    location_id = request.data.get("location")

    try:

        person = People.objects.get(id=person_id)

        # CHECK DUPLICATE VOTE
        already_voted = Vote.objects.filter(
            person=person
        ).exists()

        if already_voted:

            return Response({
                "success": False,
                "message": "Already voted"
            })

        candidate = Candidate.objects.get(
            id=candidate_id
        )

        Vote.objects.create(
            person=person,
            candidate=candidate,
            location_id=location_id
        )

        return Response({
            "success": True,
            "message": "Vote submitted successfully"
        })

    except Exception as e:

        print("VOTE ERROR:", e)

        return Response({
            "success": False,
            "message": "Error submitting vote"
        })
    

# =========================
# SEND OTP
# =========================

@api_view(["POST"])
def send_otp(request):

    mobile = request.data.get("mobile")

    if not mobile:
        return Response({
            "error": "Mobile number required"
        }, status=400)

    otp_code = str(
        random.randint(100000, 999999)
    )

    OTP.objects.create(
        mobile=mobile,
        otp=otp_code
    )

    print("OTP:", otp_code)

    return Response({
        "message": "OTP sent successfully"
    })


# =========================
# VERIFY OTP
# =========================

@api_view(["POST"])
def verify_otp(request):

    mobile = request.data.get("mobile")
    otp = request.data.get("otp")

    if not mobile or not otp:
        return Response({
            "verified": False,
            "message": "Mobile and OTP required"
        })

    try:

        latest_otp = OTP.objects.filter(
            mobile=mobile
        ).latest("created_at")

        if timezone.now() - latest_otp.created_at > timedelta(minutes=5):

            return Response({
                "verified": False,
                "message": "OTP expired"
            })

        if str(latest_otp.otp).strip() == str(otp).strip():

            return Response({
                "verified": True,
                "message": "OTP verified successfully"
            })

        return Response({
            "verified": False,
            "message": "Invalid OTP"
        })

    except OTP.DoesNotExist:

        return Response({
            "verified": False,
            "message": "OTP not found"
        })

    except OTP.DoesNotExist:

        return Response({
            "verified": False,
            "message": "OTP not found"
        })


@api_view(["DELETE"])
def delete_election(request, id):
    try:
        election = Election.objects.get(id=id)
        election.delete()

        return Response({
            "message": "Election deleted successfully"
        })

    except Election.DoesNotExist:
        return Response({
            "error": "Election not found"
        }, status=404)
    

@api_view(["PUT"])
def update_election(request, id):
    try:
        election = Election.objects.get(id=id)

        election.title = request.data.get("title")
        election.description = request.data.get("description")
        election.start_time = request.data.get("start_time")
        election.end_time = request.data.get("end_time")
        election.save()

        # DELETE OLD CANDIDATES
        election.candidates.all().delete()

        # ADD NEW
        candidates = request.data.get("candidates", [])
        for c in candidates:
            ElectionCandidate.objects.create(
                election=election,
                name=c.get("name"),
                description=c.get("description", "")
            )

        return Response({
            "message": "Election updated successfully"
        })

    except Election.DoesNotExist:
        return Response({"error": "Not found"}, status=404)
    


@api_view(["POST"])
def cast_vote(request):
    person_id = request.data.get("person_id")
    candidate_id = request.data.get("candidate_id")

    try:
        person = People.objects.get(id=person_id)

        # ❗ Prevent double voting
        if Vote.objects.filter(person=person).exists():
            return Response({"error": "Already voted"}, status=400)

        candidate = Candidate.objects.get(id=candidate_id)

        Vote.objects.create(
            person=person,
            candidate=candidate
        )

        return Response({"message": "Vote cast successfully ✅"})

    except Exception as e:
        return Response({"error": str(e)}, status=400)
    


# =========================
# SAVE RESULTS
# =========================
@api_view(["POST"])
def save_results(request):
    return Response({
        "message": "Results saved successfully"
    })


# =========================
# CLEAR RESULTS
# =========================
@api_view(["DELETE"])
def clear_results(request):
    Vote.objects.all().delete()

    return Response({
        "message": "Results cleared successfully"
    })