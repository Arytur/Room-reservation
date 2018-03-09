from django.shortcuts import render, redirect
from rooms.models import *
from datetime import datetime


today = datetime.today().strftime('%Y-%m-%d')


def show_room(request):
    rooms = Rooms.objects.all().order_by('id')
    status = dict()
    for room in rooms:
        if room.reservation_set.filter(reservation_date=today):
            status[room.id] = 'Zajęta'
        else:
            status[room.id] = 'Wolna'
    context = {
        'rooms': rooms,
        'status': status
    }
    return render(request, "show_room.html", context=context)


def show_detail(request, id):
    room = Rooms.objects.filter(id=id)
    reserv = Reservation.objects.filter(room_id=id, reservation_date__gte=today)
    context = {
        'room': room,
        'reserv': reserv,
    }
    return render(request, "details_room.html", context=context)


def modify_room(request, id):
    room = Rooms.objects.filter(id=id)
    if request.method == 'GET':
        context = {
            'room': room
        }
        return render(request, "modify_room.html", context=context)
    elif request.method == 'POST':
        name = request.POST.get('name')
        capacity = request.POST.get('capacity')
        projector = True if request.POST.get('proj') else False
        more = request.POST.get('more')
        room.update(name=name, capacity=capacity, projector=projector, more=more)
        return redirect('/')


def add_room(request):
    if request.method == 'GET':
        return render(request, "add_room.html")
    elif request.method == 'POST':
        name = request.POST.get('name')
        capacity = request.POST.get('capacity')
        projector = True if request.POST.get('proj') else False
        more = request.POST.get('more')
        new_room = Rooms.objects.create(name=name, capacity=capacity, projector=projector, more=more)
        new_room.save()
        return redirect('/')


def delete_room(request, id):
    room = Rooms.objects.filter(id=id)
    if request.method == 'GET':
        context = {
            'room': room
        }
        return render(request, "delete_room.html", context=context)
    elif request.method == 'POST':
        room.delete()
        return redirect('/')


def room_reservation(request, id):
    room = Rooms.objects.filter(id=id)
    if request.method == 'GET':
        context = {
            'room': room,
            'today': today,
        }
        return render(request, "reservation_room.html", context=context)
    elif request.method == 'POST':
        room = Rooms.objects.get(id=id)
        date = request.POST.get('res_date')
        comment = request.POST.get('comment')
        if room.reservation_set.filter(reservation_date=date):
            message = "Sala zajęta w ten dzień"
            return render(request, 'reservation_room.html', {'message': message})
        new_reservation = Reservation.objects.create(reservation_date=date, comment=comment)
        new_reservation.save()
        new_reservation.room_id.add(id)
        return redirect('/')


def room_search(request):
    name = request.GET.get('name', False)
    date = request.GET.get('date', False)
    capacity = request.GET.get('capacity', False)
    projector = request.GET.get('projector', False)

    result = {'name': [], 'date': [], 'capacity': [], 'projector': []}

    if name:
        room_name = Rooms.objects.filter(name__icontains=name).values_list('id', flat=True)
        result['name'] = list(room_name)
    else:
        room_name = Rooms.objects.all().values_list('id', flat=True)
        result['name'] = list(room_name)

    if date:
        room_date = Rooms.objects.exclude(reservation__reservation_date__exact=date).values_list('id', flat=True)
        result['date'] = list(set(room_date))
    else:
        room_date = Rooms.objects.all().values_list('id', flat=True)
        result['date'] = list(set(room_date))

    if capacity:
        room_cap = Rooms.objects.filter(capacity__gte=capacity).values_list('id', flat=True)
        result['capacity'] = list(room_cap)
    else:
        room_cap = Rooms.objects.all().values_list('id', flat=True)
        result['capacity'] = list(room_cap)

    if projector:
        room_proj = Rooms.objects.filter(projector=True).values_list('id', flat=True)
        result['projector'] = list(room_proj)
    else:
        room_proj = Rooms.objects.all().values_list('id', flat=True)
        result['projector'] = list(room_proj)

    counter = sum(result.values(), [])
    rooms_id = list(Rooms.objects.all().values_list('id', flat=True))

    list_result = []
    for id in rooms_id:
        if counter.count(id) == 4:
            list_result.append(list(Rooms.objects.filter(id=id)))

    context = {
        'list_result': list_result,
        'name': name,
        'date': date,
        'capacity': capacity,
        'projector': projector
    }

    return render(request, "search.html", context=context)






