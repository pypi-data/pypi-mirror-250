from django.shortcuts import render
from .models import Selinux, SElinuxEvent, SetroubleshootEntry
from rest_framework import viewsets
from .models import SElinuxEvent
from .serializers import SElinuxEventSerializer, SelinuxDataSerializer


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
import pprint
from .models import Selinux, SElinuxEvent


def selinux_list(request):
    selinux_entries = Selinux.objects.all()
    return render(request, 'selinux_list.html', {'selinux_entries': selinux_entries})


def SetroubleshootEntry_list(request):
    events = SetroubleshootEntry.objects
    return render(request, 'SetroubleshootEntry_list.html', {'events': events})

def SetroubleshootEntry_host(request, hostname):
    entries = SetroubleshootEntry.objects.filter(hostname=hostname).order_by('realtime_timestamp')
    context = {'entries': entries, 'hostname': hostname}
    return render(request, 'SetroubleshootEntry_list.html', context)


@method_decorator(csrf_exempt, name='dispatch')
class UploadSelinuxDataView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))

            # Assuming 'hostname' is a unique key
            hostname = data.get('hostname')

            selinux_instance, created = Selinux.objects.update_or_create(
                hostname=hostname,
                defaults=data
            )

            if created:
                return JsonResponse({'message': f'Data for {hostname} created successfully.'}, status=201)
            else:
                return JsonResponse({'message': f'Data for {hostname} updated successfully.'}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)
    
def selinux_event_list(request):
    selinux_event_entries = SElinuxEvent.objects.all()
    pprint.pprint(selinux_event_entries)

    return render(request, 'selinux_event_list.html', {'selinux_event_entries': selinux_event_entries})


@method_decorator(csrf_exempt, name='dispatch')
class UploadSElinuxEventView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            digest = data.get('digest')

            SElinuxEvent_instance, created = SElinuxEvent.objects.update_or_create(
                defaults=data
            )

            if created:
                return JsonResponse({'message': f'Data for {digest} created successfully.'}, status=201)
            else:
                return JsonResponse({'message': f'Data for {digest} updated successfully.'}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)
        

@method_decorator(csrf_exempt, name='dispatch')
class SetroubleshootEntryView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            cursor = data.get('cursor')

            SetroubleshootEntry_instance, created = SetroubleshootEntry.objects.update_or_create(
                defaults=data
            )

            if created:
                return JsonResponse({'message': f'Data for {cursor} created successfully.'}, status=201)
            else:
                return JsonResponse({'message': f'Data for {cursor} updated successfully.'}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)
        