import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Speciality, LocationDetails,Doctor
from django.shortcuts import get_object_or_404

@csrf_exempt
def create_location(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        # Check if the location already exists
        existing_locations = LocationDetails.objects.filter(
            location=data.get('location'),
            address=data.get('address'),
            state=data.get('state')
        )

        if existing_locations:
            response_data = {
                "message": "Location already exists."
            }
            return HttpResponse(json.dumps(response_data), content_type='application/json', status=409)

        # Create a new location if it doesn't exist
        new_location = LocationDetails.objects.create(
            location=data.get('location'),
            address=data.get('address'),
            email=data.get('email'),
            phone_number=data.get('phone_number'),
            pin_code=data.get('pin_code'),
            state=data.get('state')
        )

        response_data = {
            "id": new_location.id,
            "location": new_location.location,
            "address": new_location.address,
            "email": new_location.email,
            "phone_number": new_location.phone_number,
            "pin_code": new_location.pin_code,
            "state": new_location.state
        }

        return HttpResponse(json.dumps(response_data), content_type='application/json')

    else:
        return HttpResponse("Invalid request method.", status=405)



# this is for to get the selected location entire details 
def location_details(request, location_id):
    if request.method == 'GET':
        location = get_object_or_404(LocationDetails, id=location_id)
        
        data = {
            "id": location.id,
            "location": location.location,
            "address": location.address,
            "email": location.email,
            "phone_number": location.phone_number,
            "pin_code": location.pin_code,
            "state": location.state
        }
        
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponse("Invalid request method.", status=405)

    
# this is for whole location list
@csrf_exempt
def list_locations(request):
    if request.method == 'GET':
        locations = LocationDetails.objects.all()
        
        data = []
        for location in locations:
            data.append({
                "id": location.id,
                "location": location.location,
                "address": location.address,
                "email": location.email,
                "phone_number": location.phone_number,
                "pin_code": location.pin_code,
                "state": location.state
            })
        
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponse("Invalid request method.", status=405)

#only list of locations
@csrf_exempt
def locations(request):
    if request.method == 'GET':
        # Get all locations
        locations = LocationDetails.objects.all()
        
        # Use a set to collect unique states
        unique_states = set(location.state for location in locations)
        
        # Prepare the response data with unique states
        data = [state for state in unique_states]
        
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponse("Invalid request method.", status=405)

# states list 
@csrf_exempt
def locations_state(request, state_name=None):
    if request.method == 'GET':
        if state_name:
            # Filter locations by the provided state
            locations = LocationDetails.objects.filter(state=state_name)
        else:
            # If no state is provided, return all locations
            locations = LocationDetails.objects.all()
        
        # Prepare the response data with only location names
        data = [location.location for location in locations]
        
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponse("Invalid request method.", status=405)
    

@csrf_exempt
def update_location(request, location_id):
    if request.method == 'PUT':
        location = get_object_or_404(LocationDetails, id=location_id)
        data = json.loads(request.body)

        # Update fields if they exist in the request data
        location.location = data.get('location', location.location) 
        location.address = data.get('address', location.address)
        location.email = data.get('email', location.email)
        location.phone_number = data.get('phone_number', location.phone_number)
        location.pin_code = data.get('pin_code', location.pin_code)
        location.state = data.get('state', location.state)

        # Save the updated location
        location.save()

        response_data = {
            "id": location.id,
            "location": location.location,
            "address": location.address,
            "email": location.email,
            "phone_number": location.phone_number,
            "pin_code": location.pin_code,
            "state": location.state
        }

        return HttpResponse(json.dumps(response_data), content_type='application/json')

    else:
        return HttpResponse("Invalid request method.", status=405)



@csrf_exempt
def delete_location(request, location_id):
    if request.method == 'DELETE':
        location = get_object_or_404(LocationDetails, id=location_id)
        location.delete()
        response_data = {
            "message": f"Location with id={location_id} is deleted."
        }
        return HttpResponse(json.dumps(response_data), content_type='application/json')
    else:
        return HttpResponse("Invalid request method.", status=405)




@csrf_exempt
def create_speciality(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        location = get_object_or_404(LocationDetails, id=data.get('location_id'))

        speciality = Speciality.objects.create(name=data.get('name'),location=location)

        response_data = {
            "id": speciality.id,
            "name": speciality.name,
            "location": speciality.location.location
        }

        return HttpResponse(json.dumps(response_data), content_type='application/json')

    return HttpResponse("Invalid request method.", status=405)

 


def list_speciality(request):
    if request.method == 'GET':
        # Fetch all specialities
        specialities = Speciality.objects.all()

        # Prepare the list of specialities
        data = []
        for speciality in specialities:
            speciality_data = {
                "id": speciality.id,
                "name": speciality.name,
                "location": speciality.location.location
            }
            data.append(speciality_data)

        # Return the list as JSON
        return HttpResponse(json.dumps(data), content_type='application/json')

    return HttpResponse("Invalid request method.", status=405)

@csrf_exempt
def update_speciality(request, speciality_id):
    if request.method == 'PUT':
        data = json.loads(request.body)
        
        # Fetch the speciality to update
        speciality = get_object_or_404(Speciality, id=speciality_id)
        
        # Update the speciality name if provided
        if 'name' in data:
            speciality.name = data.get('name')
        
        # Update the location if location_id is provided
        if 'location_id' in data:
            location = get_object_or_404(LocationDetails, id=data.get('location_id'))
            speciality.location = location
        
        # Save the updated speciality
        speciality.save()
        
        response_data = {
            "id": speciality.id,
            "name": speciality.name,
            "location": speciality.location.location
        }

        return HttpResponse(json.dumps(response_data), content_type='application/json')
    
    return HttpResponse("Invalid request method.", status=405)
@csrf_exempt
def delete_speciality(request, speciality_id):
    if request.method == 'DELETE':
        # Fetch the speciality to delete
        speciality = get_object_or_404(Speciality, id=speciality_id)
        
        # Delete the speciality
        speciality.delete()
        
        return HttpResponse("Speciality deleted successfully.", status=204)
    
    return HttpResponse("Invalid request method.", status=405)




@csrf_exempt
def create_doctor(request):
    if request.method == 'POST':
        try:
            # Parse the JSON body
            data = json.loads(request.body)

            # Extract fields from the request body
            doctor_name = data.get('doctor_name')
            speciality_name = data.get('speciality_name')
            location_id = data.get('location_id')

            # Validate required fields
            if not doctor_name or not speciality_name or not location_id:
                return HttpResponse(
                    json.dumps({"error": "Missing required fields"}),
                    content_type='application/json',
                    status=400
                )

            # Retrieve the Speciality objects
            speciality_qs = Speciality.objects.filter(name=speciality_name)
            if not speciality_qs.exists():
                return HttpResponse(
                    json.dumps({"error": "Speciality not found"}),
                    content_type='application/json',
                    status=404
                )

            # Handle multiple specialties by picking the first one
            speciality = speciality_qs.first()

            # Create a new Doctor instance
            doctor = Doctor.objects.create(
                doctor_name=doctor_name,
                speciality=speciality
            )

            # Retrieve the LocationDetails object
            try:
                location = LocationDetails.objects.get(id=location_id)
                doctor.locations.add(location)
            except LocationDetails.DoesNotExist:
                return HttpResponse(
                    json.dumps({"error": "Location not found"}),
                    content_type='application/json',
                    status=404
                )

            # Prepare the response data
            response_data = {
                "id": doctor.id,
                "doctor_name": doctor.doctor_name,
                "speciality": doctor.speciality.name,
                "locations": [loc.location for loc in doctor.locations.all()]
            }

            return HttpResponse(
                json.dumps(response_data),
                content_type='application/json',
                status=201
            )

        except Exception as e:
            return HttpResponse(
                json.dumps({"error": str(e)}),
                content_type='application/json',
                status=400
            )

    return HttpResponse(
        json.dumps({"error": "Invalid request method"}),
        content_type='application/json',
        status=405
    )

@csrf_exempt
def update_doctor(request, doctor_id):
    if request.method == 'PUT':
        try:
            # Load JSON data from the request body
            data = json.loads(request.body)

            # Get the doctor object using doctor_id
            doctor = get_object_or_404(Doctor, id=doctor_id)

            # Update doctor_name if provided
            doctor_name = data.get('doctor_name')
            if doctor_name:
                doctor.doctor_name = doctor_name

            # Update speciality if provided
            speciality_name = data.get('speciality_name')
            if speciality_name:
                speciality = get_object_or_404(Speciality, name=speciality_name)
                doctor.speciality = speciality

            # Update location if provided
            location_id = data.get('location_id')
            if location_id:
                location = get_object_or_404(LocationDetails, id=location_id)
                doctor.locations.clear()  # Remove existing locations
                doctor.locations.add(location)

            # Save changes to the doctor object
            doctor.save()

            # Prepare response data
            response_data = {
                "id": doctor.id,
                "doctor_name": doctor.doctor_name,
                "speciality": doctor.speciality.name,
                "locations": [location.location for location in doctor.locations.all()]
            }

            # Return JSON response
            return HttpResponse(json.dumps(response_data), content_type='application/json')

        except Exception as e:
            return HttpResponse(f"An error occurred: {str(e)}", status=400)

    return HttpResponse("Invalid request method.", status=405)




@csrf_exempt
def delete_doctor(request, doctor_id):
    if request.method == 'DELETE':
        try:
            # Get the doctor object using doctor_id
            doctor = get_object_or_404(Doctor, id=doctor_id)

            # Delete the doctor
            doctor.delete()

            return HttpResponse("Doctor deleted successfully.", status=200)

        except:
            return HttpResponse("Unable to delete the doctor.", status=400)

    return HttpResponse("Invalid request method.", status=405)


def get_doctors(request):
    # Get query parameters if they exist
    doctor_name = request.GET.get('doctor_name')
    location_name = request.GET.get('location_name')
    speciality_name = request.GET.get('speciality_name')

    # Retrieve all doctors
    doctors = Doctor.objects.all()

    # Filter by doctor_name if provided
    if doctor_name:
        doctors = doctors.filter(doctor_name__icontains=doctor_name)

    # Filter by speciality_name if provided
    if speciality_name:
        # Check if speciality_name is not empty
        if speciality_name:
            # Retrieve the Speciality object by name
            try:
                speciality = Speciality.objects.get(name=speciality_name)
                # Filter doctors by speciality
                doctors = doctors.filter(speciality=speciality)
            except Speciality.DoesNotExist:
                # Handle case where Speciality does not exist
                return HttpResponse(
                    json.dumps({"error": "Speciality not found"}),
                    content_type='application/json',
                    status=404
                )

    # Filter by location_name if provided
    if location_name:
        # Filter doctors whose locations contain the location_name
        doctors = doctors.filter(locations__location__icontains=location_name).distinct()

    # Prepare response data
    response_data = []
    for doctor in doctors:
        response_data.append({
            "id": doctor.id,
            "doctor_name": doctor.doctor_name,
            "speciality": doctor.speciality.name,
            "locations": [location.location for location in doctor.locations.all()]
        })

    return HttpResponse(json.dumps(response_data), content_type='application/json')

