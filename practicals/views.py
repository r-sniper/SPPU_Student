from .models import Stream_Data, Subject_Data
from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    all_streams = Stream_Data.objects.values_list('stream', flat=True).distinct()
    return render(request, 'practicals/home.html', {
        'all_streams': all_streams,

    })


# When Go button is clicked from homepage
def default_subject(request):
    if request.POST.get("Go"):
        stream = request.POST.get('stream')
        year = request.POST.get('year')
        stream_id = Stream_Data.objects.filter(stream=stream, year=year).values_list('id', flat=True)
        subject_rows = Subject_Data.objects.filter(stream_id=stream_id)
        stream_id = list(stream_id)
        subjects = subject_rows.values_list('subject', flat=True).distinct()
        # print(subjects[0])
        assignment_title = subject_rows.filter(subject=subjects[0]).values_list('assignment_title', flat=True)
        problem_statement = subject_rows.filter(subject=subjects[0]).values_list('problem_statement', flat=True)
        list_of_assign = zip(assignment_title, problem_statement)
        # print(assignments)
        print(stream_id)
        print("test")
        print(stream_id[0])
        # return HttpResponse(stream_id)
        return render(request, 'practicals/subject.html', {
            'subjects': subjects, 'list_of_assign': list_of_assign, 'selected_subject_id': 1,
            'stream_id': int(stream_id[0])
        })
    else:

        return HttpResponse("Some Error Occured. ")
        '''
        stream_id = stream_id_passed
        subject_rows = Subject_Data.objects.filter(stream_id=stream_id)
        subjects = subject_rows.values_list('subject', flat=True).distinct()
        # print(subjects[0])
        index = 0
        for i in subjects:
            #print(str(i))
            if request.POST.get(i):
                break
            index += 1
        if index < subjects.count():
            assignment_title = subject_rows.filter(subject=subjects[index]).values_list('assignment_title', flat=True)
            problem_statement = subject_rows.filter(subject=subjects[index]).values_list('problem_statement', flat=True)
            list_of_assign = zip(assignment_title, problem_statement)
            # print(assignments)
            #print(stream_id)
            #print("test")
            # return HttpResponse(stream_id)
            return render(request, 'practicals/subject.html', {
                'subjects': subjects, 'list_of_assign': list_of_assign, 'selected_subject_id': index+1,
                'stream_id': int(stream_id)
            })
        else:
            assignments = subject_rows.filter(subject=subjects[int(selected_subject_passed)-1])
            count = 1
            for i in assignments:
                if request.POST.get(str(count)):
                    break
                count += 1
            print(str(count))
            if count < assignments.count():
                return render(request, 'practicals/code.html',{

                })

            return HttpResponse(assignments)

        '''


def change_subject(request, stream_id):
    subject_rows = Subject_Data.objects.filter(stream_id=stream_id)
    subjects = subject_rows.values_list('subject', flat=True).distinct()
    # print(subjects[0])
    index = 0
    for i in subjects:
        # print(str(i))
        if request.POST.get(i):
            break
        index += 1
    print(index)
    if index < subjects.count():
        assignment_title = subject_rows.filter(subject=subjects[index]).values_list('assignment_title', flat=True)
        problem_statement = subject_rows.filter(subject=subjects[index]).values_list('problem_statement', flat=True)
        list_of_assign = zip(assignment_title, problem_statement)
        # print(assignments)
        # print(stream_id)
        # print("test")
        # return HttpResponse(stream_id)
        return render(request, 'practicals/subject.html', {
            'subjects': subjects, 'list_of_assign': list_of_assign, 'selected_subject_id': index + 1,
            'stream_id': int(stream_id)
        })
    else:
        return HttpResponse("Subject not found")


def view_code(request,stream_id,subject_id):
    subject_rows = Subject_Data.objects.filter(stream_id=stream_id)
    subjects = subject_rows.values_list('subject', flat=True).distinct()
    assignments = subject_rows.filter(subject=subjects[int(subject_id) - 1])
    count = 0 #Used forloop.counter0 so startting from 0
    for i in assignments:
        if request.POST.get(str(count)):
            break
        count += 1
    print(str(count))

    if count < assignments.count():
        return render(request, 'practicals/code.html', {

        })
    return HttpResponse(assignments)