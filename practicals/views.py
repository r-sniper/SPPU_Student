from wsgiref.util import FileWrapper
from .models import Stream_Data, Subject_Data
from django.shortcuts import render
from django.http import HttpResponse
import os
import getpass

# Homepage
def home(request):
    #.distinct()to only get single copies of all streams
    all_streams = Stream_Data.objects.values_list('stream', flat=True).distinct()
    return render(request, 'practicals/home.html', {
        'all_streams': all_streams,
    })


# When Go button is clicked from homepage
def default_subject(request):
    if request.GET.get("Go"):
        stream = request.GET.get('stream')
        year = request.GET.get('year')
        stream_id = Stream_Data.objects.filter(stream=stream, year=year).values_list('id', flat=True)
        subject_rows = Subject_Data.objects.filter(stream_id=stream_id)
        stream_id = list(stream_id)
        subjects = subject_rows.values_list('subject', flat=True).distinct()
        assignment_title = subject_rows.filter(subject=subjects[0]).values_list('assignment_title', flat=True)
        problem_statement = subject_rows.filter(subject=subjects[0]).values_list('problem_statement', flat=True)
        list_of_assign = zip(assignment_title, problem_statement)
        return render(request, 'practicals/subject.html', {
            'subjects': subjects, 'list_of_assign': list_of_assign, 'selected_subject_id': 1,
            'stream_id': int(stream_id[0])
        })
    else:

        return HttpResponse("Some Error Occured. ")


def change_subject(request, stream_id):
    subject_rows = Subject_Data.objects.filter(stream_id=stream_id)
    subjects = subject_rows.values_list('subject', flat=True).distinct()
    # print(subjects[0])
    index = int(request.GET.get('subject'))
    print(getpass.getuser())
    if index:
        index -= 1
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


def view_code(request, stream_id, subject_id):
    stream_obj = Stream_Data.objects.get(pk=stream_id)
    stream = stream_obj.stream
    year = stream_obj.year
    #subject_rows = Subject_Data.objects.filter(stream_id=stream_id) The below line will the exactly same thing
    subject_rows = stream_obj.subject_data_set.all()
    subjects = subject_rows.values_list('subject', flat=True).distinct()
    assignments = subject_rows.filter(subject=subjects[int(subject_id) - 1])
    subject = subjects[int(subject_id) - 1]
    count = request.GET.get('code')  # It returns value from name (value = requrst.GET.get(name)
    print(count)
    # for i in assignments:
    #     if request.GET.get(str(count)):
    #         break
    #     count += 1
    # print(str(count))
    # fp = open('codes/Computer Engineering-FE/FPL-1/1.helloworld.c')

    base_directory = ''
    if getpass.getuser() == 'rsniper':
        base_directory = '/home/rsniper/SPPU_Student/'
    if count:

        filename = assignments[int(count)].filename
        directory = base_directory + 'codes/' + stream + '/' + year + '/' + subject + '/' + filename
        fp = open(directory, 'r')
        code = fp.read().split('*/') #To not display question while viewing code
        fp.close()
        return render(request, 'practicals/code.html', {
            'assignment': assignments[int(count)], 'code': code[1],
        })
    else:
        count = request.GET.get('download')
        if count:
            filename = assignments[int(count)].filename
            directory = base_directory + 'codes/' + stream + '/' + year + '/' + subject + '/' + filename
            fp = open(directory, 'r')
            fileWrap = FileWrapper(fp)
            response = HttpResponse(fileWrap, content_type='application/force-download')
            response['Content-Disposition'] = 'attachment; filename=%s' % filename
            response['Content-Length'] = os.path.getsize(directory)
            return response
        else:
            return HttpResponse("Oops! Something went wrong.")


# This adds all the new codes to the database
# Warning do not use on hosted server- only on local server.
def refresh(request):
    if getpass.getuser() == 'rsniper':
        return HttpResponse("Please don't use this URL just yet")
    osdir = os.walk('codes/')

    every_directory = set((), )
    for root, dirs, files in osdir:
        if root.count('/') == 3 and files:
            # print(root)
            # print(files)
            line = root.split('/')
            for f in files:
                temp = (line[1], line[2], line[3], f)
                every_directory.add(temp)

                # print('Stream:' + line[2])

    for s in every_directory:
        stream = s[0]
        year = s[1]
        subject = s[2]
        filename = s[3]
        title = filename.split('.')[1]
        #Important add base_directory to deirctory when deploying

        # base_directory = '/home/rsniper/SPPU_Student/'
        directory = 'codes/' + stream + '/' + year + '/' + subject + '/' + filename
        try:
            fp = open(directory, 'r')
        except IOError:
            return HttpResponse("File connot be opened")
        problem = fp.read().split("/*")[1].split("*/")[0]
        fp.close()
        if Stream_Data.objects.filter(stream=stream, year=year):
            print("Exists")
        else:
            newStream = Stream_Data(stream=stream, year=year)
            newStream.save()
            print("Dosent")
        if Subject_Data.objects.filter(stream_id=Stream_Data.objects.filter(stream=stream, year=year)[0],
                                       subject=subject, assignment_title=title, problem_statement=problem,
                                       filename=filename):
            print("Exists")
        else:
            newSubject = Subject_Data(stream_id=Stream_Data.objects.filter(stream=stream, year=year)[0],
                                      subject=subject, assignment_title=title, problem_statement=problem,
                                      filename=filename)
            newSubject.save()
    return HttpResponse("Done successfully")
