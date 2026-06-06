from django.urls import path
from .views import (
    send_otp,
    verify_otp,
    cast_vote,
    save_results,
    clear_results
)

from .views import (
    register_staff,
    get_staff,
    delete_staff,
    add_location,
    get_locations,
    delete_location,
    register_people,
    get_people,
    delete_people,
    update_people,
    add_candidate,
    get_candidates,
    delete_candidate,
    staff_login,

    set_election, get_elections,
    verify_voter,
     verify_user,
    submit_vote,
    dashboard_stats,
    election_results,
    delete_election,
    update_election,
    
)

urlpatterns = [

    path("register-staff/", register_staff),

    path("staff-list/", get_staff),

    path("delete-staff/<int:id>/", delete_staff),

    path("add-location/", add_location),

    path("get-locations/", get_locations),

    path("delete-location/<int:id>/", delete_location),

    path("register-people/", register_people),

    path("people-list/", get_people),

    path("delete-people/<int:id>/", delete_people),

    path("update-people/<int:id>/", update_people),

    path("add-candidate/", add_candidate),

    path("get-candidates/", get_candidates),

    path("delete-candidate/<int:id>/", delete_candidate),
    

    # ✅ ADD THIS

    path("staff-login/", staff_login),

    path("set-election/", set_election),

    path("get-elections/", get_elections),

    path(
        "verify-voter/",
        verify_voter
    ),

    path(
        "submit-vote/",
        submit_vote
    ),

    path(
        "dashboard-stats/",
        dashboard_stats
    ),

    path(
        "results/",
        election_results
    ),

       # NEW USER PROFILE VERIFY
    path(
        "verify-user/<str:aadhaar>/",
        verify_user
    ),


path("delete-election/<int:id>/", delete_election),
path("update-election/<int:id>/", update_election),
path("send-otp/", send_otp),
path("verify-otp/", verify_otp),
path("cast-vote/", cast_vote),
path("results/", election_results),
path("save-results/", save_results),
path("clear-results/", clear_results),

]