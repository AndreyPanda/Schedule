# from datetime import datetime
# from main.models import Doctor, Visit, Client
# from main.views import FillInTheClientData
#
#
# def test_you_can_book_this_time(create_specs_and_doctors_and_clients):
#     visit_datetime = datetime(2095,5,5,15,0)
#     new_visit = Visit(
#         visit_datetime=visit_datetime,
#         doctor_to_visit=Doctor.objects.last(),
#         client_visiting=Client.objects.last(),
#     )
#     new_visit.save()
#     assert Visit.objects.count() == 1
#     assert Visit.objects.last().doctor_to_visit == Doctor.objects.last()


# # Этот тест не работает, надо доделывать
# def test_this_time_is_already_booked(create_specs_and_doctors_and_clients):
#     visit_datetime = datetime(2095,5,5,15,0)
#     new_visit = Visit(
#         visit_datetime=visit_datetime,
#         doctor_to_visit=Doctor.objects.last(),
#         client_visiting=Client.objects.last(),
#     )
#     new_visit.save()
#     assert Visit.objects.count() == 1
#     assert Visit.objects.last().doctor_to_visit == Doctor.objects.last()
#
#     second_new_visit = FillInTheClientData(doctor_slug=Doctor.objects.last().slug, visit_string="209505051500")
#     print(f'--------------------second_new_visit = {second_new_visit}')
#     assert Visit.objects.count() == 2
#     assert Visit.objects.last().doctor_to_visit == Doctor.objects.last()


